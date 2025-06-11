from datetime import datetime
from pathlib import Path
from fpdf import FPDF
import random

def generer_numero_acte(type_acte: str, annee: int = None) -> str:
    """
    Génère un numéro d’acte formaté selon le type et l’année.
    Exemple : 'BA-2025-0001' ou 'TF-2025-0009'
    """
    prefixe = {
        "bail_agricole": "BA",
        "bail_habitation": "BH",
        "titre_foncier": "TF"
    }.get(type_acte, "XX")

    annee = annee or datetime.now().year
    numero = random.randint(1, 9999)
    return f"{prefixe}-{annee}-{numero:04d}"

def generer_pdf_notification_acte(demande: dict, numero_acte: str, type_acte: str) -> str:
    """
    Génère un document PDF de notification d'acte émis par la DGID.
    """
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    titre = {
        "bail_agricole": "Notification de bail agricole",
        "bail_habitation": "Notification de bail à usage d'habitation",
        "titre_foncier": "Notification de titre foncier"
    }.get(type_acte, "Notification d’acte foncier")

    pdf.cell(200, 10, txt=titre, ln=True, align="C")
    pdf.ln(10)

    texte = (
        f"Demande ID : {demande['id']}\n"
        f"Citoyen : {demande['citoyen']['prenom']} {demande['citoyen']['nom']}\n"
        f"NICAD : {demande.get('nicad') or 'Non renseigné'}\n"
        f"Type d’acte : {type_acte}\n"
        f"Numéro d’acte : {numero_acte}\n"
        f"Date : {datetime.now().strftime('%d/%m/%Y')}\n\n"
        f"L’acte est désormais inscrit dans le système d’enregistrement foncier national."
    )
    texte = texte.encode("latin-1", "replace").decode("latin-1")

    pdf.multi_cell(0, 10, txt=texte)

    chemin_pdf = f"documents/actes/notification_acte_{demande['id']}.pdf"
    Path(chemin_pdf).parent.mkdir(parents=True, exist_ok=True)
    pdf.output(chemin_pdf)

    return chemin_pdf

def traiter_demande_acte_foncier(demande: dict, type_acte: str) -> dict:
    """
    Traite la demande d’acte foncier après validation de la délibération.
    Génère le numéro d’acte + PDF et retourne la structure à insérer.
    """
    if demande["statut"] != "deliberation_validee":
        raise ValueError("La demande n'est pas éligible : délibération non validée.")

    numero_acte = generer_numero_acte(type_acte)
    chemin_pdf = generer_pdf_notification_acte(demande, numero_acte, type_acte)

    return {
        "type": type_acte,
        "numero": numero_acte,
        "pdf": chemin_pdf
    }
