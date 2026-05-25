import pytest
import duckdb
import pandas as pd
from app.adapters.kpi_repository_in_memory import KpiRepositoryInMemory
from app.domain.models import Kpi

class TestKpiRepositoryInMemory:

    @pytest.fixture(autouse=True)
    def setup_data(self, tmp_path):
        """
        Setup a temporary Parquet file and DuckDB connection.
        """
        data = {
            'timestamp': ['2026-04-04 10:00:00', '2026-04-04 11:00:00', '2026-04-04 12:00:00'],
            'date': ['2026-04-04', '2026-04-04', '2026-04-04'],
            'hour': [10, 11, 12],
            'service_name': ['auth-service', 'payment-service', 'auth-service'],
            'requests_per_minute': [150, 200, 180],
            'unique_users': [50, 60, 55]
        }
        df = pd.DataFrame(data)

        self.temp_parquet = str(tmp_path / "test_data.parquet")
        df.to_parquet(self.temp_parquet)

        self.con = duckdb.connect(database=':memory:')

        self.repo = KpiRepositoryInMemory(db_cursor=self.con, data_path=self.temp_parquet)
        yield

    def test_get_kpis_mapping_success(self):
        """Verify that dictionary unpacking correctly creates Kpi objects."""
        results = self.repo.get_kpis(page=1, size=1)
        
        assert len(results) == 1
        kpi = results[0]

        assert isinstance(kpi, Kpi)
        assert kpi.service_name == 'auth-service'
        assert kpi.requests_per_minute == 150
        assert kpi.hour == 10

    def test_get_kpis_pagination_logic(self):
        """Verify that OFFSET and LIMIT work correctly across pages."""
        results = self.repo.get_kpis(page=2, size=1)
        
        assert len(results) == 1
        assert results[0].hour == 11
        assert results[0].service_name == 'payment-service'

    def test_get_kpis_returns_empty_list_when_no_data(self):
        """Ensure requesting a page beyond available data returns an empty list."""
        results = self.repo.get_kpis(page=5, size=10)
        assert results == []

    def test_get_kpis_handles_all_columns(self):
        """Verify that all fields in the dataclass are populated."""
        results = self.repo.get_kpis(page=1, size=3)
        kpi = results[-1]
        
        assert kpi.timestamp == '2026-04-04 12:00:00'
        assert kpi.unique_users == 55
        assert kpi.date == '2026-04-04'