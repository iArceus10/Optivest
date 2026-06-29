from fastapi import APIRouter

from app.api.v1.auth import router as auth_router
from app.api.v1.health import router as health_router
from app.api.v1.market_data import router as market_data_router
from app.api.v1.portfolio import router as portfolio_router
from app.api.v1.root import router as root_router

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(root_router)
api_router.include_router(health_router)
api_router.include_router(auth_router)
api_router.include_router(portfolio_router)
api_router.include_router(market_data_router)