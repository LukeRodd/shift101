"""Tests avoid real network and model downloads."""
from fastapi.testclient import TestClient
from backend.shift101.main import app
from backend.shift101.ai_mentor import cosine, config, MentorUnavailable, retrieve
from backend.shift101.mission import RUNBOOKS
import pytest

client = TestClient(app)

def test_default_ai_is_disabled(monkeypatch):
    monkeypatch.delenv("SHIFT101_AI_ENABLED", raising=False)
    assert client.get("/api/ai/status").json()["enabled"] is False
    assert client.post("/api/ai/mentor", json={"question":"Por que HTTP 502?"}).status_code == 503

def test_ai_rejects_unknown_actions(monkeypatch):
    monkeypatch.setenv("SHIFT101_AI_ENABLED","true")
    response = client.post("/api/ai/mentor", json={"question":"Por que HTTP 502?", "action_ids":["secret"]})
    assert response.status_code == 422

def test_ai_ignores_action_details_from_browser(monkeypatch):
    monkeypatch.setenv("SHIFT101_AI_ENABLED","true")
    from backend.shift101 import main
    monkeypatch.setattr(main, "ask", lambda q, ids: {"question":q, "action_ids":ids})
    response = client.post("/api/ai/mentor", json={"question":"Por que HTTP 502?", "action_ids":["ping"]})
    assert response.status_code == 200
    assert response.json()["action_ids"] == ["ping"]

def test_embedding_similarity():
    assert cosine([1, 0], [1, 0]) == pytest.approx(1)
    assert cosine([1, 0], [0, 1]) == 0

def test_local_host_only(monkeypatch):
    monkeypatch.setenv("SHIFT101_OLLAMA_HOST", "https://remote.example.com")
    with pytest.raises(MentorUnavailable):
        config()

def test_retrieval_mocked(monkeypatch):
    from backend.shift101 import ai_mentor
    monkeypatch.setattr(ai_mentor, "_document_vectors", lambda host, model: tuple((1.0, 0.0) if i == 0 else (0.0, 1.0) for i in range(len(RUNBOOKS))))
    monkeypatch.setattr(ai_mentor, "_embed", lambda *args: [[1.0, 0.0]])
    results = retrieve("ICMP", object(), "http://127.0.0.1:11434", "fake")
    assert results[0]["id"] == RUNBOOKS[0]["id"]
