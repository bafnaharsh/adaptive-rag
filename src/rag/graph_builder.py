"""
Research-style adaptive RAG as a LangGraph escalation ladder:
own knowledge -> RAG (dense) -> hybrid (BM25 + dense, RRF, rerank, filter) -> web, then grounded generation with
verified citations.

plan -> END (knowledge) | rag (documents) | web (web)
rag, hybrid: retrieve, then an LLM judge decides sufficient -> generate, else the next tier (hybrid, web)
web -> generate -> verify -> END, or back to generate once with the verification failures as feedback
"""

import itertools
import json
import re
import time
from concurrent.futures import ThreadPoolExecutor

from langchain_core.messages import BaseMessage
from langgraph.graph import END, START, StateGraph

from src.config.settings import Config
from src.core.logger import logger
from src.llms import llm
from src.models.evidence import Chunk
from src.models.state import State
from src.rag import citations, store, web

PROMPTS = Config()
# Evidence cap across tiers: room for one multi-part question's document passages plus web passages, small enough
# to keep judge/generate prompts fast.
MAX_CHUNKS, MAX_CHARS = 16, 16_000
# Separate budgets per source kind: in a mixed question (specs from the web, a procedure from the manual) web passages
# must not crowd the manual's pages out of the evidence, or the other way round.
BUDGET = {"doc": (MAX_CHUNKS, MAX_CHARS), "web": (8, 8_000)}
MAX_ATTEMPTS = 2  # generate calls: the first answer plus one retry with verification feedback
ROLE = {"human": "User", "ai": "Assistant"}
KNOWLEDGE_NOTE = "*Answered from the model's general knowledge; no documents or web sources were consulted.*\n\n"
NO_EVIDENCE = "I could not find any source that answers this question, so I won't guess."


def _short(text, n: int) -> str:
    text = " ".join(str(text).split())
    return text if len(text) <= n else text[:n] + "…"


def _found(chunks: list[Chunk]) -> str:
    """'6 chunks (iphone_user_guide.pdf p. 12, 45)' for the trace."""
    pages: dict[str, dict] = {}
    for c in chunks:
        pages.setdefault(c.source, {})[c.page] = None  # dict as an ordered set
    where = "; ".join(src + (" p. " + ", ".join(str(p) for p in ps if p) if any(ps) else "") for src, ps in pages.items())
    return f"{len(chunks)} chunks ({where})" if chunks else "0 chunks"


def _evidence(chunks: list[Chunk]) -> str:
    return "\n\n".join(f'<source id="{c.id}" label="{c.label()}">\n{c.text}\n</source>' for c in chunks)


def _merge(new: list[Chunk], old: list[Chunk]) -> list[Chunk]:
    """Deduped by id and capped per source kind (BUDGET). Scores are not comparable across tiers; the later tier
    searched more specifically, so its chunks go first."""
    out: dict[str, Chunk] = {}
    used = {kind: [0, 0] for kind in BUDGET}  # chunks, chars
    for c in [*new, *old]:
        kind = c.id.partition(":")[0]
        count, size = used[kind]
        if c.id in out or count == BUDGET[kind][0] or size >= BUDGET[kind][1]:
            continue
        out[c.id] = c
        used[kind] = [count + 1, size + len(c.text)]
    return list(out.values())


