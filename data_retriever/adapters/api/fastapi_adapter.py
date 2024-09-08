from fastapi import FastAPI
from .routes import create_router
from application.services import RetrieverService
from ports.repositories import BenchmarkRepository
from ports.caching import CachePort


def create_fastapi_app(repository: BenchmarkRepository, cache: CachePort):
    app = FastAPI(title="LLM Benchmark Data Retriever")

    retriever_service = RetrieverService(repository, cache)

    router = create_router(retriever_service)
    app.include_router(router)

    return app