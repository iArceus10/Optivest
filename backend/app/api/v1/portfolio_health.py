from __future__ import annotations

from fastapi import APIRouter, HTTPException, status

from app.schemas.portfolio_health import (
    PortfolioHealthRequest,
    PortfolioHealthResponse,
)
from app.services.portfolio_health_service import (
    PortfolioHealthService,
)

router = APIRouter(
    prefix="/portfolio-health",
    tags=["Portfolio Health"],
)


@router.post(
    "",
    response_model=PortfolioHealthResponse,
    status_code=status.HTTP_200_OK,
)
def analyze_portfolio_health(
    request: PortfolioHealthRequest,
) -> PortfolioHealthResponse:
    """
    Analyze the overall health of a portfolio by combining return,
    risk, diversification, concentration, and Monte Carlo-based
    optimization efficiency diagnostics.
    """

    try:
        result = (
            PortfolioHealthService.analyze_portfolio_health(
                tickers=request.tickers,
                weights=request.weights,
                start=request.start,
                end=request.end,
                risk_free_rate=request.risk_free_rate,
                simulation_count=request.simulation_count,
                seed=request.seed,
            )
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    return PortfolioHealthResponse(
        overall_health_score=result.overall_health_score,
        return_score=result.return_score,
        risk_score=result.risk_score,
        diversification_score=result.diversification_score,
        concentration_score=result.concentration_score,
        optimization_efficiency_score=(
            result.optimization_efficiency_score
        ),
        summary=result.summary,
        recommendations=result.recommendations,
    )