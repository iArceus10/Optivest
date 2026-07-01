"""
Maximum drawdown calculations.

Maximum Drawdown measures the largest peak-to-trough decline in the
portfolio value over the observed historical period.

The implementation is deterministic, framework-independent, and operates
purely on historical portfolio return series.
"""

from __future__ import annotations

import pandas as pd

from app.financial_engines.risk.validation import (
    validate_return_series,
)


def calculate_maximum_drawdown(
    returns: pd.Series,
) -> float:
    """
    Compute the historical Maximum Drawdown.

    Parameters
    ----------
    returns:
        Historical portfolio returns expressed as decimal returns.

    Returns
    -------
    float
        Maximum drawdown expressed as a positive decimal.
        For example, 0.25 represents a 25% drawdown.
    """

    cleaned_returns = validate_return_series(
        returns
    )

    cumulative_returns = (
        1.0 + cleaned_returns
    ).cumprod()

    running_peak = cumulative_returns.cummax()

    drawdowns = (
        cumulative_returns
        / running_peak
        - 1.0
    )

    return float(
        -drawdowns.min()
    )