"""
Maximum Sharpe Ratio portfolio optimization.

Implements the tangency portfolio using a convex reformulation that is
compatible with CVXPY's Disciplined Convex Programming (DCP) rules.
"""

from __future__ import annotations

import cvxpy as cp
import pandas as pd

from ._base import (
    create_long_only_constraints,
    create_weight_variable,
    solve_problem,
)
from .validation import validate_optimization_inputs


DEFAULT_RISK_FREE_RATE = 0.02


def optimize_maximum_sharpe(
    expected_returns: pd.Series,
    covariance_matrix: pd.DataFrame,
    *,
    risk_free_rate: float = DEFAULT_RISK_FREE_RATE,
) -> pd.Series:
    """
    Compute the long-only Maximum Sharpe Ratio portfolio.

    Parameters
    ----------
    expected_returns:
        Annualized expected returns.

    covariance_matrix:
        Annualized covariance matrix.

    risk_free_rate:
        Annual risk-free rate expressed as a decimal.

    Returns
    -------
    pd.Series
        Optimal portfolio weights indexed by asset ticker.
    """

    validate_optimization_inputs(
        expected_returns,
        covariance_matrix,
    )

    asset_index = expected_returns.index.copy()

    excess_returns = (
        expected_returns - risk_free_rate
    ).to_numpy()

    covariance = covariance_matrix.to_numpy()

    weights = create_weight_variable(
        len(expected_returns)
    )

    objective = cp.Maximize(
        excess_returns @ weights
    )

    constraints = [
        *create_long_only_constraints(
            weights,
        ),
        cp.quad_form(
            weights,
            covariance,
        ) <= 1,
    ]

    scaled_weights = solve_problem(
        weights,
        objective,
        constraints,
    )

    weight_sum = scaled_weights.sum()

    if weight_sum <= 0:
        raise ValueError(
            "Optimization produced an invalid portfolio."
        )

    normalized_weights = (
        scaled_weights / weight_sum
    )

    return pd.Series(
        normalized_weights,
        index=asset_index,
        name="weight",
    )