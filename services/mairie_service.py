import json
from pathlib import Path
from typing import Dict, Any
from uuid import uuid4
from database.models import NouvelleDemandeRequest
from fpdf import FPDF
from datetime import datetime

DATA_PATH = Path("database/citizen_requests.json")
DATA_PATH.parent.mkdir(parents=True, exist_ok=True)

def charger_demandes() -> list[Dict[str, Any]]:
    if not DATA_PATH.exists():
        return []
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def enregistrer_nouvelle_demande(demande: NouvelleDemandeRequest) -> Dict[str, Any]:
    demandes = charger_demandes()

    nouvelle_entree = demande.dict()
    nouvelle_entree["id"] = f"REQ-{str(uuid4())[:8].upper()}"
    nouvelle_entree["statut"] = "en_attente"
    nouvelle_entree["nicad"] = None
    nouvelle_entree["titreFoncierCree"] = False

    demandes.append(nouvelle_entree)

    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(demandes, f, indent=2, ensure_ascii=False)

    return nouvelle_entree


def mettre_a_jour_statut_demande(id_demande: str, nouveau_statut: str) -> Dict[str, Any]:
    demandes = charger_demandes()
    mise_a_jour = None

    for d in demandes:
        if d["id"] == id_demande:
            d["statut"] = nouveau_statut
            mise_a_jour = d
            break

    if mise_a_jour is None:
        raise ValueError(f"Demande {id_demande} introuvable.")

    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(demandes, f, indent=2, ensure_ascii=False)

    return mise_a_jour

# Fonction pour mettre à jour le fichier de demandes
def mettre_a_jour_fichier_demandes(demandes: list[dict]):
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(demandes, f, indent=2, ensure_ascii=False)




def generer_pdf_deliberation(demande: dict) -> str:
    """
    Génère un PDF officiel de délibération communale basé sur les informations de la demande.
    Retourne le chemin relatif vers le fichier généré.
    """
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt="Délibération Municipale", ln=True, align="C")
    pdf.ln(10)

    texte = (
        f"Date : {datetime.now().strftime('%d/%m/%Y')}\n\n"
        f"Citoyen : {demande['citoyen']['prenom']} {demande['citoyen']['nom']}\n"
        f"Téléphone : {demande['citoyen']['telephone']}\n"
        f"ID demande : {demande['id']}\n"
        f"NICAD attribué : {demande['nicad'] or 'Non précisé'}\n\n"
        f"La présente délibération autorise la suite du processus de régularisation foncière.\n"
    )

    pdf.multi_cell(0, 10, txt=texte)

    chemin_pdf = f"documents/deliberations/delib_{demande['id']}.pdf"
    Path(chemin_pdf).parent.mkdir(parents=True, exist_ok=True)
    pdf.output(chemin_pdf)

    return chemin_pdf

def valider_deliberation_par_mairie(id_demande: str) -> dict:
    """
    Change le statut d'une demande vers 'deliberation_validee'
    et génère le PDF officiel de délibération.
    """
    demandes = charger_demandes()
    cible = None

    for d in demandes:
        if d["id"] == id_demande:
            if d["statut"] != "nicad_valide":
                raise ValueError("Impossible de valider la délibération : NICAD non validé.")
            d["statut"] = "deliberation_validee"
            d["deliberation_pdf"] = generer_pdf_deliberation(d)
            cible = d
            break

    if not cible:
        raise ValueError("Demande introuvable.")

    mettre_a_jour_fichier_demandes(demandes)
    return cible