import json
from pathlib import Path
from uuid import uuid4
from datetime import datetime
from typing import List

from schema.hypotheque_schema import DossierHypothecaireCreate, DossierHypothecaire, StatutHypotheque
from schema.conservation_schema import TitleFoncierModel

CONSERVATION_PATH = Path(__file__).resolve().parent.parent / "database" / "conservation_data.json"
HYPOTHEQUES_PATH = Path(__file__).resolve().parent.parent / "database" / "hypotheques_data.json"
HYPOTHEQUES_PATH.parent.mkdir(exist_ok=True)

def titre_existe(numeroTitre: str) -> bool:
    if not CONSERVATION_PATH.exists():
        return False
    with open(CONSERVATION_PATH, "r", encoding="utf-8") as f:
        titres = json.load(f)
        return any(t["numeroTitre"] == numeroTitre for t in titres)

def charger_dossiers() -> List[dict]:
    if not HYPOTHEQUES_PATH.exists():
        return []
    with open(HYPOTHEQUES_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def enregistrer_dossiers(dossiers: List[dict]):
    with open(HYPOTHEQUES_PATH, "w", encoding="utf-8") as f:
        json.dump(dossiers, f, ensure_ascii=False, indent=4, default=str)

def creer_dossier_hypotheque(payload: DossierHypothecaireCreate) -> DossierHypothecaire:
    if not titre_existe(payload.numeroTitre):
        raise ValueError("Titre foncier introuvable")

    dossier = DossierHypothecaire(
        id=str(uuid4()),
        numeroTitre=payload.numeroTitre,
        nomBanque=payload.nomBanque,
        contactBanque=payload.contactBanque,
        montantGaranti=payload.montantGaranti,
        dateDepot=datetime.utcnow(),
        statut=StatutHypotheque.demande_deposee,
        alertesActives=True
    )

    dossiers = charger_dossiers()
    dossiers.append(dossier.dict())
    enregistrer_dossiers(dossiers)

    return dossier



def activer_traceur(numeroTitre: str, banque: str, contact: str, montant: str) -> dict:
    if not titre_existe(numeroTitre):
        raise ValueError("Titre foncier introuvable")

    traceur = {
        "id": str(uuid4()),
        "numeroTitre": numeroTitre,
        "nomBanque": banque,
        "contactBanque": contact,
        "montantGaranti": montant,
        "dateDepot": datetime.utcnow().isoformat(),
        "alertesActives": True
    }

    dossiers = charger_dossiers()
    dossiers.append(traceur)
    enregistrer_dossiers(dossiers)
    return traceur


def activer_traceur(numeroTitre: str, banque: str, contact: str, montant: str) -> dict:
    if not titre_existe(numeroTitre):
        raise ValueError("Titre foncier introuvable")

    traceur = {
        "id": str(uuid4()),
        "numeroTitre": numeroTitre,
        "nomBanque": banque,
        "contactBanque": contact,
        "montantGaranti": montant,
        "dateDepot": datetime.utcnow().isoformat(),
        "alertesActives": True
    }

    dossiers = charger_dossiers()
    dossiers.append(traceur)
    enregistrer_dossiers(dossiers)
    return traceur
