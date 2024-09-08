from abc import ABC, abstractmethod
from typing import List
from domain.models import Ranking


class BenchmarkRepository(ABC):
    @abstractmethod
    async def get_ranking(self, metric: str) -> List[Ranking]:
        pass

    @abstractmethod
    async def get_available_metrics(self) -> List[str]:
        pass

    @abstractmethod
    async def get_available_models(self) -> List[str]:
        pass
