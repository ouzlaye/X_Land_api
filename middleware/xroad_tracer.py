from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
import json
from datetime import datetime
from pathlib import Path

# Chemin vers le fichier de journalisation X-Road simulé
LOG_PATH = Path(__file__).resolve().parent.parent / "logs" / "xroad_logs.jsonl"
LOG_PATH.parent.mkdir(exist_ok=True)

# Fonction pour ajouter un log structuré à un fichier .jsonl
def log_transaction(request: Request, body: dict, response_status: int):
    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "method": request.method,
        "url": str(request.url),
        "client": request.client.host if request.client else "unknown",
        "body": body,
        "status_code": response_status
    }
    with open(LOG_PATH, "a", encoding="utf-8") as log_file:
        log_file.write(json.dumps(log_entry, ensure_ascii=False) + "\n")

# Middleware principal
async def xroad_tracer_middleware(request: Request, call_next):
    try:
        # Cloner et lire le body JSON pour le log
        body_bytes = await request.body()
        body = json.loads(body_bytes.decode("utf-8")) if body_bytes else {}
    except Exception:
        body = {}

    # Appeler la suite de la chaîne middleware
    response = await call_next(request)

    # Log uniquement les routes /api/ (simulation inter-agence)
    if request.url.path.startswith("/api/"):
        log_transaction(request, body, response.status_code)

    return response
