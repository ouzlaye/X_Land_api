import base64
import random
from datetime import datetime
from services.mairie_service import charger_demandes_existantes, enregistrer_demandes
from schema.mairie_schema import StatutDemande

def emettre_bail_et_generer_notification(id_demande: str) -> bool:
    """
    Simule l'émission d'un bail et la génération d'une notification officielle.
    Ajoute un document de notification + numéro de bail.
    """
    demandes = charger_demandes_existantes()
    demande_trouvee = False

    for demande in demandes:
        if demande["id"] == id_demande and demande["statut"] == StatutDemande.dossier_transmis_dgid:
            demande_trouvee = True

            # Générer un numéro de bail unique
            numero_bail = f"BAIL-2025-{random.randint(1000,9999)}"

            # Construire un contenu textuel de notification réaliste
            contenu = (
                f"DGID – Notification de Bail\n\n"
                f"À : {demande['nomComplet']}\n"
                f"Téléphone : {demande['telephone']}\n"
                f"NICAD : {demande.get('nicadAttribue', '-')}\n"
                f"Superficie : {demande['superficie']}\n"
                f"Objet : Attribution d’un bail administratif sur le terrain situé à {demande['situation']}.\n\n"
                f"Le bail porte le numéro {numero_bail}, valable 30 ans, avec un canon annuel de 10 000 FCFA.\n"
                f"Fait à Dakar, le {datetime.utcnow().date()}"
            )

            base64_doc = base64.b64encode(contenu.encode("utf-8")).decode("utf-8")
            notification_doc = {
                "nom": f"Notification_Bail_{numero_bail}.pdf",
                "type": "deliberation",  # ou "notification_bail" si tu veux enrichir le type
                "contenu_base64": base64_doc
            }

            # Enrichir la demande
            demande.setdefault("documents", []).append(notification_doc)
            demande["numeroBail"] = numero_bail
            demande["duree"] = "30 ans"
            demande["canonAnnuel"] = "10 000 FCFA/an"
            demande["statut"] = StatutDemande.bail_emis
            demande.setdefault("historiqueStatuts", []).append(
                (datetime.utcnow().isoformat(), StatutDemande.bail_emis)
            )
            break

    if demande_trouvee:
        enregistrer_demandes(demandes)
        return True
    return False
