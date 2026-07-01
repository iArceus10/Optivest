"""
Risk-adjusted performance ratio calculations.

These functions implement deterministic portfolio performance metrics
used to evaluate returns relative to risk.

The implementation is framework-independent and operates purely on
historical portfolio return series.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from app.financial_engines.market_data.annualization import (
    TRADING_DAYS_PER_YEAR,
)
from app.financial_engines.risk.validation import (
    DEFAULT_CONFIDENCE_LEVEL,
    validate_risk_inputs,
)

DEFAULT_RISK_FREE_RATE = 0.02


def calculate_sharpe_ratio(
    returns: pd.Series,
    *,
    risk_free_rate: float = DEFAULT_RISK_FREE_RATE,
) -> float:
    """
    Compute the annualized Sharpe Ratio.

    Parameters
    ----------
    returns:
        Historical portfolio returns.

    risk_free_rate:
        Annualized risk-free rate expressed as a decimal.

    Returns
    -------
    float
        Annualized Sharpe Ratio.
    """

    cleaned_returns = validate_risk_inputs(
        returns,
        risk_free_rate=risk_free_rate,
        confidence_level=DEFAULT_CONFIDENCE_LEVEL,
    )

    mean_daily_return = float(
        cleaned_returns.mean()
    )

    daily_volatility = float(
        cleaned_returns.std(ddof=1)
    )

    if np.isclose(
        daily_volatility,
        0.0,
    ):
        return 0.0

    annualized_return = (
        mean_daily_return
        * TRADING_DAYS_PER_YEAR
    )

    annualized_volatility = (
        daily_volatility
        * np.sqrt(TRADING_DAYS_PER_YEAR)
    )

    return (
        annualized_return
        - risk_free_rate
    ) / annualized_volatility


def calculate_sortino_ratio(
    returns: pd.Series,
    *,
    risk_free_rate: float = DEFAULT_RISK_FREE_RATE,
) -> float:
    """
    Compute the annualized Sortino Ratio.

    Only downside volatility contributes to the denominator.

    Parameters
    ----------
    returns:
        Historical portfolio returns.

    risk_free_rate:
        Annualized risk-free rate expressed as a decimal.

    Returns
    -------
    float
        Annualized Sortino Ratio.
    """

    cleaned_returns = validate_risk_inputs(
        returns,
        risk_free_rate=risk_free_rate,
        confidence_level=DEFAULT_CONFIDENCE_LEVEL,
    )

    mean_daily_return = float(
        cleaned_returns.mean()
    )

    annualized_return = (
        mean_daily_return
        * TRADING_DAYS_PER_YEAR
    )

    daily_risk_free_rate = (
        risk_free_rate
        / TRADING_DAYS_PER_YEAR
    )

    downside_returns = cleaned_returns[
        cleaned_returns < daily_risk_free_rate
    ]

    if downside_returns.empty:
        return 0.0

    downside_deviation = float(
        np.sqrt(
            (
                (
                    downside_returns
                    - daily_risk_free_rate
                ) ** 2
            ).mean()
        )
    )

    if np.isclose(
        downside_deviation,
        0.0,
    ):
        return 0.0

    annualized_downside_deviation = (
        downside_deviation
        * np.sqrt(TRADING_DAYS_PER_YEAR)
    )

    return (
        annualized_return
        - risk_free_rate
    ) / annualized_downside_deviation