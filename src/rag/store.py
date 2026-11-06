"""
Persistent document index: one SQLite file at settings.DATA_DIR / "rag.sqlite" holding documents, page-level chunks,
their embeddings (local fastembed model, no API key) and an FTS5 table for BM25.
"""

import contextlib
import hashlib
import io
import re
import sqlite3
import sys
import threading
import time
from dataclasses import replace
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
from pypdf import PdfReader
from pypdf.errors import PyPdfError

from src.core.config import settings
from src.core.logger import logger
from src.models.evidence import Chunk

CHUNK_CHARS, CHUNK_OVERLAP = 1000, 150
# ms-marco-MiniLM logit. On the iPhone manuals, off-topic queries score <= -8.8, answers +2..+9, and weak but
# relevant chunks (e.g. a torque step) dip to about -0.5, so -2 keeps recall and still empties unrelated queries.
RERANK_MIN = -2.0
_BREAKS = [re.compile(p) for p in (r"\n\s*\n", r"[.!?][\"')\]]?\s", r"\n", r"\s")]  # paragraph > sentence > line > word

_SCHEMA = """
PRAGMA journal_mode=WAL;
CREATE TABLE IF NOT EXISTS documents (
    id INTEGER PRIMARY KEY, name TEXT NOT NULL, description TEXT NOT NULL, sha256 TEXT NOT NULL UNIQUE,
    pages INTEGER NOT NULL, chunks INTEGER NOT NULL, added_at TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS chunks (
    id INTEGER PRIMARY KEY, doc_id INTEGER NOT NULL REFERENCES documents(id), page INTEGER, text TEXT NOT NULL,
    embedding BLOB NOT NULL);
CREATE INDEX IF NOT EXISTS chunks_doc ON chunks(doc_id);
CREATE VIRTUAL TABLE IF NOT EXISTS chunks_fts USING fts5(text, content='chunks', content_rowid='id',
    tokenize='porter unicode61');
CREATE TABLE IF NOT EXISTS web_chunks (id TEXT PRIMARY KEY, url TEXT NOT NULL, title TEXT NOT NULL, text TEXT NOT NULL);
"""

_lock = threading.Lock()
_models: dict = {}
_matrices: dict = {}  # db path -> (max chunk id, chunk ids, doc ids, row-normalized embeddings)


@contextlib.contextmanager
def _db():
    """Fresh connection per call (thread-safe); commits on success."""
    con = sqlite3.connect(settings.DATA_DIR / "rag.sqlite", timeout=30)
    try:
        con.executescript(_SCHEMA)
        with con:
            yield con
    finally:
        con.close()


def _model(name: str, cls):
    with _lock:
        if name not in _models:
            # Downloads log via tqdm/loguru (stderr) but fastembed has a stray print(): keep stdout clean for MCP stdio.
            with contextlib.redirect_stdout(sys.stderr):
                _models[name] = cls(name, cache_dir=str(settings.DATA_DIR / "models"))
        return _models[name]


def _embedder():
    from fastembed import TextEmbedding

    return _model(settings.EMBED_MODEL, TextEmbedding)


def _reranker():
    from fastembed.rerank.cross_encoder import TextCrossEncoder

    return _model(settings.RERANK_MODEL, TextCrossEncoder)


def _clean(text: str) -> str:
    lines = (" ".join(line.split()) for line in text.replace("\x00", "").splitlines())
    return re.sub(r"\n{3,}", "\n\n", "\n".join(lines)).strip()


