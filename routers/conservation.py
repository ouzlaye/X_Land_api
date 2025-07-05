from fastapi import APIRouter, HTTPException, Query
from schema.conservation_schema import VerifyTitleRequest, TitleFoncierModel
from services.conservation_service import rechercher_titre_foncier
from services.fichier_sync import lire_fichier
from fastapi import APIRouter, Query
import requests
from fastapi.responses import JSONResponse

router = APIRouter()


@router.get("/verifierTitre", summary="Vérification de l’état de droit réel d’un titre")
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




@router.get("/test_xroad_verification", summary="Tester l’appel X-Road pour la vérification d’un titre")
def test_xroad_verification(
    identifiant: str = Query(..., description="Identifiant du titre à tester (NICAD ou numéro de titre)")
):
    # Adresse du Security Server X-Road
    xroad_url = (
        "http://localhost:8080/r1/CS/ORG/1111/TestService/local-service-test/api/verifierTitre"
    )

    headers = {
        "X-Road-Client": "CS/ORG/1111/TestClient"
    }

    params = {
        "identifiant": identifiant
    }

    try:
        response = requests.get(xroad_url, headers=headers, params=params, timeout=10)

        if response.status_code == 200:
            return {
                "statut": "✅ Succès",
                "données": response.json()
            }
        else:
            return JSONResponse(
                status_code=response.status_code,
                content={
                    "statut": "❌ Échec",
                    "code": response.status_code,
                    "erreur": response.text
                }
            )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"statut": "❌ Erreur interne", "détail": str(e)}
        )
