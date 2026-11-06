"""
Agent mode: instead of the fixed ladder, the model gets the pipeline's pieces as tools (quick or deep document search,
web search) and decides each round what to call; the calls of one round run in parallel. It answers with verbatim
quotes that go through the same deterministic citation check as the ladder (one retry with the failures as feedback).

Same events and result shape as graph_builder.stream_answer, so the API, UI and eval treat both modes alike.
"""

import time
from concurrent.futures import ThreadPoolExecutor

from langchain_core.messages import BaseMessage

from src.core.logger import logger
from src.llms import llm
from src.models.evidence import Chunk
from src.rag import citations, store, web
from src.rag.graph_builder import (KNOWLEDGE_NOTE, MAX_CHUNKS, NO_EVIDENCE, PROMPTS, ROLE, _board_text, _evidence,
                                   _found, _hits, _merge, _new_board, _read_on, _short, _update_board, generate, verify)

MAX_ROUNDS = 2  # search rounds (each runs its tool calls in parallel); a third took a multi-part question to ~100 s


def _run_tool(job: tuple[dict, float]) -> tuple[dict, list[Chunk]]:
    call, delay = job
    time.sleep(delay)  # free search backends throttle simultaneous web queries from one machine: stagger them
    query, part = str(call.get("query") or "").strip(), (str(call["part"]) if call.get("part") else None)
    if call.get("tool") == "search_web":
        return {"tool": "search_web", "query": query, "depth": None, "part": part}, web.web_search(query, k=5)
    depth = "deep" if call.get("depth") == "deep" else "quick"
    found = store.hybrid_search([query], k=MAX_CHUNKS) if depth == "deep" else store.dense_search(query, k=6)
    return {"tool": "search_documents", "query": query, "depth": depth, "part": part}, _read_on(found)


def _tier(used: set[str]) -> str:
    """The deepest source the agent used, in the ladder's terms, so the UI badge and the eval read both modes alike."""
    return next((tier for key, tier in (("web", "web"), ("deep", "hybrid"), ("quick", "rag")) if key in used),
                "knowledge")


def stream_agent(question: str, history: list[BaseMessage] | None = None):
    """Yields ("step", {...}) per think / tool / generate / verify, then ("final", result). Never raises."""
    start = time.monotonic()
    elapsed = lambda: round(time.monotonic() - start, 1)  # noqa: E731
    docs, history = store.list_documents(), list(history or [])
    evidence: list[Chunk] = []
    board: list[dict] = []
    log, trace, used = [], [], set()
    feedback, attempts, answer, cits, verified, search_rounds = "", 0, "", [], False, 0

    def final(tier: str) -> tuple[str, dict]:
        logger.info("agent answer: tier=%s citations=%d verified=%s", tier, len(cits), verified)
        return "final", {"answer": answer, "rendered": citations.render(answer, cits), "citations": cits,
                         "tier": tier, "trace": trace, "verified": verified, "seconds": elapsed(), "mode": "agent",
                         "parts": board}

    try:
        for rnd in range(1, MAX_ROUNDS + 3):  # search rounds + an answer round + one retry round
            searches_left = MAX_ROUNDS - search_rounds
            d = llm.ask_json(PROMPTS.prompt("agent").format(
                history="\n".join(f"{ROLE.get(m.type, m.type)}: {_short(m.content, 600)}" for m in history[-6:])
                or "(none)",
                documents="\n".join(f"- {x['name']}: {_short(x['description'] or 'no description', 200)}"
                                    for x in docs[:30]) or "(none)",
                question=question, parts=_board_text(board), log="\n".join(log) or "(none yet)",
                evidence=_evidence(evidence) or "(none yet)",
                feedback=f"\nYour previous answer failed citation checking:\n{feedback}\nFix it: copy quotes exactly "
                         f"from the evidence, cite other passages, or drop the claim.\n" if feedback else "",
                rounds_left=searches_left))
            thought = str(d.get("thought") or "")
            knowledge = bool(d.get("knowledge_answer")) and not evidence
            board = _update_board(board or _new_board(d.get("parts"), question), d.get("parts"), evidence)
            if knowledge:
                board = [p | {"status": "found", "note": "From general knowledge"} for p in board]
            yield "step", {"node": "think", "round": rnd, "summary": thought, "parts": board, "t": elapsed()}
            trace.append(f"Round {rnd} · think: {thought}")

            if knowledge:
                answer = KNOWLEDGE_NOTE + str(d["knowledge_answer"])
                yield final("knowledge")
                return

            actions = [a for a in d.get("actions") or [] if isinstance(a, dict) and str(a.get("query") or "").strip()]
            if actions and searches_left and not d.get("answer"):
                search_rounds += 1
                webs = 0
                jobs = []
                for a in actions[:3]:
                    jobs.append((a, 2.0 * webs if a.get("tool") == "search_web" else 0.0))
                    webs += a.get("tool") == "search_web"
                with ThreadPoolExecutor(len(jobs)) as pool:
                    results = list(pool.map(_run_tool, jobs))
                for info, found in results:
                    used.add("web" if info["tool"] == "search_web" else info["depth"])
                    evidence = _merge(found, evidence)
                    line = f"Round {rnd} · {info['tool']}({info['depth'] or 'web'}) “{info['query']}” → {_found(found)}"
                    log.append(line)
                    trace.append(line)
                    yield "step", {"node": "tool", "round": rnd, **info, "chunks": _hits(found), "t": elapsed()}
                continue

            if not d.get("answer") and evidence:  # still asking to search with no rounds left: write it ourselves
                d = generate({"evidence": evidence, "standalone": question, "attempts": attempts, "feedback": "",
                              "board": board})
                board = d["board"]
            attempts += 1
            answer = str(d.get("answer") or "") or NO_EVIDENCE
            cits = [{"n": int(c.get("n") or 0), "source_id": str(c.get("source_id") or ""),
                     "quote": str(c.get("quote") or "")} for c in d.get("citations") or [] if isinstance(c, dict)]
            yield "step", {"node": "generate", "attempt": attempts, "citations": len(cits), "retry": bool(feedback),
                           "t": elapsed()}
            trace.append(f"Generate{' (retry with verification feedback)' if feedback else ''}: {len(cits)} citations")
            v = verify({"citations": cits, "evidence": evidence, "answer": answer, "attempts": attempts})
            cits, feedback, verified = v["citations"], v["feedback"], v.get("verified", False)
            trace += v["trace"]
            yield "step", v["step"] | {"t": elapsed()}
            if not feedback:
                yield final(_tier(used))
                return
        yield final(_tier(used))  # out of rounds while retrying: keep the last answer, its citations stay flagged
    except Exception as e:  # LLMError, unparseable JSON, a failing tool: an error answer, never a crash
        logger.exception("agent failed")
        error = f"{type(e).__name__}: {_short(e, 300)}"
        answer, cits, verified = f"Sorry, I could not answer this question ({error}).", [], False
        trace.append(f"Error: {error}")
        yield final(_tier(used))


def answer(question: str, history: list[BaseMessage] | None = None) -> dict:
    for kind, data in stream_agent(question, history):
        if kind == "final":
            return data
