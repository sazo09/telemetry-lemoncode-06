import duckdb
from app.ports.kpi_repository import KpiRepository
from ..domain.models import Kpi as KpiModel


class KpiRepositoryInMemory(KpiRepository):
    def __init__(self, db_cursor: duckdb.DuckDBPyConnection, data_path=''):
        super().__init__()
        self.db_cursor = db_cursor
        self.data_path = data_path

    def get_kpis(self, page, size):
        offset = (page - 1) * size
        s3_path = self.data_path

        query = f"""
            SELECT * FROM read_parquet('{s3_path}')
            ORDER BY date ASC
            LIMIT {size} OFFSET {offset}
        """

        data = self.db_cursor.execute(query).df().to_dict(orient='records')
        
        results = [KpiModel(**item) for item in data]

        return results
