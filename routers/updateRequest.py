# mise à jour d'une demande depuis le frontend
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
from services.fichier_sync import lire_fichier, ecrire_fichier
from datetime import datetime

router = APIRouter()
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