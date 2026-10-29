"""Stateless API serving a synthetic educational mission."""
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from .mission import MISSION, ANSWERS, RUNBOOKS
from .mentor import lookup
from .ai_mentor import ask, enabled, MentorUnavailable
ROOT = Path(__file__).resolve().parents[2]
app = FastAPI(title="Shift101 API", version="0.1.0", description="Synthetic educational simulation. No production integrations.")

class MentorRequest(BaseModel):
    question: str = Field(min_length=3, max_length=500)

class AIRequest(BaseModel):
    question: str = Field(min_length=3, max_length=500)
    action_ids: list[str] = Field(default_factory=list, max_length=4)

class QuizRequest(BaseModel):
    answers: dict[str, int] = Field(min_length=5, max_length=5)

@app.get("/api/health")
def health() -> dict:
    return {"status": "ok", "version": "0.1.0"}

@app.get("/api/mission")
def get_mission() -> dict:
    return MISSION

@app.get("/api/runbooks")
def runbooks() -> list:
    return RUNBOOKS

@app.get("/api/action/{action_id}")
def inspect_action(action_id: str) -> dict:
    action = next((a for a in MISSION["actions"] if a["id"] == action_id), None)
    if action is None:
        raise HTTPException(status_code=404, detail="Ação não encontrada")
    return {"action_id": action_id, "result": action["result"], "synthetic": True}

@app.post("/api/mentor")
def mentor(request: MentorRequest) -> dict:
    return lookup(request.question)

@app.get("/api/ai/status")
def ai_status() -> dict:
    return {"enabled": enabled(), "mode": "rag-ollama" if enabled() else "lexical-baseline"}

@app.post("/api/ai/mentor")
def ai_mentor(request: AIRequest) -> dict:
    if not enabled():
        raise HTTPException(status_code=503, detail="Tutor generativo desabilitado; use a busca textual.")
    allowed = {a["id"] for a in MISSION["actions"]}
    if any(action_id not in allowed for action_id in request.action_ids):
        raise HTTPException(status_code=422, detail="Evidência não reconhecida")
    try:
        return ask(request.question, request.action_ids)
    except MentorUnavailable as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc

@app.post("/api/evaluate")
def evaluate(request: QuizRequest) -> dict:
    expected = set(ANSWERS)
    if set(request.answers) != expected:
        raise HTTPException(status_code=422, detail="Responda às cinco questões válidas")
    if any(not isinstance(v, int) or isinstance(v, bool) or v < 0 or v >= 3 for v in request.answers.values()):
        raise HTTPException(status_code=422, detail="Alternativa inválida")
    result = []
    for qid, (correct, explanation) in ANSWERS.items():
        selection = request.answers[qid]
        result.append({"question_id": qid, "selected": selection, "correct": correct, "is_correct": selection == correct, "explanation": explanation})
    score = sum(item["is_correct"] for item in result)
    return {"score": score, "total": len(result), "passed": score >= 4, "review": result}

app.mount("/", StaticFiles(directory=ROOT / "frontend", html=True), name="frontend")
