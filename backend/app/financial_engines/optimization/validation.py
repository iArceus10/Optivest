"""
Shared validation utilities for portfolio optimization.

These functions validate numerical inputs before optimization problems
are passed to the CVXPY solver.
"""

from __future__ import annotations

import numpy as np
import pandas as pd


MIN_ASSETS = 2


def validate_expected_returns(
    expected_returns: pd.Series,
) -> None:
    """
    Validate expected annual returns.

    Raises
    ------
    ValueError
        If the expected return vector is invalid.
    """

    if expected_returns.empty:
        raise ValueError(
            "Expected returns cannot be empty."
        )

    if len(expected_returns) < MIN_ASSETS:
        raise ValueError(
            "At least two assets are required."
        )

    if expected_returns.isna().any():
        raise ValueError(
            "Expected returns contain missing values."
        )


def validate_covariance_matrix(
    covariance_matrix: pd.DataFrame,
) -> None:
    """
    Validate an annualized covariance matrix.

    Raises
    ------
    ValueError
        If the covariance matrix is unsuitable for optimization.
    """

    if covariance_matrix.empty:
        raise ValueError(
            "Covariance matrix cannot be empty."
        )

    rows, columns = covariance_matrix.shape

    if rows != columns:
        raise ValueError(
            "Covariance matrix must be square."
        )

    if rows < MIN_ASSETS:
        raise ValueError(
            "At least two assets are required."
        )

    if covariance_matrix.isna().any().any():
        raise ValueError(
            "Covariance matrix contains missing values."
        )

    if not covariance_matrix.index.equals(
        covariance_matrix.columns
    ):
        raise ValueError(
            "Covariance matrix labels must match."
        )

    matrix = covariance_matrix.to_numpy(dtype=float)

    if not np.allclose(matrix, matrix.T):
        raise ValueError(
            "Covariance matrix must be symmetric."
        )


def validate_optimization_inputs(
    expected_returns: pd.Series,
    covariance_matrix: pd.DataFrame,
) -> None:
    """
    Validate optimization inputs.

    Raises
    ------
    ValueError
        If the expected returns and covariance matrix
        are incompatible.
    """

    validate_expected_returns(
        expected_returns,
    )

    validate_covariance_matrix(
        covariance_matrix,
    )

    if not expected_returns.index.equals(
        covariance_matrix.index
    ):
        raise ValueError(
            "Asset labels must match."
        )

    eigenvalues = np.linalg.eigvalsh(
        covariance_matrix.to_numpy(dtype=float)
    )

    tolerance = 1e-10

    if np.any(eigenvalues < -tolerance):
        raise ValueError(
            "Covariance matrix must be positive semidefinite."
        )