"""
Covariance matrix calculations.

The covariance matrix captures how asset returns move together and forms the
foundation of Modern Portfolio Theory (MPT). It is the primary input for
portfolio volatility, mean-variance optimization, and efficient frontier
construction.

These functions are deterministic and framework-independent.
"""

from __future__ import annotations

import pandas as pd

from app.financial_engines.market_data.annualization import (
    TRADING_DAYS_PER_YEAR,
)
from app.financial_engines.statistics.validation import (
    validate_returns_data,
)


def calculate_daily_covariance_matrix(
    returns: pd.DataFrame,
) -> pd.DataFrame:
    """
    Calculate the sample covariance matrix of daily asset returns.
    """

    cleaned_returns = validate_returns_data(
        returns
    )

    covariance = cleaned_returns.cov()

    if covariance.empty:
        raise ValueError(
            "Unable to compute covariance matrix."
        )

    if covariance.isna().any().any():
        raise ValueError(
            "Covariance matrix contains invalid values."
        )

    return covariance


def calculate_annualized_covariance_matrix(
    returns: pd.DataFrame,
) -> pd.DataFrame:
    """
    Calculate the annualized covariance matrix.
    """

    daily_covariance = calculate_daily_covariance_matrix(
        returns
    )

    return daily_covariance * TRADING_DAYS_PER_YEAR