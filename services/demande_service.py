from services.mairie_service import charger_demandes_existantes
from services.fichier_sync import ecrire_fichier, lire_fichier

def get_all_demandes() -> list[dict]:
    """
    Retourne la liste complète des demandes existantes.
    """
    return charger_demandes_existantes()


def mettre_a_jour_demande(demande_id: str, modifications: dict) -> dict:
    demandes = lire_fichier("citizen_requests.json")

    for demande in demandes:
        if demande["id"] == demande_id:
            demande.update(modifications)
            break
    else:
        raise ValueError(f"Aucune demande avec l'ID {demande_id} trouvée.")

    ecrire_fichier("citizen_requests.json", demandes)
    return demande  # version mise à jour