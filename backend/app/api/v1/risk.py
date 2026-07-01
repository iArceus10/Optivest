from __future__ import annotations

from fastapi import APIRouter, HTTPException, status

from app.schemas.risk import (
    RiskAnalyticsRequest,
    RiskAnalyticsResponse,
)
from app.services.risk_analytics_service import (
    RiskAnalyticsService,
)

router = APIRouter(
    prefix="/risk",
    tags=["Risk Analytics"],
)


@router.post(
    "",
    response_model=RiskAnalyticsResponse,
    summary="Analyze portfolio risk",
)
def analyze_portfolio_risk(
    request: RiskAnalyticsRequest,
) -> RiskAnalyticsResponse:
    """
    Compute portfolio risk analytics.
    """

    try:
        result = (
            RiskAnalyticsService.analyze_portfolio_risk(
                tickers=request.tickers,
                weights=request.weights,
                start=request.start,
                end=request.end,
                risk_free_rate=request.risk_free_rate,
                confidence_level=request.confidence_level,
            )
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    return RiskAnalyticsResponse(
        sharpe_ratio=result.sharpe_ratio,
        sortino_ratio=result.sortino_ratio,
        maximum_drawdown=result.maximum_drawdown,
        value_at_risk=result.value_at_risk,
        conditional_value_at_risk=(
            result.conditional_value_at_risk
        ),
    )