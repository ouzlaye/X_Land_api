from fastapi import APIRouter, HTTPException
from services.mairie_service import traiter_instruction_locale, transmettre_dossier_dgid
from services.cadastre_service import simuler_reponse_cadastre
from services.mairie_service import generer_deliberation_simulee
from services.dgid_service import emettre_bail_et_generer_notification
from services.conservation_service import inscrire_bail_au_registre

router = APIRouter()

@router.post("/requests/{id}/traiterInstruction")
def traiter_instruction(id: str):
    if not traiter_instruction_locale(id):
        raise HTTPException(status_code=404, detail="Demande introuvable ou statut invalide")
    return {"message": "Instruction locale validée → En attente NICAD"}

@router.post("/requests/{id}/simulerCadastre")
def simuler_cadastre(id: str):
    if not simuler_reponse_cadastre(id):
        raise HTTPException(status_code=404, detail="Demande invalide ou déjà traitée")
    return {"message": "Réponse du cadastre simulée (NICAD attribué ou refusé)"}

@router.post("/requests/{id}/genererDeliberation")
def generer_deliberation(id: str):
    if not generer_deliberation_simulee(id):
        raise HTTPException(status_code=400, detail="Impossible de générer la délibération")
    return {"message": "Délibération générée et ajoutée au dossier"}

@router.post("/requests/{id}/transmettreDGID")
def transmettre_dgid(id: str):
    if not transmettre_dossier_dgid(id):
        raise HTTPException(status_code=400, detail="Dossier incomplet ou erreur lors de la transmission")
    return {"message": "Dossier transmis à la DGID"}

@router.post("/requests/{id}/emettreBail")
def emettre_bail(id: str):
    if not emettre_bail_et_generer_notification(id):
        raise HTTPException(status_code=400, detail="Échec lors de l’émission du bail")
    return {"message": "Bail émis avec notification jointe"}

@router.post("/requests/{id}/inscrireBail", summary="Inscription et certification foncière via blockchain")
def inscrire_bail(id: str):
    """
    Inscrit un bail dans le registre foncier et certifie immédiatement la transaction via blockchain.
    Retourne le numéro de titre foncier et son hash blockchain.
    """
    result = inscrire_bail_au_registre(id)
    if not result["numeroTitre"]:
        raise HTTPException(status_code=400, detail=result["message"])

    return result
