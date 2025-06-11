from fastapi import APIRouter, HTTPException
from database.models import DemandeResponse
from services.mairie_service import charger_demandes

router = APIRouter(prefix="/api", tags=["Demande"])

@router.get("/citizenRequest/{id}", response_model=DemandeResponse)
def get_demande_par_id(id: str):
    demandes = charger_demandes()
    demande = next((d for d in demandes if d["id"] == id), None)
    if not demande:
        raise HTTPException(status_code=404, detail="Demande introuvable.")
    return demande
