"""
Mean-Variance portfolio optimization.

Implements the classical Markowitz optimization framework using CVXPY.
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


DEFAULT_RISK_AVERSION = 1.0


def optimize_mean_variance(
    expected_returns: pd.Series,
    covariance_matrix: pd.DataFrame,
    *,
    risk_aversion: float = DEFAULT_RISK_AVERSION,
) -> pd.Series:
    """
    Compute the optimal portfolio using the classical
    Mean-Variance optimization framework.

    Parameters
    ----------
    expected_returns:
        Annualized expected returns for each asset.

    covariance_matrix:
        Annualized covariance matrix.

    risk_aversion:
        Investor risk-aversion coefficient.
        Higher values produce more conservative portfolios.

    Returns
    -------
    pd.Series
        Optimal portfolio weights indexed by asset ticker.
    """

    validate_optimization_inputs(
        expected_returns,
        covariance_matrix,
    )

    if risk_aversion <= 0:
        raise ValueError(
            "Risk aversion must be greater than zero."
        )

    asset_index = expected_returns.index.copy()

    weights = create_weight_variable(
        len(expected_returns)
    )

    expected_return = expected_returns.to_numpy()

    covariance = covariance_matrix.to_numpy()

    objective = cp.Maximize(
        expected_return @ weights
        - risk_aversion * cp.quad_form(
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