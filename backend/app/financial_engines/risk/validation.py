"""
Validation helpers for the Risk Analytics Financial Engine.

These functions validate historical return series before they are used
by portfolio risk metrics.

Validation is intentionally centralized to avoid duplication across
individual risk metric modules while remaining framework-independent.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

MIN_OBSERVATIONS = 2

DEFAULT_CONFIDENCE_LEVEL = 0.95


def validate_return_series(
    returns: pd.Series,
) -> pd.Series:
    """
    Validate and clean a portfolio return series.

    Parameters
    ----------
    returns:
        Historical portfolio returns.

    Returns
    -------
    pd.Series
        Cleaned return series suitable for risk analysis.

    Raises
    ------
    ValueError
        If the supplied returns are unsuitable for computation.
    """

    if returns.empty:
        raise ValueError(
            "Portfolio returns are empty."
        )

    cleaned_returns = returns.dropna()

    if cleaned_returns.empty:
        raise ValueError(
            "Portfolio returns contain no usable observations."
        )

    if len(cleaned_returns) < MIN_OBSERVATIONS:
        raise ValueError(
            "At least two observations are required for risk analysis."
        )

    if not pd.api.types.is_numeric_dtype(
        cleaned_returns.dtype
    ):
        raise ValueError(
            "Portfolio returns must contain only numeric values."
        )

    values = cleaned_returns.to_numpy(dtype=float)

    if not np.isfinite(values).all():
        raise ValueError(
            "Portfolio returns contain non-finite values."
        )

    return cleaned_returns


def validate_risk_free_rate(
    risk_free_rate: float,
) -> None:
    """
    Validate the annual risk-free rate.
    """

    if not np.isfinite(risk_free_rate):
        raise ValueError(
            "Risk-free rate must be a finite number."
        )


def validate_confidence_level(
    confidence_level: float,
) -> None:
    """
    Validate the confidence level used by VaR and CVaR.

    The confidence level must lie strictly between zero and one.
    """

    if not np.isfinite(confidence_level):
        raise ValueError(
            "Confidence level must be a finite number."
        )

    if not 0.0 < confidence_level < 1.0:
        raise ValueError(
            "Confidence level must be between 0 and 1."
        )


def validate_risk_inputs(
    returns: pd.Series,
    *,
    risk_free_rate: float,
    confidence_level: float,
) -> pd.Series:
    """
    Perform complete validation for risk analytics inputs.
    """

    cleaned_returns = validate_return_series(
        returns
    )

    validate_risk_free_rate(
        risk_free_rate
    )

    validate_confidence_level(
        confidence_level
    )

    return cleaned_returns