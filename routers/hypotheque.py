from fastapi import APIRouter, HTTPException
from schema.hypotheque_schema import DossierHypothecaireCreate, DossierHypothecaire
from services.hypotheque_service import creer_dossier_hypotheque, charger_dossiers
from pathlib import Path
import json
from typing import List

router = APIRouter()

@router.post("/hypotheques", response_model=DossierHypothecaire, summary="Déposer un nouveau dossier hypothécaire")
def creer_dossier(payload: DossierHypothecaireCreate):
    """
    Permet à une banque ou un notaire de déposer un dossier de garantie hypothécaire.
    Vérifie que le titre foncier existe dans la conservation.
    """
    try:
        dossier = creer_dossier_hypotheque(payload)
        return dossier
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/hypotheques", summary="Lister tous les dossiers hypothécaires")
def lister_dossiers():
    """
    Retourne tous les dossiers hypothécaires enregistrés dans le système.
    """
    return charger_dossiers()



@router.get("/hypotheques/{id}/notifications", summary="Voir les alertes envoyées pour un dossier hypothécaire")
def consulter_notifications(id: str):
    """
    Retourne l’historique des alertes reçues pour une demande hypothécaire.
    Simule les événements de modification du titre foncier.
    """
    notifications_path = Path(__file__).resolve().parent.parent / "database" / "hypotheque_notifications.json"

    if not notifications_path.exists():
        return {"message": "Aucune alerte enregistrée"}

    with open(notifications_path, "r", encoding="utf-8") as f:
        notifications = json.load(f)

    alertes_dossier = [notif for notif in notifications if notif["dossierId"] == id]

    if not alertes_dossier:
        raise HTTPException(status_code=404, detail="Aucune alerte trouvée pour ce dossier")

    return alertes_dossier

