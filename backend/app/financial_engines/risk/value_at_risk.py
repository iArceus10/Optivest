"""
Historical Value-at-Risk (VaR) and Conditional Value-at-Risk (CVaR)
calculations.

These functions quantify downside tail risk using the empirical
distribution of historical portfolio returns.

The implementation is deterministic, framework-independent, and operates
purely on historical portfolio return series.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from app.financial_engines.risk.validation import (
    DEFAULT_CONFIDENCE_LEVEL,
    validate_confidence_level,
    validate_return_series,
)


def calculate_historical_value_at_risk(
    returns: pd.Series,
    *,
    confidence_level: float = DEFAULT_CONFIDENCE_LEVEL,
) -> float:
    """
    Compute Historical Value-at-Risk (VaR).

    Parameters
    ----------
    returns:
        Historical portfolio returns.

    confidence_level:
        Confidence level expressed as a decimal.

    Returns
    -------
    float
        Historical Value-at-Risk expressed as a positive loss.
    """

    cleaned_returns = validate_return_series(
        returns
    )

    validate_confidence_level(
        confidence_level
    )

    percentile = (
        1.0 - confidence_level
    ) * 100.0

    var_return = float(
        np.percentile(
            cleaned_returns.to_numpy(dtype=float),
            percentile,
        )
    )

    return max(
        0.0,
        -var_return,
    )


def calculate_historical_conditional_value_at_risk(
    returns: pd.Series,
    *,
    confidence_level: float = DEFAULT_CONFIDENCE_LEVEL,
) -> float:
    """
    Compute Historical Conditional Value-at-Risk (CVaR), also known as
    Expected Shortfall.

    Parameters
    ----------
    returns:
        Historical portfolio returns.

    confidence_level:
        Confidence level expressed as a decimal.

    Returns
    -------
    float
        Historical Conditional Value-at-Risk expressed as a positive
        loss.
    """

    cleaned_returns = validate_return_series(
        returns
    )

    validate_confidence_level(
        confidence_level
    )

    var = calculate_historical_value_at_risk(
        cleaned_returns,
        confidence_level=confidence_level,
    )

    loss_threshold = -var

    tail_losses = cleaned_returns[
        cleaned_returns <= loss_threshold
    ]

    if tail_losses.empty:
        return var

    return max(
        0.0,
        -float(
            tail_losses.mean()
        ),
    )