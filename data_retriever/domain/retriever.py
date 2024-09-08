from typing import List
from .models import Ranking
from ports.repositories import BenchmarkRepository
from ports.caching import CachePort

class Retriever:
    def __init__(self, repository: BenchmarkRepository, cache: CachePort):
        self.repository = repository
        self.cache = cache

    def get_ranking(self, metric: str) -> List[Ranking]:
        return self.repository.get_ranking(metric)

    def get_available_metrics(self) -> List[str]:
        return self.repository.get_available_metrics()

    def get_available_models(self) -> List[str]:
        return self.repository.get_available_models()