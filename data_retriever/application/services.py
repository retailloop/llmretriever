from domain.retriever import Retriever
from ports.repositories import BenchmarkRepository
from ports.caching import CachePort
from typing import List, Dict
from domain.models import Ranking

class RetrieverService:
    def __init__(self, repository: BenchmarkRepository, cache: CachePort):
        self.retriever = Retriever(repository, cache)
        self.cache = cache

    def get_ranking(self, metric: str) -> List[Dict]:
        cache_key = f"ranking:{metric}"
        cached_ranking = self.cache.get(cache_key)

        if cached_ranking:
            return cached_ranking

        ranking = self.retriever.get_ranking(metric)
        if ranking:
            self.cache.set(cache_key, ranking)

        return ranking

    def get_available_metrics(self) -> List[str]:
        return self.retriever.get_available_metrics()

    def get_available_models(self) -> List[str]:
        return self.retriever.get_available_models()