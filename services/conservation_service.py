import json
from pathlib import Path
from typing import Optional, Dict, Any

DATA_PATH = Path("database/conservation_data.json")

def charger_donnees_conservation() -> list[Dict[str, Any]]:
    if not DATA_PATH.exists():
        return []
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def rechercher_dossier_foncier(nicad: Optional[str] = None, title_number: Optional[str] = None) -> Optional[Dict[str, Any]]:
    enregistrements = charger_donnees_conservation()

    for record in enregistrements:
        if nicad and record.get("nicad") == nicad:
            return record
        if title_number and record.get("numeroTitre") == title_number:
            return record

    return None
