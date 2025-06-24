import json, os
from typing import Any
from services.supabase_sync import uploader_fichier
from datetime import datetime
import tempfile
import shutil
DATA_PATH = "database"  # Assure-toi que ce répertoire existe

def lire_fichier(nom_fichier: str) -> Any:
    chemin = os.path.join(DATA_PATH, nom_fichier)
    if not os.path.exists(chemin):
        return []
    with open(chemin, "r", encoding="utf-8") as f:
        return json.load(f)

def convertisseur(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f"Type non pris en charge : {type(obj)}")

def ecrire_fichier(nom_fichier: str, contenu):
    chemin_final = os.path.join("database", nom_fichier)

    with tempfile.NamedTemporaryFile("w", encoding="utf-8", delete=False) as tmp:
        json.dump(contenu, tmp, ensure_ascii=False, indent=2, default=convertisseur)  # convertisseur gère datetime
        tmp_path = tmp.name

    shutil.move(tmp_path, chemin_final)
    uploader_fichier(nom_fichier)