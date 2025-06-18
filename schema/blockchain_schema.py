from pydantic import BaseModel
from datetime import datetime

class BlockchainTransaction(BaseModel):
    id: str
    numeroTitre: str
    typeTransaction: str  # ex: "VENTE", "HYPOTHEQUE", "MUTATION"
    dateTransaction: datetime
    hashTransaction: str  # SHA256
