import os
from fastapi import APIRouter, Depends, Query
from ..database import db_manager
from ..adapters import kpi_repository_in_memory
from ..ports.kpi_repository import KpiRepository

def get_db_cursor():
    return db_manager.get_cursor()

def get_total_records():
    return db_manager._total_records

def get_kpi_repo(cursor=Depends(get_db_cursor)):
    return kpi_repository_in_memory.KpiRepositoryInMemory(cursor, os.getenv('S3_DATA_PATH'))

router = APIRouter(
    prefix="/altkpis",
    tags=["altkpis"]
)

@router.get("/")
async def read_altkpis(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    kpi_repository: KpiRepository = Depends(get_kpi_repo),
    total_records: int = Depends(get_total_records)
):
    kpis = kpi_repository.get_kpis(page, size)
    
    return {
        "page": page,
        "total_reords": total_records,
        "data": kpis 
    }
