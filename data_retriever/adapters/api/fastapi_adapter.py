from fastapi import FastAPI
from .routes import router


def create_fastapi_app(retriever_service):
    app = FastAPI(title="LLM Benchmark Data Retriever")
    app.include_router(router)
    app.state.retriever_service = retriever_service
    return app
