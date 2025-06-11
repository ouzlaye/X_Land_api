from fastapi import APIRouter, HTTPException
from database.models import TitleVerificationRequest, LandRecordResponse
from services.conservation_service import rechercher_dossier_foncier
from utils.logger import log_xroad_transaction
router = APIRouter(
    prefix="/api/landRegistry",
    tags=["Conservation Foncière"]
)

@router.post("/lookup", response_model=LandRecordResponse)
def verifier_titre_ou_nicad(req: TitleVerificationRequest):
    result = rechercher_dossier_foncier(nicad=req.nicad, title_number=req.titleNumber)

    if not result:
        raise HTTPException(status_code=404, detail="Aucun enregistrement foncier trouvé.")
    # Log the transaction
    log_xroad_transaction(
    caller="Notaire",  #  selon qui utilise l’interface
    target_service="Conservation Foncière",
    action="lookup title",
    payload=req.dict(),
    result="OK"
)
    return result
