from services.mairie_service import charger_demandes_existantes

def get_all_demandes() -> list[dict]:
    """
    Retourne la liste complète des demandes existantes.
    """
    return charger_demandes_existantes()
