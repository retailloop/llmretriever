import os
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from adapters.api.fastapi_adapter import create_fastapi_app
from adapters.persistence.sqlalchemy_adapter import init_db, SQLAlchemyRepository
from adapters.cache.redis_adapter import init_cache
from utils.logger import setup_logger

DATABASE_URL = os.getenv("DATABASE_URL").replace('postgres://', 'postgresql://')
REDIS_URL = os.getenv("REDIS_URL")
API_PORT = int(os.getenv("API_PORT", 8000))

logger = setup_logger(__name__)


def main():
    try:
        # Initialize database
        session_factory = init_db(DATABASE_URL)
        repository = SQLAlchemyRepository(session_factory)

        # Initialize cache
        cache = init_cache(REDIS_URL)

        # Create FastAPI app
        app = create_fastapi_app(repository, cache)

        # Add exception handler
        @app.exception_handler(Exception)
        async def unhandled_exception_handler(request: Request, exc: Exception):
            logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
            return JSONResponse(
                status_code=500,
                content={"message": "Internal server error"}
            )

        # Run the app
        import uvicorn
        uvicorn.run(app, host="0.0.0.0", port=API_PORT)
    except Exception as e:
        logger.error(f"Failed to start the application: {str(e)}", exc_info=True)
        raise


if __name__ == "__main__":
    main()
