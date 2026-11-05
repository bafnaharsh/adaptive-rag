import asyncio
import sys
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from src import mcp_server
from src.models.evidence import Chunk
from src.rag import citations, graph_builder, store, web

ROOT = Path(__file__).resolve().parents[1]
TOOLS = {"list_documents", "ingest_document", "search_documents", "web_search", "verify_citations", "research"}


def test_stdio_round_trip(tmp_path):
    # A real subprocess: any stray stdout print would corrupt the JSON-RPC stream and fail initialize().
    params = StdioServerParameters(
        command=sys.executable, args=["-m", "src.mcp_server"], cwd=ROOT, env={"DATA_DIR": str(tmp_path)}
    )

    async def run():
        async with stdio_client(params) as (read, write), ClientSession(read, write) as session:
            init = await session.initialize()
            tools = {t.name for t in (await session.list_tools()).tools}
            prompts = {p.name for p in (await session.list_prompts()).prompts}
            prompt = await session.get_prompt("adaptive_research", {"question": "why?"})
            return init, tools, prompts, prompt

    init, tools, prompts, prompt = asyncio.run(asyncio.wait_for(run(), 120))
    assert init.serverInfo.name == "adaptive-rag"
    assert "Tier 3" in init.instructions and "verify_citations" in init.instructions
    assert tools == TOOLS
    assert "adaptive_research" in prompts
    assert "Question: why?" in prompt.messages[0].content.text


def test_search_modes(monkeypatch):
    calls = []
    doc = Chunk(id="doc:1", text="alpha", source="a.pdf", page=3, score=0.5)
    for name in ("dense_search", "keyword_search", "hybrid_search"):
        monkeypatch.setattr(store, name, lambda *a, _n=name: calls.append((_n, *a)) or [doc])

    hits = mcp_server.search_documents("q", mode="dense", k=2)
    assert hits == [{"id": "doc:1", "label": "a.pdf, p. 3", "source": "a.pdf", "page": 3, "score": 0.5, "text": "alpha"}]
    mcp_server.search_documents("q", mode="keyword", doc_ids=[7])
    mcp_server.search_documents("q", extra_queries=["r", "s"])
    assert calls == [
        ("dense_search", "q", 2, None),
        ("keyword_search", "q", 8, [7]),
        ("hybrid_search", ["q", "r", "s"], 8, None),
    ]


def test_web_search_adds_url(monkeypatch):
    monkeypatch.setattr(web, "web_search", lambda q, k: [Chunk(id="web:ab", text="t", source="https://x.io", score=1.0)])
    (hit,) = mcp_server.web_search("q")
    assert hit["url"] == "https://x.io" and hit["label"] == "https://x.io"


def test_verify_citations_counts(monkeypatch):
    monkeypatch.setattr(citations, "verify", lambda cs: [{**c, "verified": c["quote"] == "ok"} for c in cs])
    out = mcp_server.verify_citations([{"source_id": "doc:1", "quote": "ok"}, {"source_id": "doc:1", "quote": "bad"}])
    assert out["verified"] == "1/2" and len(out["citations"]) == 2


def test_documents_and_research(monkeypatch):
    monkeypatch.setattr(store, "list_documents", lambda: [{"doc_id": 1}])
    monkeypatch.setattr(store, "add_document", lambda path, description: {"doc_id": 2, "path": path, "d": description})
    monkeypatch.setattr(graph_builder, "answer", lambda q: {"answer": q, "tier": "rag"})
    assert mcp_server.list_documents() == [{"doc_id": 1}]
    assert mcp_server.ingest_document("/x.pdf", "desc") == {"doc_id": 2, "path": "/x.pdf", "d": "desc"}
    assert mcp_server.research("q")["tier"] == "rag"
