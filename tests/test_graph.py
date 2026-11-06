"""Offline tests for the escalation ladder: every LLM, store and web call is a scripted fake."""

from types import SimpleNamespace

import pytest
from langchain_core.messages import AIMessage, HumanMessage

from src.llms import llm
from src.llms.llm import LLMError
from src.models.evidence import Chunk
from src.rag import graph_builder, store, web

Q = "How long does the iPhone battery last?"
GUIDE = Chunk("doc:1", "With always-on display off, the iPhone battery lasts up to 20 hours of video playback.",
              "iphone_user_guide.pdf", page=42)
CASE = Chunk("doc:2", "Use only Apple-certified cases so wireless charging stays efficient.", "iphone_user_guide.pdf",
             page=45)
DETAIL = Chunk("doc:3", "Battery life varies by use; streamed video playback lasts up to 16 hours.",
               "iphone_user_guide.pdf", page=112)
NEWS = Chunk("web:ab12", "Apple says the iPhone 17 battery now lasts up to 30 hours of video playback.",
             "https://example.com/iphone17", title="iPhone 17 battery")
DOCS = [{"doc_id": 1, "name": "iphone_user_guide.pdf", "description": "iPhone user guide", "pages": 120, "chunks": 300}]


def plan(route, standalone=Q, answer=""):
    return {"standalone_question": standalone, "reasoning": "test plan", "route": route, "answer": answer}


def judge(sufficient, *queries):
    return {"reasoning": "step by step", "sufficient": sufficient, "missing": "" if sufficient else "the iPhone 17 figure",
            "next_queries": list(queries)}


def gen(source_id, quote, answer="Up to 20 hours of video playback [1]."):
    return {"answer": answer, "citations": [{"n": 1, "source_id": source_id, "quote": quote}]}


GOOD = gen("doc:1", "the iPhone battery lasts up to 20 hours of video playback")
WEB_GOOD = gen("web:ab12", "the iPhone 17 battery now lasts up to 30 hours", "Up to 30 hours [1].")


@pytest.fixture
def env(monkeypatch):
    e = SimpleNamespace(docs=DOCS, hybrid=[DETAIL, GUIDE], replies={"plan": [], "judge": [], "generate": []},
                        prompts=[], calls=[])

    def ask_json(prompt, *args, **kwargs):
        kind = "plan" if "standalone_question" in prompt else "judge" if "next_queries" in prompt else "generate"
        e.prompts.append((kind, prompt))
        reply = e.replies[kind].pop(0)
        if isinstance(reply, Exception):
            raise reply
        return reply

    monkeypatch.setattr(llm, "ask_json", ask_json)
    monkeypatch.setattr(store, "list_documents", lambda: e.docs)
    monkeypatch.setattr(store, "dense_search", lambda q, k=6, doc_ids=None: e.calls.append(("dense", q, k)) or [GUIDE, CASE])
    monkeypatch.setattr(store, "hybrid_search", lambda qs, k=8, doc_ids=None: e.calls.append(("hybrid", qs, k)) or e.hybrid)
    monkeypatch.setattr(store, "get_chunk", lambda chunk_id: None)
    monkeypatch.setattr(web, "web_search", lambda q, k=5: e.calls.append(("web", q, k)) or [NEWS])
    return e


def kinds(e):
    return [kind for kind, _ in e.prompts]


def test_knowledge_route_answers_without_retrieval(env):
    env.replies["plan"] = [plan("knowledge", "What is 2 + 2?", "2 + 2 = 4.")]
    r = graph_builder.answer("What is 2 + 2?")
    assert r["tier"] == "knowledge" and r["citations"] == [] and r["verified"] is False
    assert "general knowledge" in r["answer"] and r["answer"].endswith("2 + 2 = 4.") and r["rendered"] == r["answer"]
    assert env.calls == [("dense", "What is 2 + 2?", 3)]  # only the planner's snippet lookup
    assert kinds(env) == ["plan"]


def test_dense_sufficient_stops_at_rag(env):
    env.replies |= {"plan": [plan("documents")], "judge": [judge(True)], "generate": [GOOD]}
    r = graph_builder.answer(Q)
    assert r["tier"] == "rag" and r["verified"] is True
    assert r["citations"][0]["verified"] and r["citations"][0]["page"] == 42
    assert "- [1] iphone_user_guide.pdf, p. 42 ✓ — “the iPhone battery" in r["rendered"]
    assert env.calls == [("dense", Q, 3), ("dense", Q, 6)]
    assert kinds(env) == ["plan", "judge", "generate"]
    assert r["trace"][0] == "Plan: route=documents — test plan"
    assert r["trace"][1] == ("Tier 1 · RAG (dense): 2 chunks (iphone_user_guide.pdf p. 42, 45) → judge: sufficient")
    assert r["trace"][-1] == "Verify: 1/1 citations verified"


def test_dense_insufficient_escalates_to_hybrid(env):
    env.replies |= {"plan": [plan("documents")], "judge": [judge(False, "iPhone battery hours", "video playback time"),
                                                           judge(True)],
                    "generate": [gen("doc:3", "streamed video playback lasts up to 16 hours")]}
    r = graph_builder.answer(Q)
    assert r["tier"] == "hybrid" and r["verified"] is True
    assert ("hybrid", [Q, "iPhone battery hours", "video playback time"], 12) in env.calls
    assert not any(c[0] == "web" for c in env.calls)
    assert kinds(env) == ["plan", "judge", "judge", "generate"]
    assert any(line.startswith("Tier 2 · Hybrid") and line.endswith("judge: sufficient") for line in r["trace"])
    assert "doc:3" in env.prompts[2][1] and "doc:1" in env.prompts[2][1]  # judge sees merged evidence


