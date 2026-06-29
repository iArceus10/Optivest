"""
Market Data Engine.

Responsible for retrieving and preprocessing historical market data.

This module is intentionally framework-independent.
"""

from __future__ import annotations

import pandas as pd
import yfinance as yf

from .validation import validate_price_data


class MarketDataEngine:
    """
    Retrieve historical adjusted close prices from Yahoo Finance.
    """

    @staticmethod
    def get_adjusted_close_prices(
        tickers: list[str],
        *,
        start: str,
        end: str,
    ) -> pd.DataFrame:
        """
        Download historical adjusted close prices.

        Parameters
        ----------
        tickers:
            List of ticker symbols.

        start:
            Inclusive start date.

        end:
            Exclusive end date.

        Returns
        -------
        pd.DataFrame
            Historical adjusted close prices indexed by trading date.
        """

        if not tickers:
            raise ValueError(
                "At least one ticker must be provided."
            )

        unique_tickers = sorted(set(tickers))

        data = yf.download(
            tickers=unique_tickers,
            start=start,
            end=end,
            progress=False,
            auto_adjust=True,
        )

        if data.empty:
            raise ValueError(
                "No market data returned from Yahoo Finance."
            )

        if len(unique_tickers) == 1:
            prices = data.loc[:, ["Close"]]
            prices.columns = unique_tickers
        else:
            prices = data["Close"]

        prices = prices.sort_index().dropna(how="all")

        validate_price_data(prices)

        return prices.sort_index()