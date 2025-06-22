from fastapi import APIRouter
from services.demande_service import get_all_demandes

router = APIRouter()

@router.get("/all_request", summary="Lister toutes les demandes citoyennes")
def lister_toutes_les_demandes():
    """
    Retourne toutes les demandes enregistrées dans le système.
    Le filtrage par statut ou acteur se fait côté frontend.
    """
    return get_all_demandes()
