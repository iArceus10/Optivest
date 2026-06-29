"""
Internal utilities shared by portfolio optimization engines.

This module is intentionally private to the optimization package.
"""

from __future__ import annotations

import cvxpy as cp
import numpy as np


def create_weight_variable(
    number_of_assets: int,
) -> cp.Variable:
    """
    Create the optimization variable representing portfolio weights.
    """

    return cp.Variable(number_of_assets)


def create_long_only_constraints(
    weights: cp.Variable,
) -> list[cp.Constraint]:
    """
    Create long-only constraints.
    """

    return [
        weights >= 0,
    ]


def create_fully_invested_constraint(
    weights: cp.Variable,
) -> cp.Constraint:
    """
    Create the fully invested portfolio constraint.

    The portfolio weights must sum to one.
    """

    return cp.sum(weights) == 1


def solve_problem(
    weights: cp.Variable,
    objective: cp.Minimize | cp.Maximize,
    constraints: list[cp.Constraint],
) -> np.ndarray:
    """
    Solve a convex optimization problem and return the optimal
    portfolio weights.

    Parameters
    ----------
    weights:
        CVXPY optimization variable representing portfolio weights.

    objective:
        Optimization objective.

    constraints:
        Constraints applied to the optimization problem.

    Returns
    -------
    np.ndarray
        Optimal portfolio weights.
    """

    problem = cp.Problem(
        objective,
        constraints,
    )

    problem.solve()

    if problem.status not in (
        cp.OPTIMAL,
        cp.OPTIMAL_INACCURATE,
    ):
        raise ValueError(
            f"Optimization failed: {problem.status}"
        )

    if weights.value is None:
        raise ValueError(
            "Optimization produced no solution."
        )

    optimal_weights = np.asarray(
        weights.value,
        dtype=float,
    )

    optimal_weights = np.where(
        np.abs(optimal_weights) < 1e-12,
        0.0,
        optimal_weights,
    )

    return optimal_weights
    