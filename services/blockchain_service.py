import json
import hashlib
from uuid import uuid4
from datetime import datetime
from pathlib import Path
from schema.blockchain_schema import BlockchainTransaction

BLOCKCHAIN_PATH = Path(__file__).resolve().parent.parent / "database" / "blockchain_log.json"

def generer_hash(transaction_data: str) -> str:
    return hashlib.sha256(transaction_data.encode("utf-8")).hexdigest()

def certifier_transaction(numeroTitre: str, typeTransaction: str) -> BlockchainTransaction:
    data = f"{numeroTitre}-{typeTransaction}-{datetime.utcnow().isoformat()}"
    hash_value = generer_hash(data)

    transaction = BlockchainTransaction(
        id=str(uuid4()),
        numeroTitre=numeroTitre,
        typeTransaction=typeTransaction,
        dateTransaction=datetime.utcnow(),  # 💡 Garde datetime pour le modèle Pydantic
        hashTransaction=hash_value
    )

    if BLOCKCHAIN_PATH.exists():
        with open(BLOCKCHAIN_PATH, "r", encoding="utf-8") as f:
            transactions = json.load(f)
    else:
        transactions = []

    # 🔧 Convertir `datetime` avant sauvegarde JSON
    transactions.append(transaction.dict(exclude={"dateTransaction"}))  
    transactions[-1]["dateTransaction"] = transaction.dateTransaction.isoformat()  

    with open(BLOCKCHAIN_PATH, "w", encoding="utf-8") as f:
        json.dump(transactions, f, ensure_ascii=False, indent=4)

    return transaction