import random

def simuler_validation_parcelle(coordonnees: dict) -> bool:
    # Ici, tu peux ajouter une logique de conflit ou de zone interdite
    # Pour le MVP, on accepte 80% des parcelles simulées
    return random.random() < 0.8

def generer_nicad() -> str:
    region = "01"
    departement = "230"
    arrondissement = "114"
    commune = "02"
    section = f"{random.randint(1, 999):03d}"
    parcelle = f"{random.randint(1, 99999):05d}"
    return region + departement + arrondissement + commune + section + parcelle

def traiter_demande_nicad_par_xroad(demande: dict) -> dict:
    if not simuler_validation_parcelle(demande["coordonnees"]):
        return {
            "valide": False,
            "motif": "Parcelle en conflit avec une zone réservée ou existante."
        }

    nicad = generer_nicad()
    return {
        "valide": True,
        "nicad": nicad
    }
