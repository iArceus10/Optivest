from __future__ import annotations

from datetime import date

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query,
    status,
)

from app.api.dependencies.auth import get_current_user
from app.models.user import User

from app.schemas.statistics import (
    CorrelationMatrixResponse,
    CovarianceMatrixResponse,
    ExpectedReturnsResponse,
    PortfolioVolatilityResponse,
)
from app.services.statistics_service import StatisticsService

router = APIRouter(
    prefix="/statistics",
    tags=["Statistics"],
)


@router.get(
    "/returns",
    response_model=ExpectedReturnsResponse,
)
def get_expected_returns(
    tickers: list[str] = Query(...),
    start: date = Query(...),
    end: date = Query(...),
    current_user: User = Depends(get_current_user),
) -> ExpectedReturnsResponse:
    """
    Return annualized expected returns.
    """

    try:
        returns = StatisticsService.get_expected_returns(
            tickers=tickers,
            start=start,
            end=end,
        )

        return ExpectedReturnsResponse(
            expected_returns=returns.to_dict(),
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )


@router.get(
    "/covariance",
    response_model=CovarianceMatrixResponse,
)
def get_covariance_matrix(
    tickers: list[str] = Query(...),
    start: date = Query(...),
    end: date = Query(...),
    current_user: User = Depends(get_current_user),
) -> CovarianceMatrixResponse:
    """
    Return the annualized covariance matrix.
    """

    try:
        covariance = StatisticsService.get_covariance_matrix(
            tickers=tickers,
            start=start,
            end=end,
        )

        return CovarianceMatrixResponse(
            covariance_matrix=covariance.to_dict(),
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )


@router.get(
    "/correlation",
    response_model=CorrelationMatrixResponse,
)
def get_correlation_matrix(
    tickers: list[str] = Query(...),
    start: date = Query(...),
    end: date = Query(...),
    current_user: User = Depends(get_current_user),
) -> CorrelationMatrixResponse:
    """
    Return the correlation matrix.
    """

    try:
        correlation = StatisticsService.get_correlation_matrix(
            tickers=tickers,
            start=start,
            end=end,
        )

        return CorrelationMatrixResponse(
            correlation_matrix=correlation.to_dict(),
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )


@router.get(
    "/volatility",
    response_model=PortfolioVolatilityResponse,
)
def get_portfolio_volatility(
    tickers: list[str] = Query(...),
    weights: list[float] = Query(...),
    start: date = Query(...),
    end: date = Query(...),
    current_user: User = Depends(get_current_user),
) -> PortfolioVolatilityResponse:
    """
    Return annualized portfolio volatility.
    """

    try:
        volatility = StatisticsService.get_portfolio_volatility(
            tickers=tickers,
            weights=weights,
            start=start,
            end=end,
        )

        return PortfolioVolatilityResponse(
            portfolio_volatility=volatility,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )