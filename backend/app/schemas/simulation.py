from __future__ import annotations

from datetime import date

from pydantic import BaseModel, ConfigDict, Field

from app.financial_engines.simulation.monte_carlo import (
    DEFAULT_RISK_FREE_RATE,
    DEFAULT_SIMULATION_COUNT,
)


class MonteCarloSimulationRequest(BaseModel):
    """
    Request for Monte Carlo portfolio simulation.
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

    simulation_count: int = Field(
        default=DEFAULT_SIMULATION_COUNT,
        gt=0,
        description="Number of random portfolios to simulate.",
    )

    risk_free_rate: float = Field(
        default=DEFAULT_RISK_FREE_RATE,
        description="Annual risk-free rate.",
    )

    seed: int | None = Field(
        default=None,
        description=(
            "Optional random seed for deterministic simulations."
        ),
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


class MonteCarloPortfolioResponse(BaseModel):
    """
    One simulated portfolio.
    """

    expected_return: float = Field(
        ...,
        description="Annualized expected portfolio return.",
    )

    volatility: float = Field(
        ...,
        ge=0,
        description="Annualized portfolio volatility.",
    )

    sharpe_ratio: float = Field(
        ...,
        description="Annualized Sharpe ratio.",
    )

    allocations: list[PortfolioWeight]


class MonteCarloSimulationResponse(BaseModel):
    """
    Complete Monte Carlo simulation response.
    """

    portfolios: list[
        MonteCarloPortfolioResponse
    ]

    best_sharpe: MonteCarloPortfolioResponse

    minimum_volatility: MonteCarloPortfolioResponse