"""
Research-style adaptive RAG as a LangGraph escalation ladder:
own knowledge -> RAG (dense) -> hybrid (BM25 + dense, RRF, rerank, filter) -> web, then grounded generation with
verified citations.

plan -> END (knowledge) | rag (documents) | web (web)
rag, hybrid: retrieve, then an LLM judge decides sufficient -> generate, else the next tier (hybrid, web)
web -> generate -> verify -> END, or back to generate once with the verification failures as feedback
"""

import json
import re

from langchain_core.messages import BaseMessage
from langgraph.graph import END, START, StateGraph

from src.config.settings import Config
from src.core.logger import logger
from src.llms import llm
from src.models.evidence import Chunk
from src.models.state import State
from src.rag import citations, store, web

PROMPTS = Config()
MAX_CHUNKS, MAX_CHARS = 12, 12_000  # evidence cap across tiers, keeps judge/generate prompts small and fast
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
    """Deduped by id and capped. Scores are not comparable across tiers; the later tier searched more specifically,
    so its chunks go first."""
    out: dict[str, Chunk] = {}
    size = 0
    for c in [*new, *old]:
        if len(out) == MAX_CHUNKS or size >= MAX_CHARS:
            break
        if c.id not in out:
            out[c.id] = c
            size += len(c.text)
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
    out = {"route": route, "standalone": standalone, "trace": trace}
    if route == "knowledge":
        out |= {"tier": "knowledge", "answer": KNOWLEDGE_NOTE + str(d["answer"])}
    return out


def _judge(s: State, tier: str, head: str, found: list[Chunk]) -> dict:
    old = s.get("evidence", [])
    if not {c.id for c in found} - {c.id for c in old}:  # nothing new: judging the same evidence again is wasted
        return {"tier": tier, "sufficient": False, "trace": [f"{head} → nothing new → escalate"]}
    evidence = _merge(found, old)
    d = llm.ask_json(PROMPTS.prompt("judge").format(question=s["standalone"], evidence=_evidence(evidence)))
    ok = str(d.get("sufficient")).lower() == "true"
    verdict = "sufficient" if ok else f"insufficient — {d.get('missing') or 'more evidence needed'}"
    queries = [q for q in d.get("next_queries") or [] if isinstance(q, str) and q.strip()][:3]
    return {"tier": tier, "evidence": evidence, "sufficient": ok, "next_queries": queries,
            "trace": [f"{head} → judge: {verdict}", f"Reasoning: {d.get('reasoning', '')}"]}


def rag(s: State) -> dict:
    found = store.dense_search(s["standalone"], k=6)
    return _judge(s, "rag", f"Tier 1 · RAG (dense): {_found(found)}", found)


def hybrid(s: State) -> dict:
    queries = [s["standalone"], *s.get("next_queries", [])]
    found = store.hybrid_search(queries, k=MAX_CHUNKS)  # the whole evidence budget: answers in tables rank ~9th-10th
    head = f"Tier 2 · Hybrid (BM25+dense, reranked): {len(queries)} queries ({' | '.join(queries)}) → {_found(found)}"
    return _judge(s, "hybrid", head, found)


def web_tier(s: State) -> dict:
    query = (s.get("next_queries") or [s["standalone"]])[0]
    found = web.web_search(query, k=5)
    return {"tier": "web", "evidence": _merge(found, s.get("evidence", [])),
            "trace": [f"Tier 3 · Web: “{query}” → {_found(found)}"]}


def generate(s: State) -> dict:
    evidence, attempts, feedback = s.get("evidence", []), s.get("attempts", 0) + 1, s.get("feedback")
    if not evidence:
        return {"answer": NO_EVIDENCE, "citations": [], "attempts": attempts, "trace": ["Generate: no evidence"]}
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
            "trace": [f"Generate{' (retry with verification feedback)' if feedback else ''}: {len(cits)} citations"]}


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
    if problems and s["attempts"] < MAX_ATTEMPTS:
        return {"citations": cits, "feedback": "\n".join(problems),
                "trace": [f"{line} — {'; '.join(problems)} → regenerate"]}
    # unverified citations stay in the result, flagged, rather than hidden
    return {"citations": cits, "feedback": "", "verified": bool(cits) and ok == len(cits) and not dangling,
            "trace": [line + (f" — flagged: {'; '.join(problems)}" if problems else "")]}


graph = StateGraph(State)
for name, node in [("plan", plan), ("rag", rag), ("hybrid", hybrid), ("web", web_tier), ("generate", generate),
                   ("verify", verify)]:
    graph.add_node(name, node)
graph.add_edge(START, "plan")
graph.add_conditional_edges("plan", lambda s: s["route"], {"knowledge": END, "documents": "rag", "web": "web"})
graph.add_conditional_edges("rag", lambda s: "sufficient" if s["sufficient"] else "insufficient",
                            {"sufficient": "generate", "insufficient": "hybrid"})
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
    state = {"question": question, "history": list(history or []), "trace": []}
    try:
        for state in builder.stream(state, stream_mode="values"):
            pass  # keep the last state: on failure its trace shows how far the ladder got
    except Exception as e:  # LLMError, unparseable JSON, a failing store or web call: an error answer, never a crash
        logger.exception("answer failed")
        error = f"{type(e).__name__}: {_short(e, 300)}"
        msg = f"Sorry, I could not answer this question ({error})."
        return {"answer": msg, "rendered": msg, "citations": [], "tier": state.get("tier", "knowledge"),
                "trace": state.get("trace", []) + [f"Error: {error}"], "verified": False}
    cits = state.get("citations", [])
    logger.info("answer: tier=%s citations=%d verified=%s", state["tier"], len(cits), state.get("verified", False))
    return {"answer": state["answer"], "rendered": citations.render(state["answer"], cits), "citations": cits,
            "tier": state["tier"], "trace": state["trace"], "verified": state.get("verified", False)}
