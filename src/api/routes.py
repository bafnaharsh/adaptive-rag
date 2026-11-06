"""
API routes for RAG operations.
"""

import asyncio
import json
import re
from datetime import datetime, timezone
from pathlib import Path

from fastapi import APIRouter, File, Header, HTTPException, UploadFile
from fastapi.responses import StreamingResponse
from langchain_core.messages import AIMessage, HumanMessage
from starlette.concurrency import iterate_in_threadpool

from src.core.config import settings
from src.core.logger import logger
from src.memory import get_session_history
from src.models.query_request import QueryRequest
from src.rag import agent, graph_builder, store

router = APIRouter()

HISTORY_MESSAGES = 10
ALLOWED_EXTENSIONS = {".pdf", ".txt", ".md"}


def _log_turn(req: QueryRequest, result: dict) -> None:
    """Append every answered turn (question, answer, citations, trace) to DATA_DIR/conversations.jsonl so answers can
    be reviewed and graded later; chat history itself may live only in memory."""
    line = {"ts": datetime.now(timezone.utc).isoformat(), "session_id": req.session_id, "question": req.query, **result}
    with open(settings.DATA_DIR / "conversations.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps(line, ensure_ascii=False) + "\n")


@router.post("/rag/query")
async def rag_query(req: QueryRequest):
    """Answer one chat turn; the session's earlier turns are passed along for follow-up questions."""
    history = get_session_history(req.session_id)
    earlier = (await history.aget_messages())[-HISTORY_MESSAGES:]
    try:
        # answer() is blocking (LLM + retrieval calls), so keep it off the event loop
        answer = agent.answer if req.mode == "agent" else graph_builder.answer
        result = await asyncio.to_thread(answer, req.query, earlier)
    except Exception as e:
        logger.exception("answer() failed")
        raise HTTPException(status_code=500, detail=str(e) or type(e).__name__)
    await history.aadd_messages([HumanMessage(content=req.query), AIMessage(content=result["answer"])])
    _log_turn(req, result)
    return {**result, "session_id": req.session_id}


@router.post("/rag/query/stream")
async def rag_query_stream(req: QueryRequest):
    """Server-sent events: one `step` event per finished pipeline node, then `final` (or `error`)."""
    history = get_session_history(req.session_id)
    earlier = (await history.aget_messages())[-HISTORY_MESSAGES:]

    async def events():
        try:
            # stream_answer() blocks on LLM and retrieval calls: advance it in the threadpool, off the event loop
            stream = agent.stream_agent if req.mode == "agent" else graph_builder.stream_answer
            async for kind, data in iterate_in_threadpool(stream(req.query, earlier)):
                if kind == "final":
                    data = {**data, "session_id": req.session_id}
                    await history.aadd_messages([HumanMessage(content=req.query), AIMessage(content=data["answer"])])
                    _log_turn(req, data)
                yield f"event: {kind}\ndata: {json.dumps(data, ensure_ascii=False)}\n\n"
        except Exception as e:  # the stream has started, so an error must travel as an event, not a status code
            logger.exception("stream failed")
            yield f"event: error\ndata: {json.dumps({'message': str(e) or type(e).__name__})}\n\n"

    return StreamingResponse(events(), media_type="text/event-stream", headers={"Cache-Control": "no-cache"})


@router.get("/rag/info")
async def info():
    return {"llm": settings.LLM_MODEL, "web": "tavily" if settings.TAVILY_API_KEY else "duckduckgo",
            "modes": ["ladder", "agent"], "board": True}


@router.post("/rag/documents/upload")
async def upload_file(file: UploadFile = File(...), description: str = Header("", alias="X-Description")):
    """Save an uploaded PDF/TXT/MD under DATA_DIR/uploads and index it."""
    # Strip any directory part (either separator) and odd characters: the name becomes a path on disk
    name = re.sub(r"[^\w.\- ]", "_", (file.filename or "").replace("\\", "/").rsplit("/", 1)[-1]).strip(". ")
    if Path(name).suffix.lower() not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Only .pdf, .txt and .md files are supported")
    path = settings.DATA_DIR / "uploads" / name
    path.parent.mkdir(parents=True, exist_ok=True)
    await asyncio.to_thread(path.write_bytes, await file.read())
    try:
        document = await asyncio.to_thread(store.add_document, path, description)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    return {"status": True, "document": document}


@router.get("/rag/documents")
async def list_documents():
    return await asyncio.to_thread(store.list_documents)