def plan(s: State) -> dict:
    question = s["question"]
    docs = store.list_documents()
    hits = store.dense_search(question, k=3) if docs else []
    d = llm.ask_json(PROMPTS.prompt("plan").format(
        history="\n".join(f"{ROLE.get(m.type, m.type)}: {_short(m.content, 600)}" for m in s["history"][-6:]) or "(none)",
        # shortcut: lists at most 30 documents; summarise or search the catalogue when users index more
        documents="\n".join(f"- {x['name']}: {_short(x['description'] or 'no description', 200)}" for x in docs[:30])
        or "(none)",
        snippets="\n".join(f"- {c.label()}: {_short(c.text, 200)}" for c in hits) or "(none)",
        question=question))
    route = d.get("route")
    if route not in ("knowledge", "documents", "web") or (route == "knowledge" and not d.get("answer")):
        route = "documents"
    standalone = str(d.get("standalone_question") or question)
    trace = [f"Plan: route={route} — {d.get('reasoning', '')}"]
    if standalone != question:
        trace.append(f"Standalone question: {standalone}")
    if route == "documents" and not docs:
        route = "web"
        trace.append("No documents indexed → web")
    out = {"route": route, "standalone": standalone, "trace": trace,
           "step": {"node": "plan", "route": route, "reasoning": str(d.get("reasoning", "")), "standalone": standalone,
                    "summary": str(d.get("summary") or ""),
                    "note": "No documents indexed → web" if route == "web" and d.get("route") == "documents" else None}}
    if route == "knowledge":
        out |= {"tier": "knowledge", "answer": KNOWLEDGE_NOTE + str(d["answer"])}
    return out


def _hits(chunks: list[Chunk]) -> list[dict]:
    """Retrieved chunks as the UI shows them."""
    return [{"id": c.id, "label": c.label(), "source": c.source, "page": c.page, "score": round(c.score, 3),
             "snippet": _short(c.text, 240), "url": c.source if c.id.startswith("web:") else None} for c in chunks]


def _judge(s: State, tier: str, head: str, found: list[Chunk], queries: list[str]) -> dict:
    old = s.get("evidence", [])
    new = len({c.id for c in found} - {c.id for c in old})
    step = {"node": tier, "queries": queries, "chunks": _hits(found), "new": new}
    if not new:  # nothing new: judging the same evidence again is wasted
        return {"tier": tier, "sufficient": False, "trace": [f"{head} → nothing new → escalate"],
                "step": step | {"verdict": "nothing new", "reasoning": "", "missing": "",
                                "next_queries": s.get("doc_queries", []) + s.get("web_queries", [])}}
    evidence = _merge(found, old)
    d = llm.ask_json(PROMPTS.prompt("judge").format(question=s["standalone"], evidence=_evidence(evidence)))
    labels = {c.id: f"[{c.label()}]" for c in evidence}  # the judge names sources by id; people read "file, p. 5"
    d["reasoning"] = re.sub(r"\b(?:doc|web):\w+", lambda m: labels.get(m.group().lower(), m.group()),
                            str(d.get("reasoning", "")), flags=re.I)
    ok = str(d.get("sufficient")).lower() == "true"
    doc_q, web_q = ([q for q in d.get(key) or [] if isinstance(q, str) and q.strip()][:3]
                    for key in ("search_documents", "search_web"))
    verdict = "sufficient" if ok else f"insufficient — {d.get('missing') or 'more evidence needed'}"
    if not ok:
        verdict += f" → next: documents {doc_q}, web {web_q}"
        if tier == "rag" and web_q and not doc_q:
            verdict += " (the documents don't cover the rest: skip the deeper document search)"
    return {"tier": tier, "evidence": evidence, "sufficient": ok, "doc_queries": doc_q, "web_queries": web_q,
            "trace": [f"{head} → judge: {verdict}", f"Reasoning: {d.get('reasoning', '')}"],
            "step": step | {"verdict": "sufficient" if ok else "insufficient", "reasoning": str(d.get("reasoning", "")),
                            "summary": str(d.get("summary") or ""),
                            "look_next": None if ok else ("documents" if doc_q or not web_q else "web"),
                            "missing": "" if ok else str(d.get("missing") or ""), "next_queries": doc_q + web_q}}


def _read_on(found: list[Chunk]) -> list[Chunk]:
    """The best hits are often a section's first page; its steps continue on pages that never repeat the title (the
    iPhone 16 camera removal steps on pp. 124-128 never say "camera"), so each of the top 3 hits is followed by the
    next three chunks of its document."""
    seen, expanded = {c.id for c in found}, []
    for c in found[:3]:
        expanded.append(c)
        for n in store.neighbors(c.id, after=3):
            if n.id not in seen:
                seen.add(n.id)
                expanded.append(n)
    return (expanded + found[3:])[:MAX_CHUNKS]


