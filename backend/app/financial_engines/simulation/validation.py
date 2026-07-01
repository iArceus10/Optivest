"""
Shared validation utilities for Monte Carlo portfolio simulation.

These functions validate numerical inputs before simulation begins.
"""

from __future__ import annotations

import math

import numpy as np
import pandas as pd

from app.financial_engines.optimization.validation import (
    validate_optimization_inputs,
)


def validate_simulation_count(
    simulation_count: int,
) -> None:
    """
    Validate the requested number of simulations.

    Raises
    ------
    ValueError
        If the simulation count is invalid.
    """

    if simulation_count <= 0:
        raise ValueError(
            "Simulation count must be greater than zero."
        )


def validate_risk_free_rate(
    risk_free_rate: float,
) -> None:
    """
    Validate the annual risk-free rate.

    Raises
    ------
    ValueError
        If the supplied risk-free rate is not finite.
    """

    if not math.isfinite(risk_free_rate):
        raise ValueError(
            "Risk-free rate must be a finite number."
        )


def validate_random_seed(
    seed: int | None,
) -> None:
    """
    Validate the random seed.

    Raises
    ------
    ValueError
        If the seed is invalid.
    """

    if seed is not None and not isinstance(seed, int):
        raise ValueError(
            "Random seed must be an integer or None."
        )


def validate_simulation_inputs(
    expected_returns: pd.Series,
    covariance_matrix: pd.DataFrame,
    *,
    simulation_count: int,
    risk_free_rate: float,
    seed: int | None,
) -> None:
    """
    Validate all Monte Carlo simulation inputs.

    Raises
    ------
    ValueError
        If any simulation input is invalid.
    """

    validate_optimization_inputs(
        expected_returns,
        covariance_matrix,
    )

    validate_simulation_count(
        simulation_count,
    )

    validate_risk_free_rate(
        risk_free_rate,
    )

    validate_random_seed(
        seed,
    )

    covariance = covariance_matrix.to_numpy(dtype=float)

    if not np.all(np.isfinite(covariance)):
        raise ValueError(
            "Covariance matrix contains non-finite values."
        )

    expected = expected_returns.to_numpy(dtype=float)

    if not np.all(np.isfinite(expected)):
        raise ValueError(
            "Expected returns contain non-finite values."
        )