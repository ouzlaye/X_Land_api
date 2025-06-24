from supabase import create_client, Client
import os

# Remplace les 2 lignes ci-dessous avec TES identifiants réels
SUPABASE_URL = "https://rzbvphlvhxyvtrpwjuno.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJ6YnZwaGx2aHh5dnRycHdqdW5vIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTA2OTYyODEsImV4cCI6MjA2NjI3MjI4MX0.mdxtBZi7fgqKMhxCHp1s10ySa5P1IplkmrerQR73oeU"

BUCKET = "xland-data"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def uploader_fichier(nom_fichier: str) -> bool:
    chemin = os.path.join("database", nom_fichier)
    if not os.path.exists(chemin):
        print(f"[⚠️] Fichier introuvable : {chemin}")
        return False

    with open(chemin, "rb") as f:
        contenu = f.read()

    try:
        result = supabase.storage.from_(BUCKET).upload(
            nom_fichier,
            contenu,
            {"x-upsert": "true"}
        )
        if hasattr(result, 'status_code') and result.status_code in [200, 201]:
            print(f"[✅] {nom_fichier} sauvegardé dans Supabase")
            return True
        else:
            print(f"[❌] Upload échoué. Code retour : {getattr(result, 'status_code', 'inconnu')}")
            return False

    except Exception as e:
        print(f"[❌] Exception pendant l'upload : {e}")
        return False



def restaurer_fichier(nom_fichier: str) -> bool:
    try:
        reponse = supabase.storage.from_(BUCKET).download(nom_fichier)
        contenu_bytes = reponse
        chemin = os.path.join("database", nom_fichier)
        with open(chemin, "wb") as f:
            f.write(contenu_bytes)
        print(f"[✅] {nom_fichier} restauré localement depuis Supabase")
        return True
    except Exception as e:
        print(f"[❌] Échec restauration {nom_fichier} : {e}")
        return False


