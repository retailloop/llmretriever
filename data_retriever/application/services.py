from domain.retriever import Retriever
from ports.repositories import BenchmarkRepository
from ports.caching import CachePort


class RetrieverService:
    def __init__(self, repository: BenchmarkRepository, cache: CachePort):
        self.retriever = Retriever(repository, cache)

    async def get_ranking(self, metric: str):
        return await self.retriever.get_ranking(metric)

    async def get_available_metrics(self):
        return await self.retriever.get_available_metrics()

    async def get_available_models(self):
        return await self.retriever.get_available_models()
