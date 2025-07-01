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
    conservation_data = lire_fichier("conservation_data.json")
    demande_trouvee = False

    for demande in demandes:
        if demande["id"] == id:
            demande_trouvee = True
            for champ, valeur in modifications.items():
                demande[champ] = valeur

            # Historisation du statut
            if "statut" in modifications:
                nouveau_statut = modifications["statut"]
                demande.setdefault("historiqueStatuts", []).append(
                    (datetime.utcnow().isoformat(), nouveau_statut)
                )

            # 🔍 Vérifie si bail_inscrit est présent dans l’historique
            historique = [statut for _, statut in demande.get("historiqueStatuts", [])]
            bail_inscrit_present = "bail_inscrit" in historique

            if bail_inscrit_present:
                numero_bail = demande.get("bail", f"BAIL-{id[-4:].upper()}")

                # Vérifie que le bail n’est pas déjà inscrit
                deja_inscrit = any(t["numeroTitre"] == numero_bail for t in conservation_data)

                if not deja_inscrit:
                    nouveau_titre = {
                        "numeroTitre": numero_bail,
                        "nicad": demande.get("nicadAttribue", "Inconnu"),
                        "designation": demande.get("nature", "Non précisée"),
                        "situation": demande.get("situation", "Inconnue"),
                        "superficie": demande.get("superficie", "Non précisée"),
                        "proprietaireInscrit": demande.get("nomComplet", "Non précisé"),
                        "modeAcquisition": "attribution",
                        "dateInscription": datetime.utcnow().date().isoformat(),
                        "nota": "Aucune remarque",
                        "hypotheque": "Aucune",
                        "coordonnees": demande.get("coordonnees", {}),
                        "canonAnnuel": demande.get("canonAnnuel", "sansn objet")
                    }

                    conservation_data.append(nouveau_titre)
                    ecrire_fichier("conservation_data.json", conservation_data)
                    from services.supabase_sync import uploader_fichier
                    uploader_fichier("conservation_data.json")

            break

    if not demande_trouvee:
        raise HTTPException(status_code=404, detail="Demande non trouvée")

    ecrire_fichier("citizen_requests.json", demandes)
    from services.supabase_sync import uploader_fichier
    uploader_fichier("citizen_requests.json")

    return {"message": "Demande mise à jour avec succès", "demande": demande}

