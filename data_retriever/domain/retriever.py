from typing import List
from .models import Ranking

class Retriever:
    def __init__(self, repository, cache):
        self.repository = repository
        self.cache = cache

    async def get_ranking(self, metric: str) -> List[Ranking]:
        cache_key = f"ranking:{metric}"
        cached_ranking = await self.cache.get(cache_key)

        if cached_ranking:
            return cached_ranking

        ranking = await self.repository.get_ranking(metric)
        await self.cache.set(cache_key, ranking)

        return ranking


    async def get_available_metrics(self) -> List[str]:
        return await self.repository.get_available_metrics()

    async def get_available_models(self) -> List[str]:
        return await self.repository.get_available_models()