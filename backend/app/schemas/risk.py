from __future__ import annotations

from datetime import date

from pydantic import BaseModel, ConfigDict, Field

from app.financial_engines.risk.ratios import (
    DEFAULT_RISK_FREE_RATE,
)
from app.financial_engines.risk.validation import (
    DEFAULT_CONFIDENCE_LEVEL,
)


class RiskAnalyticsRequest(BaseModel):
    """
    Request for portfolio risk analytics.
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
        description="Annual risk-free rate.",
    )

    confidence_level: float = Field(
        default=DEFAULT_CONFIDENCE_LEVEL,
        gt=0,
        lt=1,
        description="Confidence level for VaR and CVaR.",
    )


class RiskAnalyticsResponse(BaseModel):
    """
    Portfolio risk analytics response.
    """

    sharpe_ratio: float = Field(
        ...,
        description="Annualized Sharpe Ratio.",
    )

    sortino_ratio: float = Field(
        ...,
        description="Annualized Sortino Ratio.",
    )

    maximum_drawdown: float = Field(
        ...,
        ge=0,
        le=1,
        description="Maximum historical drawdown.",
    )

    value_at_risk: float = Field(
        ...,
        ge=0,
        description="Historical Value-at-Risk.",
    )

    conditional_value_at_risk: float = Field(
        ...,
        ge=0,
        description="Historical Conditional Value-at-Risk.",
    )