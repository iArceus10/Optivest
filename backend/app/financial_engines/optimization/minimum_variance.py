"""
Minimum Variance Portfolio optimization.
"""

from __future__ import annotations

import cvxpy as cp
import pandas as pd

from ._base import (
    create_long_only_constraints,
    create_weight_variable,
    solve_problem,
    create_fully_invested_constraint,
)
from .validation import validate_optimization_inputs


def optimize_minimum_variance(
    expected_returns: pd.Series,
    covariance_matrix: pd.DataFrame,
) -> pd.Series:
    """
    Compute the long-only minimum variance portfolio.

    Parameters
    ----------
    expected_returns:
        Annualized expected returns.

    covariance_matrix:
        Annualized covariance matrix.

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

    weights = create_weight_variable(
        len(expected_returns)
    )

    covariance = covariance_matrix.to_numpy()

    objective = cp.Minimize(
        cp.quad_form(
            weights,
            covariance,
        )
    )

    constraints = [
        create_fully_invested_constraint(weights),
        *create_long_only_constraints(weights),
    ]

    optimal_weights = solve_problem(
        weights,
        objective,
        constraints,
    )

    return pd.Series(
        optimal_weights,
        index=asset_index,
        name="weight",
    )