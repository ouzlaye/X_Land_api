from fastapi import FastAPI
from routers import conservation 
from routers import logs, mairie, dgid, demande



app = FastAPI(title="X-Land Sénégal - API Gateway", version="0.1")

# Intégration du routeur pour le service de conservation foncière
app.include_router(conservation.router)
# Intégration du routeur pour les logs 
app.include_router(logs.router)
# Intégration du routeur pour la mairie
app.include_router(mairie.router)
# Intégration du routeur pour la DGID  
app.include_router(dgid.router)
# Intégration du routeur pour les demandes
app.include_router(demande.router)
