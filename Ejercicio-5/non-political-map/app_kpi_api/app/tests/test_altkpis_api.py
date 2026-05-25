import pytest
from fastapi.testclient import TestClient
from typing import List, Dict, Any

# 1. Import your FastAPI app and the specific dependencies to override
# Assuming your main app is in 'main.py' and router is included there
from ..main import app 
from ..routers.altkpis import get_kpi_repo, get_total_records

# 2. Define a Mock Repository to replace the real DuckDB/In-Memory logic
class MockKpiRepository:
    def __init__(self):
        # Mock data for testing
        self.mock_data = [
            {"id": 1, "value": 10.5},
            {"id": 2, "value": 20.0},
            {"id": 3, "value": 35.2}
        ]

    def get_kpis(self, page: int, size: int) -> List[Dict[str, Any]]:
        offset = (page - 1) * size
        return self.mock_data[offset : offset + size]

# 3. Use a Pytest Fixture to manage the TestClient and Dependency Overrides
@pytest.fixture
def client():
    """
    Setup the TestClient and swap real dependencies for mocks.
    """
    # Create the mock instance
    mock_repo = MockKpiRepository()

    # Override the repository creation logic
    app.dependency_overrides[get_kpi_repo] = lambda: mock_repo
    
    # Override the total records fetch (returning a static number for testing)
    app.dependency_overrides[get_total_records] = lambda: 3
    
    # Instantiate the FastAPI TestClient
    with TestClient(app) as test_client:
        yield test_client
    
    # Clean up overrides after the test is finished
    app.dependency_overrides.clear()

# --- 4. The Actual Test Cases ---

def test_read_altkpis_success(client: TestClient):
    """Test that the endpoint returns 200 OK and correct JSON structure."""
    response = client.get("/altkpis/?page=1&size=2")
    
    assert response.status_code == 200
    json_data = response.json()
    
    assert json_data["page"] == 1
    # Note: Using your existing typo 'total_reords' so the test passes!
    assert json_data["total_reords"] == 3 
    assert len(json_data["data"]) == 2
    assert json_data["data"][0]["value"] == 10.5

def test_read_altkpis_pagination_logic(client: TestClient):
    """Test that page 2 correctly offsets the data."""
    response = client.get("/altkpis/?page=2&size=2")
    
    assert response.status_code == 200
    json_data = response.json()
    
    # Page 2 with size 2 should return only the 3rd item
    assert len(json_data["data"]) == 1
    assert json_data["data"][0]["id"] == 3

def test_read_altkpis_validation_failure(client: TestClient):
    """Test that invalid parameters trigger a 422 error."""
    # Test 'ge=1' constraint
    response = client.get("/altkpis/?page=0")
    assert response.status_code == 422
    
    # Test 'le=100' constraint
    response = client.get("/altkpis/?size=101")
    assert response.status_code == 422