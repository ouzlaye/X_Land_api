from fastapi import FastAPI
from api_gateway import api_router

app = FastAPI(
    title="X-Land Sénégal Backend",
    description="Backend pour la plateforme d'interopérabilité foncière (MVP)",
    version="0.1.0"
)

app.include_router(api_router, prefix="/api")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)