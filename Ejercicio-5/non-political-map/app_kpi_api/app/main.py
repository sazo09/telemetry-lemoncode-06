from fastapi import FastAPI
from contextlib import asynccontextmanager
from .routers import kpis, altkpis
from .config import main as config_main
from .database import db_manager

@asynccontextmanager
async def lifespan(app: FastAPI):
    config_main()
    db_manager.connect()
    db_manager.metadata()

    yield

    db_manager.disconnect()

app = FastAPI(lifespan=lifespan)

app.include_router(kpis.router)
app.include_router(altkpis.router)

@app.get("/")
async def root():
    return {"message": "Hello"}
