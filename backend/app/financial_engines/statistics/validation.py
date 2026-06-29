"""
Validation helpers for statistical computations.

These functions validate historical return matrices before they are used
by portfolio statistics, optimization, and risk analytics algorithms.

The validation logic is intentionally centralized to avoid duplication
across statistical engines while remaining framework-independent.
"""

from __future__ import annotations

import pandas as pd

MIN_OBSERVATIONS = 2


def validate_returns_data(
    returns: pd.DataFrame,
) -> pd.DataFrame:
    """
    Validate and clean a daily returns DataFrame.

    Parameters
    ----------
    returns:
        Daily percentage returns where each column represents an asset.

    Returns
    -------
    pd.DataFrame
        Cleaned returns DataFrame suitable for statistical analysis.

    Raises
    ------
    ValueError
        If the supplied returns are unsuitable for computation.
    """

    if returns.empty:
        raise ValueError(
            "Daily returns data is empty."
        )

    cleaned_returns = returns.dropna(how="any")

    if cleaned_returns.empty:
        raise ValueError(
            "Daily returns contain no usable observations."
        )

    if cleaned_returns.shape[0] < MIN_OBSERVATIONS:
        raise ValueError(
            "At least two observations are required for statistical analysis."
        )

    if not all(
        pd.api.types.is_numeric_dtype(dtype)
        for dtype in cleaned_returns.dtypes
    ):
        raise ValueError(
            "Daily returns must contain only numeric values."
        )

    return cleaned_returns