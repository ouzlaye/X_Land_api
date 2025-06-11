from fastapi import APIRouter, HTTPException
from pathlib import Path
import json

router = APIRouter(prefix="/api/logs", tags=["Logs"])

@router.get("/xroad")
def lire_journal_xroad():
    log_path = Path("logs/xroad_logs.json")
    if not log_path.exists():
        raise HTTPException(status_code=404, detail="Aucun log trouvé.")

    try:
        with open(log_path, "r", encoding="utf-8") as f:
            logs = json.load(f)
        return logs
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Erreur de lecture du fichier log.")
  