def _split(text: str) -> list[str]:
    """~CHUNK_CHARS pieces overlapping by ~CHUNK_OVERLAP, cut at the best boundary in the second half of the window.
    Whitespace is collapsed in the result so a quote copied from a chunk matches it verbatim."""
    out, start = [], 0
    while start < len(text):
        end = min(start + CHUNK_CHARS, len(text))
        if end < len(text):
            for pat in _BREAKS:
                cuts = [m.end() for m in pat.finditer(text, start + CHUNK_CHARS // 2, end)]
                if cuts:
                    end = cuts[-1]
                    break
        piece = " ".join(text[start:end].split())
        if piece:
            out.append(piece)
        if end >= len(text):
            break
        ws = re.compile(r"\s").search(text, end - CHUNK_OVERLAP, end)  # start the overlap on a word boundary
        start = ws.end() if ws else end
    return out


def _read_pages(name: str, data: bytes) -> tuple[int, list[tuple[int | None, str]]]:
    """(page count, [(1-based page or None, cleaned text)]) with empty pages dropped."""
    ext = Path(name).suffix.lower()
    if ext == ".pdf":
        try:
            reader = PdfReader(io.BytesIO(data))
        except PyPdfError as e:
            raise ValueError(f"Unreadable PDF {name}: {e}") from e
        pages = []
        for n, page in enumerate(reader.pages, 1):
            try:
                pages.append((n, _clean(page.extract_text() or "")))
            except Exception as e:  # one malformed page must not sink a 500-page manual
                logger.warning("%s p.%d: text extraction failed: %s", name, n, e)
        total = len(reader.pages)
    elif ext in (".txt", ".md"):
        pages, total = [(None, _clean(data.decode("utf-8", errors="replace")))], 1
    else:
        raise ValueError(f"Unsupported file type {ext or '(none)'}: use .pdf, .txt or .md")
    return total, [(n, t) for n, t in pages if t]


def _doc_dict(row) -> dict:
    return dict(zip(("doc_id", "name", "description", "pages", "chunks"), row))


def _existing(sha: str) -> dict | None:
    with _db() as con:
        row = con.execute("SELECT id, name, description, pages, chunks FROM documents WHERE sha256 = ?", (sha,)).fetchone()
    return {**_doc_dict(row), "status": "exists"} if row else None


def add_document(path: str | Path, description: str = "", name: str | None = None) -> dict:
    """Index a PDF / TXT / MD file. Chunks never span PDF pages, so every chunk has its 1-based page.
    Idempotent on file content: re-adding the same bytes returns the existing doc with "status": "exists".
    Returns {"doc_id": int, "name": str, "description": str, "pages": int, "chunks": int, "status": "added"|"exists"}.
    Raises ValueError for unsupported extensions or files with no extractable text."""
    path = Path(path)
    name = name or path.name
    data = path.read_bytes()
    sha = hashlib.sha256(data).hexdigest()
    if existing := _existing(sha):
        return existing

    t0 = time.perf_counter()
    total, pages = _read_pages(path.name, data)
    chunks = [(n, piece) for n, text in pages for piece in _split(text)]
    if not chunks:
        raise ValueError(f"No extractable text in {path.name} (scanned PDF?)")
    vectors = list(_embedder().passage_embed([text for _, text in chunks], batch_size=32))
    try:
        with _db() as con:
            doc_id = con.execute(
                "INSERT INTO documents (name, description, sha256, pages, chunks, added_at) VALUES (?, ?, ?, ?, ?, ?)",
                (name, description, sha, total, len(chunks), datetime.now(timezone.utc).isoformat()),
            ).lastrowid
            for (page, text), vec in zip(chunks, vectors):
                cid = con.execute(
                    "INSERT INTO chunks (doc_id, page, text, embedding) VALUES (?, ?, ?, ?)",
                    (doc_id, page, text, np.asarray(vec, dtype=np.float32).tobytes()),
                ).lastrowid
                con.execute("INSERT INTO chunks_fts (rowid, text) VALUES (?, ?)", (cid, text))
    except sqlite3.IntegrityError:
        if existing := _existing(sha):  # the same file was added concurrently
            return existing
        raise
    logger.info("Indexed %s: %d pages, %d chunks in %.1fs", name, total, len(chunks), time.perf_counter() - t0)
    return {"doc_id": doc_id, "name": name, "description": description, "pages": total, "chunks": len(chunks),
            "status": "added"}


def list_documents() -> list[dict]:
    """[{"doc_id": int, "name": str, "description": str, "pages": int, "chunks": int}], oldest first."""
    with _db() as con:
        return [_doc_dict(r) for r in con.execute("SELECT id, name, description, pages, chunks FROM documents ORDER BY id")]


def _load(ids: list[int], scores: list[float]) -> list[Chunk]:
    """Chunks for doc chunk ids, in the given order, carrying the given scores."""
    if not ids:
        return []
    with _db() as con:
        rows = con.execute(
            f"SELECT c.id, c.text, d.name, c.page, d.description FROM chunks c JOIN documents d ON d.id = c.doc_id "
            f"WHERE c.id IN ({','.join('?' * len(ids))})", ids).fetchall()
    by_id = {r[0]: r for r in rows}
    return [Chunk(f"doc:{i}", by_id[i][1], by_id[i][2], by_id[i][3], by_id[i][4], s)
            for i, s in zip(ids, scores) if i in by_id]


def _matrix():
    """All chunk embeddings of the current DB, cached until a chunk is added (checked per call, so another process's
    ingest is seen too)."""
    path = str(settings.DATA_DIR / "rag.sqlite")
    with _db() as con:
        max_id = con.execute("SELECT max(id) FROM chunks").fetchone()[0]
        cached = _matrices.get(path)
        if cached is None or cached[0] != max_id:
            rows = con.execute("SELECT id, doc_id, embedding FROM chunks ORDER BY id").fetchall()
            dim = len(rows[0][2]) // 4 if rows else 0
            mat = np.frombuffer(b"".join(r[2] for r in rows), dtype=np.float32).reshape(len(rows), dim)
            mat = mat / np.maximum(np.linalg.norm(mat, axis=1, keepdims=True), 1e-12)
            cached = _matrices[path] = (max_id, np.array([r[0] for r in rows]), np.array([r[1] for r in rows]), mat)
    return cached[1:]


def dense_search(query: str, k: int = 6, doc_ids: list[int] | None = None) -> list[Chunk]:
    """Tier 1 (plain RAG): top-k chunks by embedding cosine similarity. score = cosine."""
    ids, docs, mat = _matrix()
    if not len(ids) or not query.strip():
        return []
    q = np.asarray(next(iter(_embedder().query_embed(query))), dtype=np.float32)
    # shortcut: brute-force cosine over all chunks, fine to ~200k chunks; beyond that use sqlite-vec or FAISS.
    sims = mat @ (q / max(np.linalg.norm(q), 1e-12))
    if doc_ids:
        sims = np.where(np.isin(docs, doc_ids), sims, -np.inf)
    top = [i for i in np.argsort(-sims)[:k] if np.isfinite(sims[i])]
    return _load([int(ids[i]) for i in top], [float(sims[i]) for i in top])


def keyword_search(query: str, k: int = 20, doc_ids: list[int] | None = None) -> list[Chunk]:
    """BM25 over the FTS5 index. score = -bm25 (higher is better). Any user text is safe (FTS syntax escaped)."""
    terms = re.findall(r"\w+", query)
    if not terms:
        return []
    match = " OR ".join(f'"{t}"' for t in terms)  # \w+ tokens can't contain quotes, so this is always valid FTS
    sql = "SELECT rowid, -bm25(chunks_fts) FROM chunks_fts WHERE chunks_fts MATCH ?"
    params: list = [match]
    if doc_ids:
        sql += f" AND rowid IN (SELECT id FROM chunks WHERE doc_id IN ({','.join('?' * len(doc_ids))}))"
        params += list(doc_ids)
    with _db() as con:
        rows = con.execute(sql + " ORDER BY bm25(chunks_fts) LIMIT ?", [*params, k]).fetchall()
    return _load([r[0] for r in rows], [r[1] for r in rows])


def _rerank(queries: list[str], chunks: list[Chunk], min_score: float | None) -> list[Chunk]:
    """All chunks, best first, scored by the max cross-encoder score over the queries."""
    if not chunks:
        return []
    texts = [c.text for c in chunks]
    scores = np.max([list(_reranker().rerank(q, texts, batch_size=16)) for q in queries], axis=0)
    ranked = sorted((replace(c, score=float(s)) for c, s in zip(chunks, scores)), key=lambda c: -c.score)
    return [c for c in ranked if min_score is None or c.score >= min_score]


def _near_duplicate(a: Chunk, b: Chunk) -> bool:
    wa, wb = set(a.text.lower().split()), set(b.text.lower().split())
    overlap = len(wa & wb) / max(len(wa | wb), 1)
    return overlap >= (0.5 if (a.source, a.page) == (b.source, b.page) else 0.9)


def hybrid_search(queries: str | list[str], k: int = 8, doc_ids: list[int] | None = None) -> list[Chunk]:
    """Tier 2: dense + BM25 for every query, reciprocal-rank fusion, cross-encoder rerank where a chunk's score is the
    MAX over all the queries (the extra ones are rewrites / sub-questions), drop chunks below the relevance threshold
    and near-duplicates, order by fusing the rerank and BM25+dense rankings, return the best k. score = rerank score.
    May return [] when nothing is relevant (that is the signal to escalate to web)."""
    queries = [queries] if isinstance(queries, str) else [q for q in queries if q.strip()]
    fused: dict[str, list] = {}
    for q in queries:
        for ranked in (dense_search(q, 20, doc_ids), keyword_search(q, 20, doc_ids)):
            for rank, c in enumerate(ranked):
                fused.setdefault(c.id, [c, 0.0])[1] += 1 / (60 + rank + 1)
    candidates = [c for c, _ in sorted(fused.values(), key=lambda x: -x[1])[:30]]
    fusion_rank = {c.id: i for i, c in enumerate(candidates)}
    reranked = _rerank(queries, candidates, RERANK_MIN)
    rerank_rank = {c.id: i for i, c in enumerate(reranked)}
    # The cross-encoder underrates terse tables (a part-number list scored 13th although BM25 ranked it 3rd), so the
    # final order fuses its ranking with the BM25+dense one instead of trusting it alone.
    reranked.sort(key=lambda c: -(1 / (61 + rerank_rank[c.id]) + 1 / (61 + fusion_rank[c.id])))
    kept: list[Chunk] = []
    for c in reranked:
        if not any(_near_duplicate(c, other) for other in kept):
            kept.append(c)
        if len(kept) == k:
            break
    return kept


def rerank(query: str, chunks: list[Chunk], k: int, min_score: float | None = None) -> list[Chunk]:
    """Cross-encoder rerank of any chunks (also used for web passages). score = rerank score."""
    return _rerank([query], chunks, min_score)[:k]


def neighbors(chunk_id: str, after: int = 2) -> list[Chunk]:
    """The `after` chunks that follow a doc chunk in the same document, in reading order. Search finds a section by
    its first page (the one carrying the title); the steps of the procedure or the rest of the table follow it."""
    kind, _, key = chunk_id.partition(":")
    if kind != "doc" or not key.isdigit():
        return []
    with _db() as con:
        ids = [r[0] for r in con.execute(
            "SELECT id FROM chunks WHERE doc_id = (SELECT doc_id FROM chunks WHERE id = ?) AND id > ? ORDER BY id LIMIT ?",
            (int(key), int(key), after))]
    return _load(ids, [0.0] * len(ids))


def get_chunk(chunk_id: str) -> Chunk | None:
    """Look up "doc:<int>" or "web:<hex>" (web passages saved by save_web_chunks). None when unknown."""
    kind, _, key = chunk_id.partition(":")
    if kind == "doc" and key.isdigit():
        found = _load([int(key)], [0.0])
        return found[0] if found else None
    if kind == "web":
        with _db() as con:
            row = con.execute("SELECT url, title, text FROM web_chunks WHERE id = ?", (chunk_id,)).fetchone()
        return Chunk(chunk_id, row[2], row[0], None, row[1]) if row else None
    return None


def save_web_chunks(chunks: list[Chunk]) -> None:
    """Persist web passages so get_chunk (and citation verification) finds them later, even in another process."""
    with _db() as con:
        con.executemany("INSERT OR REPLACE INTO web_chunks (id, url, title, text) VALUES (?, ?, ?, ?)",
                        [(c.id, c.source, c.title, c.text) for c in chunks])


def warm() -> None:
    """Load both models and the embedding matrix now instead of on the first question. The reranker must also run
    once: its first inference in a process took ~13 s (ONNX session start), later ones ~2.5 s for 49 passages."""
    dense_search("warm up", 1)
    list(_reranker().rerank("warm up", ["warm up the cross-encoder"]))
