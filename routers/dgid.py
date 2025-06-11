from fastapi import APIRouter, HTTPException
from database.models import DemandeActeRequest, DemandeResponse
from services.mairie_service import charger_demandes, mettre_a_jour_fichier_demandes
from services.dgid_service import traiter_demande_acte_foncier
from utils.logger import log_xroad_transaction

router = APIRouter(prefix="/api", tags=["DGID"])

@router.post("/citizenRequest/{id}/demandeActe", response_model=DemandeResponse)
def generer_acte(id: str, req: DemandeActeRequest):
    """
    Permet au citoyen (via mairie) de demander un acte foncier à la DGID,
    à partir d’une demande déjà validée par délibération.
    """
    demandes = charger_demandes()
    demande = next((d for d in demandes if d["id"] == id), None)

    if not demande:
        raise HTTPException(status_code=404, detail="Demande introuvable.")

    if demande.get("statut") != "deliberation_validee":
        raise HTTPException(status_code=400, detail="Délibération non encore validée.")

    if not demande.get("nicad"):
        raise HTTPException(status_code=400, detail="NICAD manquant.")

    try:
        acte = traiter_demande_acte_foncier(demande, req.typeActe.value)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    # Enregistrer les infos d’acte dans la demande
    demande["acte"] = acte
    demande["titreFoncierCree"] = True
    demande["statut"] = "titre_cree"

    mettre_a_jour_fichier_demandes(demandes)

    # Journalisation X-Road simulée
    log_xroad_transaction(
        caller="Mairie",
        target_service="DGID",
        action=f"Demande d’acte foncier ({req.typeActe.value})",
        payload={"id": id, "nicad": demande["nicad"]},
        result=acte["numero"]
    )

    return demande
