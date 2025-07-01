from fastapi import APIRouter
from services.demande_service import get_all_demandes
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any
from services.demande_service import mettre_a_jour_demande, lire_fichier, ecrire_fichier
from datetime import datetime

router = APIRouter()

@router.get("/all_request", summary="Lister toutes les demandes citoyennes")
def lister_toutes_les_demandes():
    """
    Retourne toutes les demandes enregistrées dans le système.
    Le filtrage par statut ou acteur se fait côté frontend.
    """
    return get_all_demandes()


