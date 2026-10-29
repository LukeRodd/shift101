"""Optional AWS Bedrock RAG mentor using in-memory vector retrieval.

The model never receives evaluation answer keys. Bedrock is disabled by default.
"""
import json
import os
from functools import lru_cache
from .mission import MISSION, RUNBOOKS
from .ai_mentor import MentorUnavailable, SYSTEM_PROMPT, cosine

CHAT_MODEL = "amazon.nova-micro-v1:0"
EMBED_MODEL = "amazon.titan-embed-text-v2:0"

def _runtime():
    import boto3
    from botocore.config import Config
    return boto3.client(
        "bedrock-runtime",
        region_name=os.getenv("AWS_REGION", "us-east-1"),
        config=Config(connect_timeout=3, read_timeout=18, retries={"max_attempts": 1}),
    )

def _embedding(client, value: str) -> tuple[float, ...]:
    response = client.invoke_model(
        modelId=EMBED_MODEL,
        contentType="application/json",
        accept="application/json",
        body=json.dumps({"inputText": value, "dimensions": 256, "normalize": True}),
    )
    data = json.loads(response["body"].read())
    vector = data.get("embedding")
    if not isinstance(vector, list) or len(vector) != 256:
        raise MentorUnavailable("Resposta inválida do modelo de embeddings.")
    return tuple(float(number) for number in vector)

@lru_cache(maxsize=1)
def _document_vectors() -> tuple[tuple[float, ...], ...]:
    client = _runtime()
    return tuple(_embedding(client, doc["title"] + ": " + doc["text"]) for doc in RUNBOOKS)

def retrieve(question: str, client) -> list[dict]:
    vector = _embedding(client, question)
    documents = _document_vectors()
    results = sorted(
        [(cosine(vector, doc_vector), item) for doc_vector, item in zip(documents, RUNBOOKS)],
        key=lambda item: item[0],
        reverse=True,
    )
    return [
        {"id": item["id"], "title": item["title"], "text": item["text"]}
        for score, item in results[:2] if score >= 0.35
    ]

def ask(question: str, action_ids: list[str] | None = None) -> dict:
    if os.getenv("SHIFT101_AI_ENABLED", "false").strip().lower() != "true":
        raise MentorUnavailable("Bedrock não habilitado.")
    completed = set(action_ids or [])
    inspected = [action["result"] for action in MISSION["actions"] if action["id"] in completed]
    try:
        client = _runtime()
        sources = retrieve(question, client)
        if not sources:
            return {"mode": "rag-bedrock", "found": False, "message": "Não encontrei evidências suficientes nos runbooks.", "sources": []}
        excerpts = "\n".join("[{}] {}: {}".format(item["id"], item["title"], item["text"]) for item in sources)
        prompt = (
            "MISSÃO FICTÍCIA: " + MISSION["title"]
            + "\nEVIDÊNCIAS INSPECIONADAS: " + ("; ".join(inspected) if inspected else "Nenhuma")
            + "\nFONTES:\n" + excerpts
            + "\nPERGUNTA DO ALUNO: " + question
            + "\nOriente com pistas, sem revelar o gabarito."
        )
        response = client.converse(
            modelId=CHAT_MODEL,
            system=[{"text": SYSTEM_PROMPT}],
            messages=[{"role": "user", "content": [{"text": prompt}]}],
            inferenceConfig={"maxTokens": 240, "temperature": 0.2},
        )
        parts = response["output"]["message"]["content"]
        message = " ".join(part["text"] for part in parts if "text" in part).strip()
        if not message:
            raise MentorUnavailable("O modelo não retornou conteúdo.")
    except MentorUnavailable:
        raise
    except Exception as exc:
        raise MentorUnavailable("O serviço de IA está temporariamente indisponível.") from exc
    return {
        "mode": "rag-bedrock",
        "found": True,
        "message": message[:1400],
        "sources": [{"id": doc["id"], "title": doc["title"]} for doc in sources],
        "disclaimer": "IA experimental. Verifique runbooks; sem acesso ao gabarito.",
    }
