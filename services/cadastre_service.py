import random
from services.mairie_service import charger_demandes_existantes, enregistrer_demandes
from schema.mairie_schema import StatutDemande
from datetime import datetime
from services.fichier_sync import ecrire_fichier

def generer_nicad_valide() -> str:
    """
    Génère un NICAD simulé de 16 chiffres valides.
    Structure : RR (2) D (1) AM (3) CICR (2) SSS (3) PPPPP (5)
    """
    return f"{random.randint(10,99)}{random.randint(0,9)}{random.randint(100,999)}{random.randint(10,99)}{random.randint(100,999)}{random.randint(10000,99999)}"

def simuler_reponse_cadastre(id_demande: str) -> bool:
    """
    Simule la réponse du cadastre à une demande NICAD.
    Le NICAD peut être attribué ou refusé de manière aléatoire.
    """
    demandes = charger_demandes_existantes()
    demande_trouvee = False

    for demande in demandes:
        if demande["id"] == id_demande and demande["statut"] == StatutDemande.attente_nicad:
            demande_trouvee = True

            nicad_ok = random.random() > 0.2  # 80% de chance de succès

            if nicad_ok:
                nicad_simule = generer_nicad_valide()
                demande["nicadAttribue"] = nicad_simule
                nouveau_statut = StatutDemande.nicad_valide
            else:
                nouveau_statut = StatutDemande.nicad_refuse

            demande["statut"] = nouveau_statut
            demande.setdefault("historiqueStatuts", []).append(
                (datetime.utcnow().isoformat(), nouveau_statut)
            )
            break

    if demande_trouvee:
        enregistrer_demandes(demandes)
        ecrire_fichier("citizen_requests.json", demandes)

        return True
    return False
