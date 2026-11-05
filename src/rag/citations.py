"""
Grounding: every citation names a source chunk and quotes it verbatim; a citation counts as verified only when the
quote is really in that chunk's text. Deterministic, no LLM.
"""

import re
import unicodedata
from difflib import SequenceMatcher

from src.models.evidence import Chunk
from src.rag import store

MIN_QUOTE = 12  # shorter quotes ("20 hours") occur almost anywhere, so they prove nothing
FUZZY = 0.9
_PUNCT = str.maketrans({"‘": "'", "’": "'", "‚": "'", "‛": "'", "′": "'",
                        "“": '"', "”": '"', "„": '"', "‟": '"', "″": '"',
                        "‐": "-", "‑": "-", "‒": "-", "–": "-", "—": "-", "―": "-",
                        "−": "-"})


def _norm(text: str) -> str:
    text = unicodedata.normalize("NFKC", text).lower().translate(_PUNCT)  # NFKC also turns "…" into "..."
    return re.sub(r"\s+", " ", text).strip()


def _find(seg: str, src: str, pos: int) -> int:
    """End of seg's match in src at or after pos, else -1. Exact first, then the best difflib window, which tolerates
    PDF artifacts (hyphenation, stray spaces)."""
    i = src.find(seg, pos)
    if i >= 0:
        return i + len(seg)
    if len(seg) < MIN_QUOTE:
        return -1
    tail, words = src[pos:], re.findall(r"\w+", seg)
    best, end = FUZZY, -1
    for block in SequenceMatcher(None, tail, seg, autojunk=False).get_matching_blocks():
        start = max(0, block.a - block.b)
        window = tail[start:start + len(seg) * 11 // 10]  # slack for the characters hyphenation and spacing add
        ratio = SequenceMatcher(None, window, seg, autojunk=False).ratio()
        skeleton = re.sub(r"\W+", "", window)
        # every quoted word must really be there: the ratio alone passes a changed number or an inserted "not"
        if ratio >= best and all(w in skeleton for w in words):
            best, end = ratio, pos + start + len(window)
    return end


def _matches(segments: list[str], text: str) -> bool:
    src, pos = _norm(text), 0
    for seg in segments:  # "..." in a quote skips words, so its segments must appear in order
        pos = _find(seg, src, pos)
        if pos < 0:
            return False
    return True


def verify(citations: list[dict], evidence: dict[str, Chunk] | None = None) -> list[dict]:
    """citations: [{"n": int, "source_id": "doc:12" | "web:ab12", "quote": str}].
    Looks each source up in `evidence` (id -> Chunk), else store.get_chunk. Returns new dicts with the input keys plus
    "verified": bool, "reason": str ("" when verified), "source": str, "page": int | None, "url": str | None,
    "title": str (web page title, or the document description), "label": str (Chunk.label())."""
    out = []
    for c in citations:
        sid = str(c.get("source_id") or "")
        chunk = (evidence or {}).get(sid) or (store.get_chunk(sid) if sid else None)
        segments = [s for s in (p.strip(" \"'.") for p in _norm(str(c.get("quote") or "")).split("...")) if s]
        if chunk is None:
            reason = "unknown source id"
        elif len(" ".join(segments)) < MIN_QUOTE:
            reason = f"quote too short to verify (under {MIN_QUOTE} characters)"
        elif not _matches(segments, chunk.text):
            reason = "quote not found in the source text"
        else:
            reason = ""
        out.append({**c, "verified": not reason, "reason": reason,
                    "source": chunk.source if chunk else "", "page": chunk.page if chunk else None,
                    "url": chunk.source if chunk and chunk.id.startswith("web:") else None,
                    "title": chunk.title if chunk else "", "label": chunk.label() if chunk else sid})
    return out


def render(answer: str, citations: list[dict]) -> str:
    """The answer markdown followed by a numbered Sources list built from verify() output, e.g.
    - [1] iphone_user_guide.pdf, p. 42 ✓ — “quote”   /   - [2] [Title](https://...) ✓ — “quote”."""
    if not citations:
        return answer
    lines = []
    for c in citations:
        target = f"[{c.get('title') or c['url']}]({c['url']})" if c.get("url") else c["label"]
        mark = "✓" if c["verified"] else f"⚠ {c['reason']}"
        lines.append(f"- [{c['n']}] {target} {mark} — “{c['quote']}”")
    return answer + "\n\n**Sources**\n" + "\n".join(lines)  # a list, so markdown keeps one source per line
