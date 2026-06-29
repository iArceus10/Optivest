"""
Expected return calculations.

These functions operate purely on historical daily returns and contain no
application-specific or framework-specific logic.

The outputs produced here become direct inputs to portfolio optimization,
Monte Carlo simulation, and risk analytics.
"""

from __future__ import annotations

import pandas as pd

from app.financial_engines.market_data.annualization import (
    annualize_mean_return,
)
from app.financial_engines.statistics.validation import (
    validate_returns_data,
)


def calculate_mean_daily_returns(
    returns: pd.DataFrame,
) -> pd.Series:
    """
    Calculate the historical mean daily return for each asset.
    """

    cleaned_returns = validate_returns_data(
        returns
    )

    mean_returns = cleaned_returns.mean()

    if mean_returns.isna().any():
        raise ValueError(
            "Unable to compute mean daily returns."
        )

    return mean_returns


def calculate_expected_annual_returns(
    returns: pd.DataFrame,
) -> pd.Series:
    """
    Calculate the annualized expected return for each asset.
    """

    mean_daily_returns = calculate_mean_daily_returns(
        returns
    )

    return mean_daily_returns.apply(
        annualize_mean_return
    )