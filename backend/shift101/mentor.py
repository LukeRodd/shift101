"""Lexical lookup baseline: not generative AI or semantic RAG."""
import re
import unicodedata
from .mission import RUNBOOKS
STOPWORDS = {"a", "as", "ao", "como", "com", "de", "do", "da", "e", "em", "o", "os", "para", "por", "que", "um", "uma", "no", "na", "me", "tem", "esta", "esse"}

def terms(value: str) -> set[str]:
    value = unicodedata.normalize("NFKD", value.casefold())
    value = "".join(c for c in value if not unicodedata.combining(c))
    return {w for w in re.findall(r"[a-z0-9]+", value) if len(w) > 2 and w not in STOPWORDS}

def lookup(question: str) -> dict:
    query = terms(question)
    hits = []
    for doc in RUNBOOKS:
        score = len(query & terms(doc["title"] + " " + doc["text"]))
        if score:
            hits.append((score, doc))
    hits.sort(key=lambda item: (-item[0], item[1]["id"]))
    if not hits:
        return {"mode": "lexical-baseline", "found": False, "message": "Não encontrei referência suficiente. Revise o runbook ou solicite apoio ao instrutor.", "sources": []}
    top = hits[0][1]
    return {"mode": "lexical-baseline", "found": True, "message": top["text"], "sources": [{"id": top["id"], "title": top["title"]}]}
