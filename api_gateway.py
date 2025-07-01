from fastapi import FastAPI
from routers import  conservation, logs, mairie, procedure, hypotheque, demande, updateRequest
from services.supabase_sync import restaurer_fichier
import os
app = FastAPI()

@app.get("/")
def home():
    return {"message": "X-Land API en ligne !"}

def include_all_routers(app: FastAPI):
    #app.include_router(dgid.router, prefix="/api", tags=["DGID"])
    # app.include_router(cadastre.router, prefix="/api", tags=["Cadastre"])
    app.include_router(mairie.router, prefix="/api", tags=["Mairie"])
    app.include_router(conservation.router, prefix="/api", tags=["Conservation Foncière"])
    # app.include_router(blockchain.router, prefix="/api", tags=["Blockchain PoC"])
   # app.include_router(logs.router, prefix="/api", tags=["X-Road Logs"])
   # app.include_router(procedure.router, prefix="/api", tags=["Procédure Demande D'attribution Foncière"])
    #app.include_router(hypotheque.router, prefix="/api", tags=["Hypothèque"])
    # app.include_router.demande.router, prefix="/api", tags=["Demande Citoyenne"])
    app.include_router(demande.router, prefix="/api", tags=["Retourne toutes les Demandes"])
    #mise a jours des statut
    app.include_router(updateRequest.router, prefix="/api", tags=["Mise à jour des demandes depuis le frontend"])    



    


# 🔁 Toujours recharger la dernière version synchronisée
restaurer_fichier("citizen_requests.json")
restaurer_fichier("conservation_data.json")

# ✅ Ajout de l’inclusion des routes
include_all_routers(app)