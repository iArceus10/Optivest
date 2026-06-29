from __future__ import annotations

from datetime import date

import pandas as pd

from app.financial_engines.market_data.market_data_engine import (
    MarketDataEngine,
)
from app.financial_engines.market_data.returns import (
    calculate_daily_returns,
)


class MarketDataService:
    """
    Service responsible for orchestrating market data retrieval.

    This service performs business-level validation and delegates all
    numerical computations to the Financial Engine.
    """

    @staticmethod
    def get_historical_prices(
        tickers: list[str],
        *,
        start: date,
        end: date,
    ) -> pd.DataFrame:
        """
        Retrieve historical adjusted close prices.
        """

        if not tickers:
            raise ValueError(
                "At least one ticker must be provided."
            )

        normalized_tickers = sorted(
            {
                ticker.strip().upper()
                for ticker in tickers
                if ticker.strip()
            }
        )

        if not normalized_tickers:
            raise ValueError(
                "Ticker list cannot be empty."
            )

        if start >= end:
            raise ValueError(
                "Start date must be earlier than end date."
            )

        return MarketDataEngine.get_adjusted_close_prices(
            normalized_tickers,
            start=start.isoformat(),
            end=end.isoformat(),
        )

    @staticmethod
    def get_daily_returns(
        tickers: list[str],
        *,
        start: date,
        end: date,
    ) -> pd.DataFrame:
        """
        Retrieve historical daily returns.
        """

        prices = MarketDataService.get_historical_prices(
            tickers,
            start=start,
            end=end,
        )

        return calculate_daily_returns(prices)