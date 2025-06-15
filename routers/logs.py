from fastapi import APIRouter
from pathlib import Path
from fastapi.responses import JSONResponse
import json

router = APIRouter()

LOG_PATH = Path(__file__).resolve().parent.parent / "logs" / "xroad_logs.jsonl"

@router.get("/xroadLogs", tags=["X-Road Logs"], summary="Liste des requêtes simulées entre services")
def lire_logs_xroad():
    """
    Retourne les logs simulés du middleware X-Road.
    Chaque ligne représente une transaction inter-agence.
    """
    if not LOG_PATH.exists():
        return JSONResponse(content={"logs": []})

    logs = []
    with open(LOG_PATH, "r", encoding="utf-8") as f:
        for line in f:
            try:
                logs.append(json.loads(line.strip()))
            except Exception:
                continue

    return {"logs": logs}
