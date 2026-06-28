from fastapi import FastAPI

from app.core.config import settings

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
)


@app.get("/", tags=["Root"])
async def root():
    return {
        "message": "Welcome to OptiVest API",
        "version": settings.app_version,
    }


@app.get("/health", tags=["Health"])
async def health():
    return {
        "status": "healthy",
        "environment": settings.environment,
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
    )