import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch
import pandas as pd
from fastapi import FastAPI

# 1. Use absolute imports for your local modules
from app.routers.kpis import router, get_db_cursor

app = FastAPI()
app.include_router(router)
client = TestClient(app)

## --- Fixtures ---

@pytest.fixture
def mock_cursor():
    mock = MagicMock()
    # Create a dummy DataFrame to return
    mock_df = pd.DataFrame([{"id": 1, "val": 10}])
    mock.execute.return_value.df.return_value = mock_df
    return mock

## --- Tests ---

def test_read_kpis_success(mock_cursor):
    # Fix 1: Use the absolute path to your db_manager for patching
    with patch("app.routers.kpis.db_manager") as mock_db_mgr, \
         patch.dict("os.environ", {"S3_DATA_PATH": "s3://test.parquet"}):
        
        # Setup mock behavior
        mock_db_mgr._total_records = 100
        app.dependency_overrides[get_db_cursor] = lambda: mock_cursor
        
        response = client.get("/kpis/?page=1&size=5")
        
        assert response.status_code == 200
        json_data = response.json()
        assert json_data["total_records"] == 100
        assert "LIMIT 5 OFFSET 0" in mock_cursor.execute.call_args[0][0]

    app.dependency_overrides.clear()

def test_read_kpis_validation_errors():
    """
    This test failed with 'NoneType' because even though it's a validation error, 
    FastAPI might still be trying to resolve dependencies. 
    We mock the manager here to prevent the crash.
    """
    with patch("app.routers.kpis.db_manager"):
        # Page must be >= 1
        response = client.get("/kpis/?page=0")
        assert response.status_code == 422
        
        # Size must be <= 100
        response = client.get("/kpis/?size=101")
        assert response.status_code == 422
