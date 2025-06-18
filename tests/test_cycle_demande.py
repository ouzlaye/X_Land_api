import requests
import time

BASE = "http://localhost:8000/api"

# Étape 1 : Soumission initiale
payload = {
    "nomComplet": "Ndeye Diarra Sall",
    "telephone": "778800999",
    "email": "ndeye@example.sn",
    "superficie": "450 m²",
    "nature": "lot",
    "situation": "Rufisque Est",
    "coordonnees": {
        "A": [2488200.0, 1637600.0],
        "B": [2488205.0, 1637600.0],
        "C": [2488205.0, 1637605.0],
        "D": [2488200.0, 1637605.0]
    },
    "documents": [
        {
            "nom": "CNI_NdeyeSall.pdf",
            "type": "identite",
            "contenu_base64": "Q0lOIGZhaXRl"
        },
        {
            "nom": "Justif_Rufisque.pdf",
            "type": "justificatif_occupation",
            "contenu_base64": "amVzdGlmIGR1IHRlcnJhaW4="
        }
    ]
}

print("▶️ Soumission...")
res = requests.post(f"{BASE}/citizenRequest", json=payload)
demande = res.json()
demande_id = demande["id"]
print("✅ ID :", demande_id)

# Chaîne d'exécution des étapes
def appeler(endpoint, label):
    print(f"📌 {label}...")
    r = requests.post(f"{BASE}/requests/{demande_id}/{endpoint}")
    print("✔️", r.json()["message"])
    time.sleep(1)

# Étapes successives
appeler("traiterInstruction", "Instruction mairie")
appeler("simulerCadastre", "Réponse cadastre")
appeler("genererDeliberation", "Délibération")
appeler("transmettreDGID", "Transmission DGID")
appeler("emettreBail", "Émission du bail")
appeler("inscrireBail", "Inscription foncière")

# Final : Affichage du statut complet
print("📄 Statut final :")
statut = requests.get(f"{BASE}/citizenRequest/{demande_id}").json()
print("🔎", statut["statut"])
