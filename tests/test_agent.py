"""Agent mode: the model picks tools; fully offline (LLM, store and web faked)."""

from types import SimpleNamespace

import pytest

from src.llms import llm
from src.models.evidence import Chunk
from src.rag import agent, store, web

MANUAL = Chunk("doc:7", "Lift the ends of the three flex cables from the connectors, starting with the button flex cable.",
               "iphone_16_repair_manual.pdf", 125)
SPECS = Chunk("web:ab12", "iPhone 16 cameras: 48MP Fusion main camera and 12MP Ultra Wide camera.",
              "https://www.apple.com/iphone-16/specs/", None, "iPhone 16 specs")


@pytest.fixture
def env(monkeypatch):
    e = SimpleNamespace(replies=[], prompts=[], calls=[])

    def ask_json(prompt, *args, **kwargs):
        e.prompts.append(prompt)
        return e.replies.pop(0)

    monkeypatch.setattr(llm, "ask_json", ask_json)
    monkeypatch.setattr(store, "list_documents", lambda: [{"name": "iphone_16_repair_manual.pdf", "description": ""}])
    monkeypatch.setattr(store, "dense_search", lambda q, k=6, doc_ids=None: e.calls.append(("quick", q)) or [MANUAL])
    monkeypatch.setattr(store, "hybrid_search", lambda qs, k=8, doc_ids=None: e.calls.append(("deep", qs)) or [MANUAL])
    monkeypatch.setattr(store, "neighbors", lambda chunk_id, after=2: [])
    monkeypatch.setattr(store, "get_chunk", lambda chunk_id: None)
    monkeypatch.setattr(web, "web_search", lambda q, k=5: e.calls.append(("web", q)) or [SPECS])
    return e


GOOD = {"thought": "I have both parts.", "answer": "48MP main [1]; lift the three flex cables [2].",
        "citations": [{"n": 1, "source_id": "web:ab12", "quote": "48MP Fusion main camera and 12MP Ultra Wide camera"},
                      {"n": 2, "source_id": "doc:7", "quote": "Lift the ends of the three flex cables from the connectors"}]}


def test_knowledge_answer_needs_one_call_and_no_tools(env):
    env.replies = [{"thought": "Well-known fact.", "knowledge_answer": "Apple makes the iPhone."}]
    r = agent.answer("who makes iphone")
    assert r["tier"] == "knowledge" and r["answer"].endswith("Apple makes the iPhone.") and r["mode"] == "agent"
    assert env.calls == [] and len(env.prompts) == 1


def test_parallel_tools_then_verified_answer(env):
    env.replies = [{"thought": "Manual for the steps, web for the specs.",
                    "actions": [{"tool": "search_documents", "query": "camera removal", "depth": "quick"},
                                {"tool": "search_web", "query": "iPhone 16 camera megapixels"}]},
                   GOOD]
    events = list(agent.stream_agent("camera MP and how to replace it"))
    steps = [d for kind, d in events if kind == "step"]
    assert [s["node"] for s in steps] == ["think", "tool", "tool", "think", "generate", "verify"]
    assert {(s["tool"], s["depth"]) for s in steps if s["node"] == "tool"} == {("search_documents", "quick"),
                                                                              ("search_web", None)}
    final = events[-1][1]
    assert final["tier"] == "web" and final["verified"] is True
    assert [c["page"] for c in final["citations"]] == [None, 125]
    assert 'id="doc:7"' in env.prompts[1] and 'id="web:ab12"' in env.prompts[1]  # the answer round sees all evidence


def test_agent_board_and_part_tagged_tools(env):
    env.replies = [{"thought": "Two parts.", "parts": [{"id": "p1", "label": "Camera megapixels", "status": "pending"},
                                                      {"id": "p2", "label": "How to replace it", "status": "pending"}],
                    "actions": [{"tool": "search_web", "query": "iPhone 16 camera megapixels", "part": "p1"},
                                {"tool": "search_documents", "query": "camera removal", "depth": "quick", "part": "p2"}]},
                   GOOD | {"parts": [{"id": "p1", "status": "found", "note": "48MP main", "sources": ["web:ab12"]},
                                     {"id": "p2", "status": "found", "note": "Lift the flex cables", "sources": ["doc:7"]}]}]
    events = list(agent.stream_agent("camera MP and how to replace it"))
    steps = [d for kind, d in events if kind == "step"]
    assert [p["label"] for p in steps[0]["parts"]] == ["Camera megapixels", "How to replace it"]
    assert {s["part"] for s in steps if s["node"] == "tool"} == {"p1", "p2"}
    final = events[-1][1]
    assert [(p["status"], p["sources"][0]["id"]) for p in final["parts"]] == [("found", "web:ab12"), ("found", "doc:7")]


def test_fabricated_quote_gets_one_retry_with_feedback(env):
    bad = GOOD | {"citations": [GOOD["citations"][0], {"n": 2, "source_id": "doc:7", "quote": "unplug the camera gently"}]}
    env.replies = [{"thought": "Search.", "actions": [{"tool": "search_documents", "query": "camera", "depth": "deep"},
                                                      {"tool": "search_web", "query": "camera MP"}]},
                   bad, GOOD]
    r = agent.answer("camera MP and how to replace it")
    assert r["verified"] is True and r["tier"] == "web"
    assert "failed citation checking" in env.prompts[2] and ("deep", ["camera"]) in env.calls


def test_search_rounds_are_bounded(env):
    search = {"thought": "Search more.", "actions": [{"tool": "search_documents", "query": "x", "depth": "quick"}]}
    env.replies = [search] * agent.MAX_ROUNDS + [search, {"thought": "Answer.", "answer": "Nothing found.",
                                                           "citations": []}]
    r = agent.answer("q")
    assert len([c for c in env.calls if c[0] == "quick"]) == agent.MAX_ROUNDS
    assert r["answer"] == "Nothing found."


def test_llm_failure_is_an_error_answer(env):
    env.replies = [ValueError("no JSON in reply")]

    def boom(prompt, *a, **k):
        raise llm.LLMError("claude session ended")

    llm.ask_json = boom  # monkeypatch restores it after the test
    r = agent.answer("q")
    assert "could not answer" in r["answer"] and r["verified"] is False and r["trace"][-1].startswith("Error:")
