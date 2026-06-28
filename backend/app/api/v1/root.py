from fastapi import APIRouter

from app.core.config import settings

router = APIRouter(tags=["Root"])


@router.get("/")
async def root() -> dict[str, str]:
    return {
        "message": "Welcome to OptiVest API",
        "version": settings.app_version,
    }