"""
Correlation matrix calculations.

Correlation measures the strength and direction of linear relationships
between asset returns. Unlike covariance, correlation is normalized to the
range [-1, 1], making it useful for interpreting diversification.

These functions are deterministic and framework-independent.
"""

from __future__ import annotations

import pandas as pd

from app.financial_engines.statistics.validation import (
    validate_returns_data,
)


def calculate_correlation_matrix(
    returns: pd.DataFrame,
) -> pd.DataFrame:
    """
    Calculate the Pearson correlation matrix of daily asset returns.
    """

    cleaned_returns = validate_returns_data(
        returns
    )

    correlation = cleaned_returns.corr()

    if correlation.empty:
        raise ValueError(
            "Unable to compute correlation matrix."
        )

    if correlation.isna().any().any():
        raise ValueError(
            "Correlation matrix contains invalid values."
        )

    return correlation