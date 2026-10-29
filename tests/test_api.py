from fastapi.testclient import TestClient
from backend.shift101.main import app
client = TestClient(app)

def test_health():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_mission_contains_five_questions_and_no_answer_key():
    result = client.get("/api/mission")
    assert result.status_code == 200
    assert len(result.json()["questions"]) == 5
    assert "correct" not in str(result.json())

def test_action_is_synthetic():
    assert client.get("/api/action/ping").json()["synthetic"] is True
    assert client.get("/api/action/invalid").status_code == 404

def test_mentor_is_lexical_baseline():
    result = client.post("/api/mentor", json={"question": "Por que aparece HTTP 502?"})
    assert result.status_code == 200
    assert result.json()["mode"] == "lexical-baseline"
    assert result.json()["sources"]

def test_quiz_score_and_review():
    answers = {"q1": 1, "q2": 2, "q3": 0, "q4": 1, "q5": 2}
    result = client.post("/api/evaluate", json={"answers": answers})
    assert result.status_code == 200
    assert result.json()["score"] == 5
    assert result.json()["passed"] is True
    assert len(result.json()["review"]) == 5

def test_invalid_quiz_answers():
    assert client.post("/api/evaluate", json={"answers": {"q1": 1}}).status_code == 422
    assert client.post("/api/evaluate", json={"answers": {"q1": 10, "q2": 2, "q3": 0, "q4": 1, "q5": 2}}).status_code == 422
    assert client.post("/api/mentor", json={"question": "x" * 501}).status_code == 422

def test_index_served():
    response = client.get("/")
    assert response.status_code == 200
    assert "SHIFT" in response.text
