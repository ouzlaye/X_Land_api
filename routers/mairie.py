from fastapi import APIRouter
from schema.mairie_schema import DemandeFonciereCreate, DemandeFonciere
from services.mairie_service import soumettre_demande
from services.mairie_service import charger_demandes_existantes 
from fastapi import HTTPException
from services.supabase_sync import restaurer_fichier
import asyncio

router = APIRouter()

@router.post("/citizenRequest", response_model=DemandeFonciere, summary="Soumettre une demande citoyenne de régularisation ou attribution foncière")
async def soumettre_demande_citoyenne(payload: DemandeFonciereCreate):
    demande = soumettre_demande(payload)
    asyncio.create_task(retarder_restoration())
    return demande

async def retarder_restoration():
    await asyncio.sleep(5)
    restaurer_fichier("citizen_requests.json")


"""@router.get("/citizenRequest/{id}", response_model=DemandeFonciere, summary="Consulter une demande foncière")
def consulter_statut_demande(id: str):
    
    #Retourne les détails d'une demande citoyenne (statut, historique, NICAD, bail, etc.).
    
    demandes = charger_demandes_existantes()
    for demande in demandes:
        if demande["id"] == id:
            return demande

    raise HTTPException(status_code=404, detail="Demande introuvable")"""