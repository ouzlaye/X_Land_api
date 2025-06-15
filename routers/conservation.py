from fastapi import APIRouter, HTTPException
from schema.conservation_schema import VerifyTitleRequest, TitleFoncierModel
from services.conservation_service import rechercher_titre_foncier

router = APIRouter()

@router.post("/verifyTitle", response_model=dict, summary="Vérifie un titre foncier par NICAD ou numéro")
def verify_title(payload: VerifyTitleRequest):
    """
    Recherche un titre foncier dans le registre simulé.
    Accepte en entrée soit un numeroTitre, soit un nicad (16 chiffres).
    """
    titre = rechercher_titre_foncier(numeroTitre=payload.numeroTitre, nicad=payload.nicad)

    if not titre:
        return {
            "status": "not_found",
            "message": "Aucun titre foncier correspondant."
        }

    return {
        "status": "found",
        "data": titre.dict()
    }
