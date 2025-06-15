from fastapi import FastAPI
from api_gateway import include_all_routers
from middleware.xroad_tracer import xroad_tracer_middleware

app = FastAPI(title="X-Land Backend - Sénégal", version="0.1")

# Middleware de traçabilité simulée
app.middleware("http")(xroad_tracer_middleware)

# Inclusion des routes depuis le Gateway
include_all_routers(app)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)