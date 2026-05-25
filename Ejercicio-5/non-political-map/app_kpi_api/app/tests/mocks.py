from typing import List, Dict, Any

class MockKpiRepository:
    """A clean mock that follows the KpiRepository port."""
    def __init__(self):
        self.data = [
            {"id": 1, "name": "KPI 1"},
            {"id": 2, "name": "KPI 2"},
            {"id": 3, "name": "KPI 3"}
        ]

    def get_kpis(self, page: int, size: int) -> List[Dict[str, Any]]:
        offset = (page - 1) * size
        return self.data[offset : offset + size]