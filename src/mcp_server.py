"""
MCP server: lets a harness (Claude Code, Antigravity, Copilot) run the adaptive research loop with its own model.
The tools only do retrieval, web search and citation checking; the harness model does the reasoning.

Run: python -m src.mcp_server   (stdio; stdout carries JSON-RPC only, logs go to stderr)
"""

from typing import Literal

from mcp.server.fastmcp import FastMCP

from src.models.evidence import Chunk
from src.rag import citations as citations_mod
from src.rag import store, web

PROTOCOL = """\
Research protocol. Climb the tiers only as far as needed and say which tier answered.

Tier 0 - answer from your own knowledge ONLY if the question is not about the indexed documents, is not
time-sensitive and you know it reliably. Label it "(model knowledge, not verified)".
Tier 1 - search_documents(query, mode="dense"). Reason step by step: does the evidence fully answer the question?
Tier 2 - if not, search_documents(mode="hybrid") with the query plus 2-3 rewritten or decomposed queries in
extra_queries (BM25 + dense, reranked, filtered).
Tier 3 - if still not, web_search(query).

Answer only from the evidence, with [n] markers. Then call verify_citations with a VERBATIM quote from each cited
source (citations: [{n, source_id, quote}], source_id = the id of the search hit). Fix or drop citations that do not
verify. End with a Sources list (PDF: file + page; web: URL).
"""

mcp = FastMCP("adaptive-rag", instructions=PROTOCOL)


def _hit(c: Chunk) -> dict:
    d = {"id": c.id, "label": c.label(), "source": c.source, "page": c.page, "score": round(c.score, 4), "text": c.text}
    if c.id.startswith("web:"):
        d["url"] = c.source
    return d


@mcp.tool()
def list_documents() -> list[dict]:
    """List the indexed documents: [{doc_id, name, description, pages, chunks}]."""
    return store.list_documents()


@mcp.tool()
def ingest_document(path: str, description: str = "") -> dict:
    """Index a local PDF, TXT or MD file so search_documents can find it. `path` must be an absolute local path.
    Returns {doc_id, name, pages, chunks, status}; status is "exists" when the same file was indexed before."""
    return store.add_document(path, description)


@mcp.tool()
def search_documents(
    query: str,
    mode: Literal["dense", "hybrid", "keyword"] = "hybrid",
    k: int = 8,
    extra_queries: list[str] = [],
    doc_ids: list[int] = [],
) -> list[dict]:
    """Search the indexed documents. Returns [{id, label, source, page, score, text}], best first.
    mode "dense" = embedding similarity (cheap first try); "hybrid" = BM25 + dense for the query and every
    extra_queries rewrite, reranked and filtered (may return [] = nothing relevant); "keyword" = BM25 only.
    doc_ids restricts the search to those documents (empty = all)."""
    ids = doc_ids or None
    if mode == "dense":
        chunks = store.dense_search(query, k, ids)
    elif mode == "keyword":
        chunks = store.keyword_search(query, k, ids)
    else:
        chunks = store.hybrid_search([query, *extra_queries], k, ids)
    return [_hit(c) for c in chunks]


@mcp.tool()
def web_search(query: str, k: int = 5) -> list[dict]:
    """Search the web (Tavily if a key is set, else DuckDuckGo). Returns [{id, label, source, url, page, score, text}]
    passages from the top pages; [] when offline. Use as the last tier."""
    return [_hit(c) for c in web.web_search(query, k)]


@mcp.tool()
def verify_citations(citations: list[dict]) -> dict:
    """Check that every quote really appears in the cited source. citations: [{n, source_id, quote}] where source_id is
    the `id` of a search hit and quote is copied VERBATIM from its text. Returns {"verified": "x/y", "citations": [...]}
    with per-citation verified/reason/label; fix or drop the ones that fail."""
    out = citations_mod.verify(citations)
    return {"verified": f"{sum(c['verified'] for c in out)}/{len(out)}", "citations": out}


@mcp.tool()
def research(question: str) -> dict:
    """Run the whole adaptive pipeline server-side and return {answer, rendered, citations, tier, trace, verified}.
    It calls its own LLM backend (LLM_MODEL, default the `claude` CLI), so it is slower than doing the protocol
    yourself with the other tools; prefer that when you can reason yourself."""
    from src.rag import graph_builder  # lazy: heavy imports, and only this tool needs them

    return graph_builder.answer(question)


@mcp.prompt()
def adaptive_research(question: str) -> str:
    """Answer a question with the adaptive research protocol."""
    return f"{PROTOCOL}\nQuestion: {question}"


if __name__ == "__main__":
    mcp.run()
