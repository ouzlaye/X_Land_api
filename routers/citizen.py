from fastapi import APIRouter
from models.citizen_request import CitizenRequest
from schemas.citizen_request import CitizenRequestCreate
import uuid
from datetime import datetime

router = APIRouter()

@router.post("/citizenRequest", summary="Soumettre une demande citoyenne postgres")
async def soumettre_demande(demande: CitizenRequestCreate):
    req = await CitizenRequest.create(
        id=str(uuid.uuid4()),
        nom_complet=demande.nomComplet,
        telephone=demande.telephone,
        email=demande.email,
        superficie=demande.superficie,
        nature=demande.nature,
        situation=demande.situation,
        donnees_geo=demande.coordonnees.dict(),
        documents=[doc.dict() for doc in demande.documents],
        statut="demande_soumise",
        date_soumission=datetime.utcnow()
    )
    return {
        "id": req.id,
        "statut": req.statut,
        "dateSoumission": req.date_soumission
    }
