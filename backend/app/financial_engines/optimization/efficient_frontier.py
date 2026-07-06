"""
Efficient Frontier generation.

Produces a collection of optimal portfolios spanning the range of
achievable expected returns under long-only constraints.
"""

from __future__ import annotations

import cvxpy as cp
import numpy as np
import pandas as pd

from ._base import (
    create_fully_invested_constraint,
    create_long_only_constraints,
    create_weight_variable,
    solve_problem,
)
from .models import EfficientFrontierPoint
from .validation import validate_optimization_inputs


DEFAULT_FRONTIER_POINTS = 50
WEIGHT_TOLERANCE = 1e-8


def _sanitize_long_only_weights(
    weights: np.ndarray,
    *,
    tolerance: float = WEIGHT_TOLERANCE,
) -> np.ndarray:
    """
    Clean solver-produced portfolio weights for long-only portfolios.

    CVXPY can return extremely small negative values (for example -1e-9)
    even when long-only constraints are imposed. Those values are numerical
    artifacts rather than economically meaningful short positions.

    This helper:
    1. clips tiny negative values to zero,
    2. raises if a materially negative weight is encountered,
    3. renormalizes weights so the final portfolio remains fully invested.
    """

    cleaned_weights = np.asarray(
        weights,
        dtype=float,
    ).copy()

    for index, weight in enumerate(cleaned_weights):
        if weight < 0:
            if abs(weight) <= tolerance:
                cleaned_weights[index] = 0.0
            else:
                raise ValueError(
                    "Efficient Frontier optimization produced a materially "
                    f"negative long-only weight: {weight}"
                )

    total_weight = float(cleaned_weights.sum())

    if np.isclose(total_weight, 0.0):
        raise ValueError(
            "Efficient Frontier optimization produced zero total weight."
        )

    cleaned_weights = cleaned_weights / total_weight

    return cleaned_weights


def _compute_frontier_point(
    expected_returns: pd.Series,
    covariance_matrix: pd.DataFrame,
    *,
    target_return: float,
) -> EfficientFrontierPoint:
    """
    Compute a single Efficient Frontier portfolio for the specified
    target return.
    """

    asset_index = expected_returns.index.copy()

    expected_return_vector = expected_returns.to_numpy()
    covariance = covariance_matrix.to_numpy()

    weights = create_weight_variable(len(expected_returns))

    objective = cp.Minimize(
        cp.quad_form(
            weights,
            covariance,
        )
    )

    constraints = [
        create_fully_invested_constraint(weights),
        *create_long_only_constraints(weights),
        expected_return_vector @ weights >= target_return,
    ]

    optimal_weights = solve_problem(
        weights,
        objective,
        constraints,
    )

    optimal_weights = _sanitize_long_only_weights(
        optimal_weights
    )

    portfolio_return = float(
        expected_return_vector @ optimal_weights
    )

    portfolio_variance = float(
        optimal_weights.T
        @ covariance
        @ optimal_weights
    )

    portfolio_variance = max(
        portfolio_variance,
        0.0,
    )

    portfolio_volatility = float(
        np.sqrt(portfolio_variance)
    )

    return EfficientFrontierPoint(
        expected_return=portfolio_return,
        volatility=portfolio_volatility,
        weights=pd.Series(
            optimal_weights,
            index=asset_index,
            name="weight",
        ),
    )


def generate_efficient_frontier(
    expected_returns: pd.Series,
    covariance_matrix: pd.DataFrame,
    *,
    num_points: int = DEFAULT_FRONTIER_POINTS,
) -> list[EfficientFrontierPoint]:
    """
    Generate an Efficient Frontier consisting of multiple optimal
    portfolios.

    Parameters
    ----------
    expected_returns:
        Annualized expected returns.

    covariance_matrix:
        Annualized covariance matrix.

    num_points:
        Number of portfolios to generate.

    Returns
    -------
    list[EfficientFrontierPoint]
        Efficient Frontier ordered by increasing expected return.
    """

    validate_optimization_inputs(
        expected_returns,
        covariance_matrix,
    )

    if num_points <= 0:
        raise ValueError(
            "Number of frontier points must be positive."
        )

    minimum_return = float(expected_returns.min())
    maximum_return = float(expected_returns.max())

    if np.isclose(
        minimum_return,
        maximum_return,
    ):
        return [
            _compute_frontier_point(
                expected_returns,
                covariance_matrix,
                target_return=minimum_return,
            )
        ]

    target_returns = np.linspace(
        minimum_return,
        maximum_return,
        num_points,
    )

    frontier: list[EfficientFrontierPoint] = []

    for target_return in target_returns:
        frontier.append(
            _compute_frontier_point(
                expected_returns,
                covariance_matrix,
                target_return=float(target_return),
            )
        )

    return frontier