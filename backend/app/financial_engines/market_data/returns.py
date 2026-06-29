"""
Utilities for computing daily asset returns.
"""

from __future__ import annotations

import pandas as pd


def calculate_daily_returns(
    prices: pd.DataFrame,
) -> pd.DataFrame:
    """
    Compute percentage daily returns from adjusted closing prices.

    Parameters
    ----------
    prices:
        DataFrame whose columns represent tickers and whose rows represent
        historical adjusted close prices.

    Returns
    -------
    pd.DataFrame
        Daily percentage returns with missing values removed.
    """
    returns = prices.pct_change()

    return returns.dropna(how="any")