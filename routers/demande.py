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


# mise à jour d'une demande depuis le frontend

class ModificationDemande(BaseModel):
    champ: str
    valeur: Any

@router.patch("/requests/{id}/mettreAJour")
def mettre_a_jour_demande_depuis_front(id: str, modifications: Dict[str, Any]):
    demandes = lire_fichier("citizen_requests.json")
    demande_trouvee = False

    for demande in demandes:
        if demande["id"] == id:
            demande_trouvee = True
            for champ, valeur in modifications.items():
                demande[champ] = valeur

            # Historisation automatique si "statut" est modifié
            if "statut" in modifications:
                demande.setdefault("historiqueStatuts", []).append(
                    (datetime.utcnow().isoformat(), modifications["statut"])
                )
            break

    if not demande_trouvee:
        raise HTTPException(status_code=404, detail="Demande non trouvée")

    ecrire_fichier("citizen_requests.json", demandes)
    return {"message": "Demande mise à jour avec succès", "demande": demande}