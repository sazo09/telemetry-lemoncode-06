from dataclasses import dataclass

@dataclass(frozen=True)
class Kpi:
    """
    Domain model representing a KPI
    """
    timestamp: str
    date: str
    hour: int
    service_name: str
    requests_per_minute: int
    unique_users: int