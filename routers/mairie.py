from fastapi import APIRouter, Path
from database.models import NouvelleDemandeRequest, DemandeResponse
from services.mairie_service import enregistrer_nouvelle_demande, mettre_a_jour_statut_demande, charger_demandes, valider_deliberation_par_mairie, mettre_a_jour_fichier_demandes
from services.cadastre_service import traiter_demande_nicad_par_xroad
from pydantic import BaseModel
from fastapi import HTTPException
from utils.logger import log_xroad_transaction
import json

router = APIRouter(prefix="/api", tags=["Mairie"])

@router.post("/citizenRequest", response_model=DemandeResponse)
def soumettre_demande_citoyenne(req: NouvelleDemandeRequest):
    nouvelle_demande = enregistrer_nouvelle_demande(req)
    return nouvelle_demande
 

class StatutUpdateRequest(BaseModel):
    statut: str  # Exemple : "deliberation_validee"

@router.post("/citizenRequest/{id}/updateStatut", response_model=DemandeResponse)
def modifier_statut_demande(id: str, req: StatutUpdateRequest):
    try:
        updated = mettre_a_jour_statut_demande(id, req.statut)
        return updated
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    


@router.post("/citizenRequest/{id}/demandeNICAD", response_model=DemandeResponse)
def soumettre_demande_de_nicad(id: str):
    demandes = charger_demandes()

    demande = next((d for d in demandes if d["id"] == id), None)
    if demande is None:
        raise HTTPException(status_code=404, detail="Demande introuvable.")

    if demande.get("statut") != "en_attente":
        raise HTTPException(status_code=400, detail="Demande déjà traitée ou invalide.")

    reponse_cadastre = traiter_demande_nicad_par_xroad(demande)

    if not reponse_cadastre["valide"]:
        demande["statut"] = "refuse_par_cadastre"
        demande["motifRefus"] = reponse_cadastre["motif"]
        resultat = "REFUSE"
    else:
        demande["nicad"] = reponse_cadastre["nicad"]
        demande["statut"] = "nicad_valide"
        resultat = reponse_cadastre["nicad"]

    # Logger l'échange X-Road
    log_xroad_transaction(
        caller="Mairie",
        target_service="Cadastre",
        action="Demande NICAD",
        payload={"id": id, "coordonnees": demande["coordonnees"]},
        result=resultat
    )

    # Mise à jour du fichier
    mettre_a_jour_fichier_demandes(demandes)

    return demande



@router.post("/citizenRequest/{id}/validerDeliberation", response_model=DemandeResponse)
def valider_deliberation(id: str):
    """
    Permet à la mairie de valider une délibération
    après attribution du NICAD par le cadastre.
    """
    try:
        updated = valider_deliberation_par_mairie(id)
        return updated
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