def rag(s: State) -> dict:
    found = _read_on(store.dense_search(s["standalone"], k=6))
    return _judge(s, "rag", f"Tier 1 · RAG (dense): {_found(found)}", found, [s["standalone"]])


def hybrid(s: State) -> dict:
    queries = [s["standalone"], *s.get("doc_queries", [])]
    found = _read_on(store.hybrid_search(queries, k=MAX_CHUNKS))  # whole budget: answers in tables rank ~9th-10th
    head = f"Tier 2 · Hybrid (BM25+dense, reranked): {len(queries)} queries ({' | '.join(queries)}) → {_found(found)}"
    return _judge(s, "hybrid", head, found, queries)


def web_tier(s: State) -> dict:
    # The judge's top two web queries, searched in parallel: a multi-part question ("MP of the cameras, who makes them,
    # how to replace them") has its missing parts spread over different queries.
    queries = (s.get("web_queries") or s.get("doc_queries") or [s["standalone"]])[:2]

    def search(i_q):
        i, q = i_q
        time.sleep(2 * i)  # free search backends throttle simultaneous queries from one machine: stagger them
        return web.web_search(q, k=5)

    with ThreadPoolExecutor(len(queries)) as pool:
        results = list(pool.map(search, enumerate(queries)))
    found = list({c.id: c for c in itertools.chain(*itertools.zip_longest(*results)) if c}.values())  # interleaved
    return {"tier": "web", "evidence": _merge(found, s.get("evidence", [])),
            "trace": [f"Tier 3 · Web: {' | '.join(f'“{q}”' for q in queries)} → {_found(found)}"],
            "step": {"node": "web", "query": " | ".join(queries), "chunks": _hits(found)}}


def generate(s: State) -> dict:
    evidence, attempts, feedback = s.get("evidence", []), s.get("attempts", 0) + 1, s.get("feedback")
    step = {"node": "generate", "attempt": attempts, "retry": bool(feedback)}
    if not evidence:
        return {"answer": NO_EVIDENCE, "citations": [], "attempts": attempts, "trace": ["Generate: no evidence"],
                "step": step | {"citations": 0}}
    prompt = PROMPTS.prompt("generate").format(question=s["standalone"], evidence=_evidence(evidence))
    if feedback:
        previous = {"answer": s["answer"],
                    "citations": [{k: c[k] for k in ("n", "source_id", "quote")} for c in s["citations"]]}
        prompt += "\n\n" + PROMPTS.prompt("regenerate").format(
            problems=feedback, previous=json.dumps(previous, ensure_ascii=False))
    d = llm.ask_json(prompt)
    cits = [{"n": int(c.get("n") or 0), "source_id": str(c.get("source_id") or ""), "quote": str(c.get("quote") or "")}
            for c in d.get("citations") or [] if isinstance(c, dict)]
    return {"answer": str(d.get("answer") or ""), "citations": cits, "attempts": attempts,
            "trace": [f"Generate{' (retry with verification feedback)' if feedback else ''}: {len(cits)} citations"],
            "step": step | {"citations": len(cits)}}


def verify(s: State) -> dict:
    cits = citations.verify(s["citations"], {c.id: c for c in s.get("evidence", [])})
    markers = {int(n) for group in re.findall(r"\[([\d,\s]+)\]", s["answer"]) for n in re.findall(r"\d+", group)}
    numbers = {c["n"] for c in cits}
    dangling = sorted(markers - numbers)
    problems = [f"[{c['n']}] ({c['source_id']}) {c['reason']}" for c in cits if not c["verified"]]
    problems += [f"[{n}] is in the answer but has no citation" for n in dangling]
    problems += [f"citation {n} is never marked in the answer" for n in sorted(numbers - markers)]
    ok = sum(c["verified"] for c in cits)
    line = f"Verify: {ok}/{len(cits)} citations verified"
    retry = bool(problems) and s["attempts"] < MAX_ATTEMPTS
    step = {"node": "verify", "verified": ok, "total": len(cits), "problems": problems, "retry": retry}
    if retry:
        return {"citations": cits, "feedback": "\n".join(problems),
                "trace": [f"{line} — {'; '.join(problems)} → regenerate"], "step": step}
    # unverified citations stay in the result, flagged, rather than hidden
    return {"citations": cits, "feedback": "", "verified": bool(cits) and ok == len(cits) and not dangling,
            "trace": [line + (f" — flagged: {'; '.join(problems)}" if problems else "")], "step": step}


