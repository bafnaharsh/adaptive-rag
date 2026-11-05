"""
API routes for RAG operations.
"""

import asyncio
import re
from pathlib import Path

from fastapi import APIRouter, File, Header, HTTPException, UploadFile
from langchain_core.messages import AIMessage, HumanMessage

from src.core.config import settings
from src.core.logger import logger
from src.memory import get_session_history
from src.models.query_request import QueryRequest
from src.rag import graph_builder, store

router = APIRouter()

HISTORY_MESSAGES = 10
ALLOWED_EXTENSIONS = {".pdf", ".txt", ".md"}


@router.post("/rag/query")
async def rag_query(req: QueryRequest):
    """Answer one chat turn; the session's earlier turns are passed along for follow-up questions."""
    history = get_session_history(req.session_id)
    earlier = (await history.aget_messages())[-HISTORY_MESSAGES:]
    try:
        # answer() is blocking (LLM + retrieval calls), so keep it off the event loop
        result = await asyncio.to_thread(graph_builder.answer, req.query, earlier)
    except Exception as e:
        logger.exception("answer() failed")
        raise HTTPException(status_code=500, detail=str(e) or type(e).__name__)
    await history.aadd_messages([HumanMessage(content=req.query), AIMessage(content=result["answer"])])
    return {**result, "session_id": req.session_id}


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
