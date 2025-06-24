import json
from pathlib import Path
from uuid import uuid4
from datetime import datetime
from typing import List
import base64

from schema.mairie_schema import DemandeFonciereCreate, DemandeFonciere, StatutDemande
from services.fichier_sync import ecrire_fichier

# Chemin vers la base simulée des demandes citoyennes
DATA_PATH = Path(__file__).resolve().parent.parent / "database" / "citizen_requests.json"
DATA_PATH.parent.mkdir(exist_ok=True)

def charger_demandes_existantes() -> List[dict]:
    if not DATA_PATH.exists():
        return []
    try:
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []
# Fonction pour sérialiser les données avant l'enregistrement
def serialiser_donnees(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    return obj
# Fonction pour enregistrer les demandes dans le fichier JSON
def enregistrer_demandes(demandes: List[dict]):
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(demandes, f, ensure_ascii=False, indent=4, default=serialiser_donnees)
        ecrire_fichier("citizen_requests.json", demandes)

# Fonction pour soumettre une nouvelle demande foncière


def soumettre_demande(payload: DemandeFonciereCreate) -> DemandeFonciere:
    demandes = charger_demandes_existantes()

    nouvelle_demande = DemandeFonciere(
        id=str(uuid4()),
        dateSoumission=datetime.utcnow(),
        statut=StatutDemande.demande_soumise,
        historiqueStatuts=[(datetime.utcnow(), StatutDemande.demande_soumise)],
        nomComplet=payload.nomComplet,
        telephone=payload.telephone,
        email=payload.email,
        superficie=payload.superficie,
        nature=payload.nature,
        situation=payload.situation,
        coordonnees=payload.coordonnees,
        documents=payload.documents or [],
        nicadAttribue=None
    )

    demandes.append(nouvelle_demande.dict())
    enregistrer_demandes(demandes)
    return nouvelle_demande

# Mettre à jour le statut d'une demande existante coté maire
def mettre_a_jour_statut(id_demande: str, nouveau_statut: StatutDemande) -> bool:
    """
    Met à jour le statut d'une demande existante identifiée par son ID.
    Enregistre le nouveau statut avec un horodatage dans l'historique.
    Retourne True si succès, False si ID introuvable.
    """
    demandes = charger_demandes_existantes()
    demande_trouvee = False

    for demande in demandes:
        if demande["id"] == id_demande:
            demande["statut"] = nouveau_statut
            historique = demande.get("historiqueStatuts", [])
            historique.append((datetime.utcnow().isoformat(), nouveau_statut))
            demande["historiqueStatuts"] = historique
            demande_trouvee = True
            break

    if demande_trouvee:
        enregistrer_demandes(demandes)
        return True
    return False

# Simule le traitement initial de la demande par la mairie
def traiter_instruction_locale(id_demande: str) -> bool:
    """
    Simule le traitement initial de la demande par la mairie.
    Le statut passe de demande_soumise → instruction_locale → attente_nicad, sans réécrire un statut finalisé.
    """
    demandes = charger_demandes_existantes()
    demande_trouvee = False

    for demande in demandes:
        if demande["id"] == id_demande:
            demande_trouvee = True

            #  Vérifier si le traitement est déjà terminé
            if demande["statut"] == StatutDemande.attente_nicad:
                return False  # 🚨 Ne rien faire si déjà à l'étape finale
            
            # Étape 1 : passer à instruction_locale (uniquement si encore en demande_soumise)
            if demande["statut"] == StatutDemande.demande_soumise:
                demande["statut"] = StatutDemande.instruction_locale
                demande.setdefault("historiqueStatuts", []).append(
                    (datetime.utcnow().isoformat(), StatutDemande.instruction_locale)
                )

            # Étape 2 : Préparer la demande au cadastre (uniquement si encore en instruction_locale)
            if demande["statut"] == StatutDemande.instruction_locale:
                demande["statut"] = StatutDemande.attente_nicad
                demande["historiqueStatuts"].append(
                    (datetime.utcnow().isoformat(), StatutDemande.attente_nicad)
                )
            break

    if demande_trouvee:
        enregistrer_demandes(demandes)
        ecrire_fichier("citizen_requests.json", demandes) 
        return True
    return False



# Simule la génération d'une délibération PDF pour une demande
def generer_deliberation_simulee(id_demande: str) -> bool:
    """
    Simule la génération d'une délibération PDF pour une demande.
    Ajoute un document synthétique dans la liste des pièces jointes.
    Bascule le statut en 'deliberation_validee'.
    """
    demandes = charger_demandes_existantes()
    demande_trouvee = False

    for demande in demandes:
        if demande["id"] == id_demande and demande["statut"] == StatutDemande.nicad_valide:
            demande_trouvee = True

            # Création du document simulé (base64 textuel)
            contenu = f"DÉLIBÉRATION\nDemandeur : {demande['nomComplet']}\nTerrain : {demande['situation']}\nNICAD : {demande['nicadAttribue']}"
            encoded = base64.b64encode(contenu.encode("utf-8")).decode("utf-8")

            deliberation_doc = {
                "nom": f"Deliberation_{id_demande[:8]}.pdf",
                "type": "deliberation",
                "contenu_base64": encoded
            }

            # Ajout du document + maj statut
            demande.setdefault("documents", []).append(deliberation_doc)
            demande["statut"] = StatutDemande.deliberation_validee
            demande.setdefault("historiqueStatuts", []).append(
                (datetime.utcnow().isoformat(), StatutDemande.deliberation_validee)
            )
            break

    if demande_trouvee:
        enregistrer_demandes(demandes)
        ecrire_fichier("citizen_requests.json", demandes) 
        return True
    return False


# Simule l'envoi du dossier à la DGID
def transmettre_dossier_dgid(id_demande: str) -> bool:
    """
    Simule la transmission du dossier foncier à la DGID pour instruction.
    Nécessite un NICAD et une délibération validée.
    """
    demandes = charger_demandes_existantes()
    demande_trouvee = False

    for demande in demandes:
        if demande["id"] == id_demande and demande["statut"] == StatutDemande.deliberation_validee:
            demande_trouvee = True

            documents = demande.get("documents", [])
            types_disponibles = [doc["type"] for doc in documents]

            # Vérification des pièces clés (simulation)
            if not all(t in types_disponibles for t in ["identite", "justificatif_occupation", "deliberation"]):
                return False  # Blocage si le dossier est incomplet

            # Bascule du statut
            demande["statut"] = StatutDemande.dossier_transmis_dgid
            demande.setdefault("historiqueStatuts", []).append(
                (datetime.utcnow().isoformat(), StatutDemande.dossier_transmis_dgid)
            )
            break

    if demande_trouvee:
        enregistrer_demandes(demandes)
        ecrire_fichier("citizen_requests.json", demandes) 
        return True
    return False