graph = StateGraph(State)
for name, node in [("plan", plan), ("rag", rag), ("hybrid", hybrid), ("web", web_tier), ("generate", generate),
                   ("verify", verify)]:
    graph.add_node(name, node)
graph.add_edge(START, "plan")
graph.add_conditional_edges("plan", lambda s: s["route"], {"knowledge": END, "documents": "rag", "web": "web"})
# After Tier 1 a deeper document search (Tier 2) runs only when some missing part is likely in the documents; when
# the judge says the rest is only on the web, Tier 2 would just cost time.
graph.add_conditional_edges(
    "rag", lambda s: "sufficient" if s["sufficient"] else
    "web" if s.get("web_queries") and not s.get("doc_queries") else "documents",
    {"sufficient": "generate", "documents": "hybrid", "web": "web"})
graph.add_conditional_edges("hybrid", lambda s: "sufficient" if s["sufficient"] else "insufficient",
                            {"sufficient": "generate", "insufficient": "web"})
graph.add_edge("web", "generate")  # the last tier: no judge, generate says what the evidence does not cover
graph.add_edge("generate", "verify")
graph.add_conditional_edges("verify", lambda s: "retry" if s.get("feedback") else "done",
                            {"retry": "generate", "done": END})
builder = graph.compile()


def answer(question: str, history: list[BaseMessage] | None = None) -> dict:
    """Run the ladder for one user turn (history = earlier turns, for follow-up questions). Returns:
    {"answer": str,          # markdown with [n] citation markers
     "rendered": str,        # citations.render(answer, citations): answer + Sources list
     "citations": list[dict],# citations.verify() output
     "tier": "knowledge" | "rag" | "hybrid" | "web",
     "trace": list[str],     # the step-by-step reasoning shown to the user
     "verified": bool}       # True when there is at least one citation and every citation verified
    """
    for kind, data in stream_answer(question, history):
        if kind == "final":
            return data


def stream_answer(question: str, history: list[BaseMessage] | None = None):
    """answer() as a stream for the UI: yields ("step", node's step dict + "t" seconds) as each node finishes, then
    ("final", the answer() dict + "seconds"). Never raises: a failure becomes an error answer."""
    start = time.monotonic()
    state = {"question": question, "history": list(history or []), "trace": []}
    try:
        for mode, chunk in builder.stream(state, stream_mode=["updates", "values"]):
            if mode == "values":
                state = chunk  # the last one is the final state; on failure its trace shows how far the ladder got
                continue
            for update in chunk.values():
                if update and update.get("step"):
                    yield "step", update["step"] | {"t": round(time.monotonic() - start, 1)}
    except Exception as e:  # LLMError, unparseable JSON, a failing store or web call: an error answer, never a crash
        logger.exception("answer failed")
        error = f"{type(e).__name__}: {_short(e, 300)}"
        msg = f"Sorry, I could not answer this question ({error})."
        yield "final", {"answer": msg, "rendered": msg, "citations": [], "tier": state.get("tier", "knowledge"),
                        "trace": state.get("trace", []) + [f"Error: {error}"], "verified": False,
                        "seconds": round(time.monotonic() - start, 1)}
        return
    cits = state.get("citations", [])
    logger.info("answer: tier=%s citations=%d verified=%s", state["tier"], len(cits), state.get("verified", False))
    yield "final", {"answer": state["answer"], "rendered": citations.render(state["answer"], cits), "citations": cits,
                    "tier": state["tier"], "trace": state["trace"], "verified": state.get("verified", False),
                    "seconds": round(time.monotonic() - start, 1)}
