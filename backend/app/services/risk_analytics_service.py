from __future__ import annotations

from datetime import date

import pandas as pd

from app.financial_engines.risk import (
    calculate_risk_metrics,
)
from app.financial_engines.risk.models import (
    RiskAnalyticsResult,
)
from app.financial_engines.risk.validation import (
    DEFAULT_CONFIDENCE_LEVEL,
)
from app.services.market_data_service import (
    MarketDataService,
)


class RiskAnalyticsService:
    """
    Service responsible for orchestrating portfolio risk analytics.

    Responsibilities
    ----------------
    * Perform business-level validation.
    * Retrieve historical market data.
    * Prepare portfolio return series.
    * Delegate all financial computations to the Risk Analytics
      Financial Engine.

    This service intentionally performs no financial calculations.
    """

    @staticmethod
    def _prepare_portfolio_returns(
        tickers: list[str],
        weights: list[float],
        *,
        start: date,
        end: date,
    ) -> pd.Series:
        """
        Retrieve historical asset returns and construct the historical
        portfolio return series.
        """

        if not tickers:
            raise ValueError(
                "At least one ticker must be provided."
            )

        if len(tickers) != len(weights):
            raise ValueError(
                "Number of weights must match number of tickers."
            )

        daily_returns = (
            MarketDataService.get_daily_returns(
                tickers=tickers,
                start=start,
                end=end,
            )
        )

        weight_series = pd.Series(
            weights,
            index=daily_returns.columns,
            dtype=float,
        )

        return daily_returns @ weight_series

    @staticmethod
    def analyze_portfolio_risk(
        tickers: list[str],
        weights: list[float],
        *,
        start: date,
        end: date,
        risk_free_rate: float = 0.02,
        confidence_level: float = DEFAULT_CONFIDENCE_LEVEL,
    ) -> RiskAnalyticsResult:
        """
        Compute portfolio risk analytics.
        """

        portfolio_returns = (
            RiskAnalyticsService._prepare_portfolio_returns(
                tickers,
                weights,
                start=start,
                end=end,
            )
        )

        return calculate_risk_metrics(
            portfolio_returns,
            risk_free_rate=risk_free_rate,
            confidence_level=confidence_level,
        )