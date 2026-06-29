"""
Portfolio volatility calculations.

Portfolio volatility measures the annualized standard deviation of portfolio
returns. It is the primary risk metric used throughout Modern Portfolio
Theory (MPT).

These functions are deterministic, framework-independent, and reusable by
portfolio optimization, simulation, and risk analytics modules.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from app.financial_engines.statistics.covariance import (
    calculate_annualized_covariance_matrix,
)


def calculate_portfolio_volatility(
    returns: pd.DataFrame,
    weights: np.ndarray,
) -> float:
    """
    Calculate the annualized volatility of a portfolio.

    Parameters
    ----------
    returns:
        Daily asset returns.

    weights:
        Portfolio allocation weights.

    Returns
    -------
    float
        Annualized portfolio volatility.

    Raises
    ------
    ValueError
        If portfolio weights are invalid or incompatible with the
        supplied returns.
    """

    covariance_matrix = calculate_annualized_covariance_matrix(
        returns
    )

    weights = np.asarray(
        weights,
        dtype=float,
    )

    asset_count = covariance_matrix.shape[0]

    if weights.ndim != 1:
        raise ValueError(
            "Portfolio weights must be one-dimensional."
        )

    if len(weights) != asset_count:
        raise ValueError(
            "Number of portfolio weights must match the number of assets."
        )

    if np.isnan(weights).any():
        raise ValueError(
            "Portfolio weights contain NaN values."
        )

    if not np.isclose(
        weights.sum(),
        1.0,
        atol=1e-8,
    ):
        raise ValueError(
            "Portfolio weights must sum to 1."
        )

    portfolio_variance = float(
        weights.T @ covariance_matrix.values @ weights
    )

    # Numerical precision can produce extremely small negative
    # values (e.g. -1e-16). Clamp them to zero before taking the
    # square root.
    if portfolio_variance < 0:
        if np.isclose(
            portfolio_variance,
            0.0,
            atol=1e-12,
        ):
            portfolio_variance = 0.0
        else:
            raise ValueError(
                "Portfolio variance cannot be negative."
            )

    return float(
        np.sqrt(portfolio_variance)
    )