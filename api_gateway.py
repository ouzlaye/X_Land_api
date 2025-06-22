from fastapi import FastAPI
from routers import dgid, conservation, logs, mairie, procedure, hypotheque, demande

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
    app.include_router(logs.router, prefix="/api", tags=["X-Road Logs"])
    app.include_router(procedure.router, prefix="/api", tags=["Procédure Demande D'attribution Foncière"])
    app.include_router(hypotheque.router, prefix="/api", tags=["Hypothèque"])
    # app.include_router.demande.router, prefix="/api", tags=["Demande Citoyenne"])
    app.include_router(demande.router, prefix="/api", tags=["Retourne toutes les Demandes"])


# ✅ Ajout de l’inclusion des routes
include_all_routers(app)