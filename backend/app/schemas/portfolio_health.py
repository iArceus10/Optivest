from __future__ import annotations

from datetime import date

from pydantic import BaseModel, ConfigDict, Field

from app.financial_engines.risk.ratios import (
    DEFAULT_RISK_FREE_RATE,
)


class PortfolioHealthRequest(BaseModel):
    """
    Request schema for portfolio health analytics.
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

    weights: list[float] = Field(
        ...,
        min_length=2,
        description="Portfolio asset weights.",
        examples=[[0.4, 0.35, 0.25]],
    )

    start: date = Field(
        ...,
        description="Start date for historical market data.",
    )

    end: date = Field(
        ...,
        description="End date for historical market data.",
    )

    risk_free_rate: float = Field(
        default=DEFAULT_RISK_FREE_RATE,
        description="Annual risk-free rate used for risk metrics and Monte Carlo simulation.",
    )

    simulation_count: int = Field(
        default=10_000,
        gt=0,
        description="Number of Monte Carlo portfolios to simulate.",
    )

    seed: int | None = Field(
        default=None,
        description="Optional random seed for deterministic Monte Carlo simulation.",
    )


class PortfolioHealthResponse(BaseModel):
    """
    Response schema for portfolio health analytics.
    """

    overall_health_score: float = Field(
        ...,
        ge=0,
        le=100,
        description="Overall portfolio health score.",
    )

    return_score: float = Field(
        ...,
        ge=0,
        le=100,
        description="Return quality score derived from expected annual return.",
    )

    risk_score: float = Field(
        ...,
        ge=0,
        le=100,
        description="Risk quality score derived from volatility and downside risk metrics.",
    )

    diversification_score: float = Field(
        ...,
        ge=0,
        le=100,
        description="Diversification score based on portfolio weight dispersion.",
    )

    concentration_score: float = Field(
        ...,
        ge=0,
        le=100,
        description="Concentration score based on the largest portfolio position.",
    )

    optimization_efficiency_score: float = Field(
        ...,
        ge=0,
        le=100,
        description=(
            "Portfolio efficiency score relative to the best Sharpe-ratio "
            "portfolio found during Monte Carlo simulation."
        ),
    )

    summary: str = Field(
        ...,
        description="High-level summary of portfolio health.",
    )

    recommendations: tuple[str, ...] = Field(
        ...,
        description="Actionable portfolio health recommendations.",
    )