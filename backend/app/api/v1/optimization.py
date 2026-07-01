from fastapi import APIRouter, HTTPException, status
import pandas as pd

from app.schemas.optimization import (
    EfficientFrontierRequest,
    EfficientFrontierPointResponse,
    EfficientFrontierResponse,
    MaximumSharpeOptimizationRequest,
    MeanVarianceOptimizationRequest,
    MinimumVarianceOptimizationRequest,
    OptimizationResponse,
    PortfolioWeight,
)
from app.services.optimization_service import (
    OptimizationService,
)

router = APIRouter(
    prefix="/optimization",
    tags=["Optimization"],
)


def _serialize_allocations(
    weights: pd.Series,
) -> OptimizationResponse:
    """
    Convert portfolio weights into an API response.
    """

    return OptimizationResponse(
        allocations=[
            PortfolioWeight(
                ticker=ticker,
                weight=float(weight),
            )
            for ticker, weight in weights.items()
        ]
    )


@router.post(
    "/mean-variance",
    response_model=OptimizationResponse,
)
def mean_variance(
    request: MeanVarianceOptimizationRequest,
) -> OptimizationResponse:
    """
    Compute the Mean-Variance optimal portfolio.
    """

    try:
        weights = (
            OptimizationService.get_mean_variance_portfolio(
                tickers=request.tickers,
                start=request.start,
                end=request.end,
                risk_aversion=request.risk_aversion,
            )
        )

        return _serialize_allocations(weights)

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc


@router.post(
    "/minimum-variance",
    response_model=OptimizationResponse,
)
def minimum_variance(
    request: MinimumVarianceOptimizationRequest,
) -> OptimizationResponse:
    """
    Compute the Minimum Variance portfolio.
    """

    try:
        weights = (
            OptimizationService.get_minimum_variance_portfolio(
                tickers=request.tickers,
                start=request.start,
                end=request.end,
            )
        )

        return _serialize_allocations(weights)

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc


@router.post(
    "/maximum-sharpe",
    response_model=OptimizationResponse,
)
def maximum_sharpe(
    request: MaximumSharpeOptimizationRequest,
) -> OptimizationResponse:
    """
    Compute the Maximum Sharpe Ratio portfolio.
    """

    try:
        weights = (
            OptimizationService.get_maximum_sharpe_portfolio(
                tickers=request.tickers,
                start=request.start,
                end=request.end,
                risk_free_rate=request.risk_free_rate,
            )
        )

        return _serialize_allocations(weights)

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc


@router.post(
    "/efficient-frontier",
    response_model=EfficientFrontierResponse,
)
def efficient_frontier(
    request: EfficientFrontierRequest,
) -> EfficientFrontierResponse:
    """
    Generate the Efficient Frontier.
    """

    try:
        frontier = (
            OptimizationService.get_efficient_frontier(
                tickers=request.tickers,
                start=request.start,
                end=request.end,
                num_points=request.num_points,
            )
        )

        return EfficientFrontierResponse(
            frontier=[
                EfficientFrontierPointResponse(
                    expected_return=point.expected_return,
                    volatility=point.volatility,
                    allocations=[
                        PortfolioWeight(
                            ticker=ticker,
                            weight=float(weight),
                        )
                        for ticker, weight in point.weights.items()
                    ],
                )
                for point in frontier
            ]
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc