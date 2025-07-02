from fastapi import APIRouter, HTTPException, Query
from schema.conservation_schema import VerifyTitleRequest, TitleFoncierModel
from services.conservation_service import rechercher_titre_foncier
from services.fichier_sync import lire_fichier

router = APIRouter()


@router.get("/verifierTitre", tags=["Vérification"])
def verifier_titre(
    identifiant: str = Query(..., description="Numéro de bail, de titre foncier ou NICAD")
):
    titres = lire_fichier("conservation_data.json")

    # Recherche souple selon le type d’identifiant
    for titre in titres:
        if (
            identifiant.strip() == titre.get("numeroTitre") or
            identifiant.strip() == titre.get("nicad")
        ):
            return {
                "numeroTitre": titre["numeroTitre"],
                "nicad": titre["nicad"],
                "proprietaireInscrit": titre["proprietaireInscrit"],
                "designation": titre["designation"],
                "situation": titre["situation"],
                "superficie": titre["superficie"],
                "coordonnees": titre.get("coordonnees", {}),
                "modeAcquisition": titre["modeAcquisition"],
                "dateInscription": titre["dateInscription"],
                "hypotheque": titre["hypotheque"],
                "nota": titre["nota"],
                "source": "registre_foncier_simulé"
            }

    raise HTTPException(status_code=404, detail="Aucun titre correspondant trouvé.")