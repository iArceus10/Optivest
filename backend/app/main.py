from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.v1.router import api_router
from app.core.config import settings
from app.core.logging import configure_logging, get_logger

# Configure logging once when the application starts
configure_logging()
logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting OptiVest API")
    yield
    logger.info("Stopping OptiVest API")


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Portfolio Optimization and Risk Analytics Platform.",
    lifespan=lifespan,
)

# Register all API routes
app.include_router(api_router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
    )

@app.get("/", tags=["Root"])
async def root() -> dict[str, str]:
    return {
        "message": "Welcome to OptiVest API",
        "docs": "/docs",
        "api": "/api/v1",
        "version": settings.app_version,
    }