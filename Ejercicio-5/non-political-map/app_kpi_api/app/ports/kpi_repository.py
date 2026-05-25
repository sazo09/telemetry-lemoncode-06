from abc import ABC, abstractmethod
from ..domain.models import Kpi as KpiModel

class KpiRepository(ABC):
    @abstractmethod
    def get_kpis(self, page: int, size: int) -> list[KpiModel]:
        raise NotImplementedError
