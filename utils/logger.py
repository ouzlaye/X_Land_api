import json
from datetime import datetime
from pathlib import Path

LOG_PATH = Path("logs/xroad_logs.json")
LOG_PATH.parent.mkdir(parents=True, exist_ok=True)

def log_xroad_transaction(
    caller: str,
    target_service: str,
    action: str,
    payload: dict,
    result: str
):
    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "caller": caller,
        "target_service": target_service,
        "action": action,
        "payload": payload,
        "result": result
    }

    # Charger les logs existants
    logs = []
    if LOG_PATH.exists():
        with open(LOG_PATH, "r", encoding="utf-8") as f:
            try:
                logs = json.load(f)
            except json.JSONDecodeError:
                logs = []

    # Ajouter la nouvelle entrée
    logs.append(log_entry)

    # Sauvegarder
    with open(LOG_PATH, "w", encoding="utf-8") as f:
        json.dump(logs, f, indent=2, ensure_ascii=False)
