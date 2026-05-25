import pytest
from fastapi.testclient import TestClient
from typing import List, Dict, Any

from ..main import app 
from ..routers.altkpis import get_kpi_repo, get_total_records

class MockKpiRepository:
    def __init__(self):
        self.mock_data = [
            {"id": 1, "value": 10.5},
            {"id": 2, "value": 20.0},
            {"id": 3, "value": 35.2}
        ]

    def get_kpis(self, page: int, size: int) -> List[Dict[str, Any]]:
        offset = (page - 1) * size
        return self.mock_data[offset : offset + size]

@pytest.fixture
def client():
    """
    Setup the TestClient and swap real dependencies for mocks.
    """
    mock_repo = MockKpiRepository()

    app.dependency_overrides[get_kpi_repo] = lambda: mock_repo

    app.dependency_overrides[get_total_records] = lambda: 3

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()

def test_read_altkpis_success(client: TestClient):
    """Test that the endpoint returns 200 OK and correct JSON structure."""
    response = client.get("/altkpis/?page=1&size=2")
    
    assert response.status_code == 200
    json_data = response.json()
    
    assert json_data["page"] == 1
    assert json_data["total_reords"] == 3 
    assert len(json_data["data"]) == 2
    assert json_data["data"][0]["value"] == 10.5

def test_read_altkpis_pagination_logic(client: TestClient):
    """Test that page 2 correctly offsets the data."""
    response = client.get("/altkpis/?page=2&size=2")
    
    assert response.status_code == 200
    json_data = response.json()

    assert len(json_data["data"]) == 1
    assert json_data["data"][0]["id"] == 3

def test_read_altkpis_validation_failure(client: TestClient):
    """Test that invalid parameters trigger a 422 error."""
    response = client.get("/altkpis/?page=0")
    assert response.status_code == 422

    response = client.get("/altkpis/?size=101")
    assert response.status_code == 422