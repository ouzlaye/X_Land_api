import logging
from datetime import datetime
from uuid import uuid4
from utils.logger import log_transaction

async def xroad_call(service: str, operation: str, payload: dict):
    """Simule un appel X-Road avec journalisation"""
    transaction_id = f"XR-{uuid4().hex[:8]}"
    timestamp = datetime.utcnow().isoformat()
    
    # Logique de routage basique
    response = {
        "transaction_id": transaction_id,
        "service": service,
        "operation": operation,
        "timestamp": timestamp,
        "status": "success",
        "data": {"simulated": True, **payload}
    }
    
    # Journalisation
    await log_transaction({
        "id": transaction_id,
        "timestamp": timestamp,
        "service": service,
        "operation": operation,
        "request": payload,
        "response": response,
        "security": {
            "certificate": "SIMULATED-CERT",
            "signature": "SIMULATED-SIG"
        }
    })
    
    return response