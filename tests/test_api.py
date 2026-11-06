import json

import pytest
from fastapi.testclient import TestClient

from src.core.config import settings
from src.main import app
from src.rag import graph_builder, store

RESULT = {"answer": "42 [1]", "rendered": "42 [1]\n\nSources", "citations": [], "tier": "rag", "trace": ["t"], "verified": True}


@pytest.fixture
def client(monkeypatch, tmp_path):
    monkeypatch.setattr(settings, "DATA_DIR", tmp_path)
    monkeypatch.setattr(settings, "MONGO_URL", "")
    return TestClient(app)


def test_query_and_history(client, monkeypatch):
    calls = []
    monkeypatch.setattr(graph_builder, "answer", lambda q, h: calls.append((q, list(h))) or RESULT)

    r = client.post("/rag/query", json={"query": "q1", "session_id": "s-hist"})
    assert r.status_code == 200
    assert r.json() == {**RESULT, "session_id": "s-hist"}

    client.post("/rag/query", json={"query": "q2", "session_id": "s-hist"})
    assert calls[0][1] == []
    assert [(m.type, m.content) for m in calls[1][1]] == [("human", "q1"), ("ai", "42 [1]")]


def test_query_error_is_500(client, monkeypatch):
    def boom(q, h):
        raise RuntimeError("llm down")

    monkeypatch.setattr(graph_builder, "answer", boom)
    r = client.post("/rag/query", json={"query": "q", "session_id": "s-err"})
    assert r.status_code == 500 and "llm down" in r.json()["detail"]


def test_upload_txt(client, monkeypatch, tmp_path):
    seen = {}
    monkeypatch.setattr(store, "add_document", lambda path, description="": seen.update(path=path, d=description) or {"name": "a.txt"})

    r = client.post("/rag/documents/upload", files={"file": ("a.txt", b"hello")}, headers={"X-Description": "my doc"})
    assert r.json() == {"status": True, "document": {"name": "a.txt"}}
    assert seen["path"] == tmp_path / "uploads" / "a.txt" and seen["path"].read_bytes() == b"hello"
    assert seen["d"] == "my doc"


def test_upload_bad_extension(client):
    r = client.post("/rag/documents/upload", files={"file": ("virus.exe", b"x")})
    assert r.status_code == 400


def test_upload_value_error_is_422(client, monkeypatch):
    def empty(path, description=""):
        raise ValueError("no text")

    monkeypatch.setattr(store, "add_document", empty)
    assert client.post("/rag/documents/upload", files={"file": ("a.pdf", b"x")}).status_code == 422


def test_upload_path_traversal_sanitized(client, monkeypatch, tmp_path):
    seen = {}
    monkeypatch.setattr(store, "add_document", lambda path, description="": seen.update(path=path) or {})

    client.post("/rag/documents/upload", files={"file": ("../../evil.txt", b"x")})
    client.post("/rag/documents/upload", files={"file": ("..\\..\\win.md", b"x")})
    assert (tmp_path / "uploads" / "evil.txt").exists() and (tmp_path / "uploads" / "win.md").exists()
    assert seen["path"].parent == tmp_path / "uploads"


def test_list_documents(client, monkeypatch):
    monkeypatch.setattr(store, "list_documents", lambda: [{"doc_id": 1, "name": "a.pdf"}])
    assert client.get("/rag/documents").json() == [{"doc_id": 1, "name": "a.pdf"}]


def test_stream_sends_steps_then_final_and_logs_the_turn(client, monkeypatch):
    def stream_answer(q, h):
        yield "step", {"node": "plan", "route": "documents", "t": 0.5}
        yield "final", {**RESULT, "seconds": 1.0}

    monkeypatch.setattr(graph_builder, "stream_answer", stream_answer)
    r = client.post("/rag/query/stream", json={"query": "q1", "session_id": "s-stream"})
    assert r.status_code == 200 and r.headers["content-type"].startswith("text/event-stream")
    events = [block.split("\n", 1) for block in r.text.strip().split("\n\n")]
    assert [e[0] for e in events] == ["event: step", "event: final"]
    assert json.loads(events[1][1].removeprefix("data: "))["session_id"] == "s-stream"
    logged = json.loads((settings.DATA_DIR / "conversations.jsonl").read_text(encoding="utf-8"))
    assert logged["question"] == "q1" and logged["answer"] == RESULT["answer"]


def test_info(client):
    web = "tavily" if settings.TAVILY_API_KEY else "duckduckgo"
    assert client.get("/rag/info").json() == {"llm": settings.LLM_MODEL, "web": web}
