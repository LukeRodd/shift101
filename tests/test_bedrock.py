from backend.shift101 import bedrock_mentor
from backend.shift101.ai_mentor import MentorUnavailable
import pytest

def test_bedrock_disabled(monkeypatch):
    monkeypatch.setenv("SHIFT101_AI_ENABLED","false")
    with pytest.raises(MentorUnavailable):
        bedrock_mentor.ask("O que significa 502?")

def test_bedrock_retrieval_mocked(monkeypatch):
    monkeypatch.setattr(bedrock_mentor, "_embedding", lambda client, text: (1.0,0.0))
    monkeypatch.setattr(bedrock_mentor, "_document_vectors", lambda: tuple((1.0,0.0) for _ in bedrock_mentor.RUNBOOKS))
    assert len(bedrock_mentor.retrieve("HTTP", object())) == 2
