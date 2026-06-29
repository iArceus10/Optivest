"""
Validation helpers for market data.

These functions ensure downstream numerical algorithms receive valid,
well-formed historical price data.
"""

from __future__ import annotations

import pandas as pd


MIN_OBSERVATIONS = 2


def validate_price_data(
    prices: pd.DataFrame,
) -> None:
    """
    Validate a historical price DataFrame.

    Raises
    ------
    ValueError
        If the supplied market data is unsuitable for financial analysis.
    """

    if prices.empty:
        raise ValueError("Historical price data is empty.")

    if prices.shape[0] < MIN_OBSERVATIONS:
        raise ValueError(
            "Insufficient historical observations."
        )

    if prices.isna().all().all():
        raise ValueError(
            "Historical price data contains only missing values."
        )

    if prices.dropna(how="all").empty:
        raise ValueError(
            "Historical price data contains no usable observations."
        )