"""
Utilities for converting daily financial statistics into annualized values.

These functions are intentionally framework-independent and contain no
FastAPI, SQLAlchemy, or application-specific logic.
"""

from __future__ import annotations

TRADING_DAYS_PER_YEAR: int = 252


def annualize_mean_return(
    daily_mean_return: float,
) -> float:
    """
    Annualize an average daily return.

    Formula:
        annual_return = daily_mean_return × 252

    Parameters
    ----------
    daily_mean_return:
        Mean daily return expressed as a decimal.

    Returns
    -------
    float
        Annualized expected return.
    """
    return daily_mean_return * TRADING_DAYS_PER_YEAR


def annualize_volatility(
    daily_volatility: float,
) -> float:
    """
    Annualize daily volatility.

    Formula:
        annual_volatility = daily_volatility × √252

    Parameters
    ----------
    daily_volatility:
        Standard deviation of daily returns.

    Returns
    -------
    float
        Annualized volatility.
    """
    return daily_volatility * (TRADING_DAYS_PER_YEAR ** 0.5)