def test_hybrid_insufficient_escalates_to_web(env):
    env.replies |= {"plan": [plan("documents")],
                    "judge": [judge(False, "iPhone battery hours"), judge(False, "iPhone 17 battery life hours")],
                    "generate": [WEB_GOOD]}
    r = graph_builder.answer(Q)
    assert r["tier"] == "web" and r["verified"] is True
    assert r["citations"][0]["url"] == "https://example.com/iphone17"
    assert "- [1] [iPhone 17 battery](https://example.com/iphone17) ✓" in r["rendered"]
    assert ("web", "iPhone 17 battery life hours", 5) in env.calls
    assert kinds(env) == ["plan", "judge", "judge", "generate"]  # no judge after the last tier


def test_hybrid_with_nothing_new_escalates_without_judging(env):
    env.hybrid = [GUIDE]
    env.replies |= {"plan": [plan("documents")], "judge": [judge(False, "iPhone 17 battery")], "generate": [WEB_GOOD]}
    r = graph_builder.answer(Q)
    assert r["tier"] == "web" and kinds(env) == ["plan", "judge", "generate"]
    assert ("web", "iPhone 17 battery", 5) in env.calls


def test_plan_route_web_skips_store_search(env):
    env.replies |= {"plan": [plan("web", "iPhone 17 battery life 2026")], "generate": [WEB_GOOD]}
    r = graph_builder.answer("Latest iPhone battery news?")
    assert r["tier"] == "web" and r["verified"] is True
    assert env.calls == [("dense", "Latest iPhone battery news?", 3), ("web", "iPhone 17 battery life 2026", 5)]
    assert kinds(env) == ["plan", "generate"]


def test_no_documents_never_searches_the_store(env):
    env.docs = []
    env.replies |= {"plan": [plan("documents")], "generate": [WEB_GOOD]}
    r = graph_builder.answer(Q)
    assert r["tier"] == "web"
    assert env.calls == [("web", Q, 5)]
    assert "No documents indexed → web" in r["trace"]
    assert "Indexed documents:\n(none)" in env.prompts[0][1]


@pytest.mark.parametrize("bad", [
    gen("doc:1", "the iPhone battery lasts for three whole days"),  # fabricated quote
    gen("doc:1", "the iPhone battery lasts up to 20 hours of video playback", "20 hours [1], fast charging [2]."),
])
def test_failed_verification_regenerates_once_then_flags(env, bad):
    env.replies |= {"plan": [plan("documents")], "judge": [judge(True)], "generate": [bad, bad]}
    r = graph_builder.answer(Q)
    assert kinds(env) == ["plan", "judge", "generate", "generate"]
    assert "failed citation checking" in env.prompts[-1][1]
    assert r["verified"] is False and len(r["citations"]) == 1
    assert any(line.endswith("→ regenerate") for line in r["trace"])
    assert "flagged" in r["trace"][-1]


def test_fabricated_quote_is_kept_flagged(env):
    bad = gen("doc:1", "the iPhone battery lasts for three whole days")
    env.replies |= {"plan": [plan("documents")], "judge": [judge(True)], "generate": [bad, bad]}
    r = graph_builder.answer(Q)
    assert r["citations"][0]["verified"] is False
    assert "⚠ quote not found in the source text" in r["rendered"]


def test_follow_up_uses_history(env):
    history = [HumanMessage("Tell me about the iPhone battery."), AIMessage("It is a lithium-ion battery.")]
    env.replies |= {"plan": [plan("documents", standalone=Q)], "judge": [judge(True)], "generate": [GOOD]}
    r = graph_builder.answer("How long does it last?", history)
    assert "User: Tell me about the iPhone battery.\nAssistant: It is a lithium-ion battery." in env.prompts[0][1]
    assert ("dense", Q, 6) in env.calls
    assert f"Standalone question: {Q}" in r["trace"]
    assert Q in env.prompts[1][1] and Q in env.prompts[2][1]  # judge and generate get the standalone question


@pytest.mark.parametrize("failure", [LLMError("claude session ended"), ValueError("no JSON in reply: sorry")])
def test_llm_failure_returns_error_answer(env, failure):
    env.replies |= {"plan": [plan("documents")], "judge": [failure]}
    r = graph_builder.answer(Q)
    assert str(failure) in r["answer"] and r["rendered"] == r["answer"]
    assert r["citations"] == [] and r["verified"] is False
    assert r["trace"][0].startswith("Plan:") and r["trace"][-1] == f"Error: {type(failure).__name__}: {failure}"


def test_stream_answer_emits_one_step_per_node_then_final(env):
    env.replies |= {"plan": [plan("documents")], "judge": [judge(False, "iPhone battery hours"), judge(True)],
                    "generate": [gen("doc:3", "streamed video playback lasts up to 16 hours")]}
    events = list(graph_builder.stream_answer(Q))
    steps = [d for kind, d in events if kind == "step"]
    assert [s["node"] for s in steps] == ["plan", "rag", "hybrid", "generate", "verify"]
    assert steps[0]["route"] == "documents" and steps[0]["standalone"] == Q
    assert steps[1]["verdict"] == "insufficient" and steps[1]["next_queries"] == ["iPhone battery hours"]
    assert steps[1]["chunks"][0]["label"] == "iphone_user_guide.pdf, p. 42" and steps[1]["chunks"][0]["url"] is None
    assert steps[2]["queries"] == [Q, "iPhone battery hours"] and steps[2]["verdict"] == "sufficient"
    assert steps[4] | {"t": 0} == {"node": "verify", "verified": 1, "total": 1, "problems": [], "retry": False, "t": 0}
    assert all(isinstance(s["t"], float) for s in steps)
    kind, final = events[-1]
    assert kind == "final" and final["tier"] == "hybrid" and final["verified"] is True and "seconds" in final
