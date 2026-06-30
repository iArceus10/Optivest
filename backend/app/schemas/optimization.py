from __future__ import annotations

from datetime import date

from pydantic import BaseModel, ConfigDict, Field

from app.financial_engines.optimization.efficient_frontier import (
    DEFAULT_FRONTIER_POINTS,
)
from app.financial_engines.optimization.maximum_sharpe import (
    DEFAULT_RISK_FREE_RATE,
)
from app.financial_engines.optimization.mean_variance import (
    DEFAULT_RISK_AVERSION,
)


class OptimizationRequestBase(BaseModel):
    """
    Base request model shared by all optimization endpoints.
    """

    model_config = ConfigDict(
        extra="forbid",
    )

    tickers: list[str] = Field(
        ...,
        min_length=2,
        description="Portfolio asset tickers.",
        examples=[["AAPL", "MSFT", "NVDA"]],
    )

    start: date = Field(
        ...,
        description="Start date for historical market data.",
    )

    end: date = Field(
        ...,
        description="End date for historical market data.",
    )


class MeanVarianceOptimizationRequest(
    OptimizationRequestBase,
):
    """
    Request for Mean-Variance optimization.
    """

    risk_aversion: float = Field(
        default=DEFAULT_RISK_AVERSION,
        gt=0,
        description=(
            "Risk-aversion coefficient. "
            "Higher values produce more conservative portfolios."
        ),
    )


class MinimumVarianceOptimizationRequest(
    OptimizationRequestBase,
):
    """
    Request for Minimum Variance optimization.
    """

    pass


class MaximumSharpeOptimizationRequest(
    OptimizationRequestBase,
):
    """
    Request for Maximum Sharpe optimization.
    """

    risk_free_rate: float = Field(
        default=DEFAULT_RISK_FREE_RATE,
        description="Annual risk-free rate.",
    )


class EfficientFrontierRequest(
    OptimizationRequestBase,
):
    """
    Request for Efficient Frontier generation.
    """

    num_points: int = Field(
        default=DEFAULT_FRONTIER_POINTS,
        gt=0,
        description="Number of portfolios to generate.",
    )


class PortfolioWeight(BaseModel):
    """
    Portfolio allocation for a single asset.
    """

    ticker: str = Field(
        ...,
        description="Ticker symbol.",
    )

    weight: float = Field(
        ...,
        ge=0,
        le=1,
        description="Normalized portfolio weight.",
    )


class OptimizationResponse(BaseModel):
    """
    Response for an optimized portfolio.
    """

    allocations: list[PortfolioWeight] = Field(
        ...,
        description="Optimized portfolio allocations.",
    )


class EfficientFrontierPointResponse(BaseModel):
    """
    One portfolio on the Efficient Frontier.
    """

    expected_return: float = Field(
        ...,
        ge=0,
        description="Annualized expected portfolio return.",
    )

    volatility: float = Field(
        ...,
        ge=0,
        description="Annualized portfolio volatility.",
    )

    allocations: list[PortfolioWeight]


class EfficientFrontierResponse(BaseModel):
    """
    Response containing the Efficient Frontier.
    """

    frontier: list[
        EfficientFrontierPointResponse
    ]