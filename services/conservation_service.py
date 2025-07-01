import json
from pathlib import Path
from typing import Optional
from schema.conservation_schema import TitleFoncierModel
from datetime import datetime
from schema.conservation_schema import TitleFoncierModel
from schema.mairie_schema import StatutDemande
from services.mairie_service import charger_demandes_existantes, enregistrer_demandes
from typing import List
from services.blockchain_service import certifier_transaction
from services.fichier_sync import lire_fichier, ecrire_fichier
from datetime import datetime
# Chemin vers la base simulée
DATA_PATH = Path(__file__).resolve().parent.parent / "database" / "conservation_data.json"

def rechercher_titre_foncier(numeroTitre: Optional[str] = None, nicad: Optional[str] = None) -> Optional[TitleFoncierModel]:
    """
    Recherche un titre foncier dans le fichier JSON simulé à partir d'un numeroTitre ou d'un NICAD.
    Retourne un objet TitleFoncierModel si trouvé, sinon None.
    """
    try:
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"Fichier de données non trouvé à l'emplacement : {DATA_PATH}")

    for item in data:
        if numeroTitre and item["numeroTitre"] == numeroTitre:
            return TitleFoncierModel(**item)
        if nicad and item["nicad"] == nicad:
            return TitleFoncierModel(**item)

    return None  # Aucun titre correspondant trouvé




def generer_numero_titre_foncier() -> str:
    import random
    return f"TF-{random.randint(1000, 9999)}"

# Fonction pour ajouter un titre  (pour les tests ou l'initialisation)

def inscrire_bail_au_registre(id_demande: str) -> dict:
    demandes = charger_demandes_existantes()
    conservation_path = Path(__file__).resolve().parent.parent / "database" / "conservation_data.json"

    if conservation_path.exists():
        with open(conservation_path, "r", encoding="utf-8") as f:
            conservation_data = json.load(f)
    else:
        conservation_data = []

    demande_trouvee = False
    titre_certifie = None

    for demande in demandes:
        if demande["id"] == id_demande and demande["statut"] == StatutDemande.bail_emis:
            demande_trouvee = True

            titre = TitleFoncierModel(
                numeroTitre=generer_numero_titre_foncier(),
                nicad=demande["nicadAttribue"],
                designation="Terrain à usage d’habitation",
                situation=demande["situation"],
                superficie=demande["superficie"],
                proprietaireInscrit=demande["nomComplet"],
                modeAcquisition="Bail administratif",
                dateInscription=str(datetime.utcnow().date()),
                nota=f"Bail attribué sous le n° {demande.get('numeroBail', '-')}",
                hypotheque="Aucune",
                coordonnees=demande["coordonnees"]
            )

            conservation_data.append(titre.dict())

            # 🔗 Certification blockchain après inscription
            titre_certifie = certifier_transaction(titre.numeroTitre, "INSCRIPTION_TF")

            # Mise à jour statut côté demande
            demande["statut"] = StatutDemande.bail_inscrit
            demande.setdefault("historiqueStatuts", []).append(
                (datetime.utcnow().isoformat(), StatutDemande.bail_inscrit)
            )
            break

    if demande_trouvee:
        with open(conservation_path, "w", encoding="utf-8") as f:
            json.dump(conservation_data, f, ensure_ascii=False, indent=4)
        enregistrer_demandes(demandes)

        return {
            "message": "Bail inscrit au registre foncier.",
            "numeroTitre": titre.numeroTitre,
            "hashBlockchain": titre_certifie.hashTransaction if titre_certifie else "Erreur certification"
        }

    return {"message": "Erreur lors de l’inscription du bail.", "numeroTitre": None, "hashBlockchain": None}


def charger_titres_fonciers() -> List[dict]:
    if not DATA_PATH.exists():
        return []
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def enregistrer_evenement_conservation(event: dict):
    logs = lire_fichier("conservation_data.json")
    event["horodatage"] = datetime.utcnow().isoformat()
    logs.append(event)
    ecrire_fichier("database/conservation_data.json", logs)