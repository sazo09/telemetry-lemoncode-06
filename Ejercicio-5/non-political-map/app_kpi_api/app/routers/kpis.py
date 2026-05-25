from fastapi import APIRouter, Depends, Query
from ..database import db_manager
import duckdb
import os

def get_db_cursor():
    return db_manager.get_cursor()


router = APIRouter(
    prefix="/kpis",
    tags=["kpis"]
)

@router.get("/")
async def read_kpis(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    cursor: duckdb.DuckDBPyConnection = Depends(get_db_cursor)
):
    offset = (page - 1) * size
    s3_path = os.getenv('S3_DATA_PATH')
    
    query = f"""
        SELECT * FROM read_parquet('{s3_path}')
        ORDER BY date ASC
        LIMIT {size} OFFSET {offset}
    """

    results = cursor.execute(query).df().to_dict()

    return {
        "page": page,
        "total_records": db_manager._total_records,
        "data": results
    }
