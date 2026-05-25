from fastapi import FastAPI, Response
from fastapi.staticfiles import StaticFiles
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST, REGISTRY
from .api.endpoints import router as item_router

app = FastAPI()

app.include_router(item_router)

@app.get("/metrics")
def metrics():
    return Response(generate_latest(REGISTRY), media_type=CONTENT_TYPE_LATEST)

app.mount('/', StaticFiles(directory="statics", html=True), name="static")
