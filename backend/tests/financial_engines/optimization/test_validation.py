from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from app.financial_engines.optimization.validation import (
    validate_covariance_matrix,
    validate_expected_returns,
    validate_optimization_inputs,
)


def sample_expected_returns() -> pd.Series:
    return pd.Series(
        [0.12, 0.15, 0.18],
        index=["AAPL", "MSFT", "NVDA"],
    )


def sample_covariance_matrix() -> pd.DataFrame:
    return pd.DataFrame(
        [
            [0.040, 0.010, 0.015],
            [0.010, 0.050, 0.020],
            [0.015, 0.020, 0.060],
        ],
        index=["AAPL", "MSFT", "NVDA"],
        columns=["AAPL", "MSFT", "NVDA"],
    )


def test_validate_expected_returns_accepts_valid_series():
    validate_expected_returns(
        sample_expected_returns()
    )


def test_validate_expected_returns_rejects_empty_series():
    with pytest.raises(ValueError):
        validate_expected_returns(
            pd.Series(dtype=float)
        )


def test_validate_expected_returns_rejects_missing_values():
    returns = sample_expected_returns()

    returns.iloc[1] = np.nan

    with pytest.raises(ValueError):
        validate_expected_returns(returns)


def test_validate_covariance_matrix_accepts_valid_matrix():
    validate_covariance_matrix(
        sample_covariance_matrix()
    )


def test_validate_covariance_matrix_rejects_non_square_matrix():
    covariance = sample_covariance_matrix().iloc[:, :2]

    with pytest.raises(ValueError):
        validate_covariance_matrix(covariance)


def test_validate_covariance_matrix_rejects_missing_values():
    covariance = sample_covariance_matrix()

    covariance.iloc[0, 0] = np.nan

    with pytest.raises(ValueError):
        validate_covariance_matrix(covariance)


def test_validate_covariance_matrix_rejects_mismatched_labels():
    covariance = sample_covariance_matrix()

    covariance.columns = ["A", "B", "C"]

    with pytest.raises(ValueError):
        validate_covariance_matrix(covariance)


def test_validate_covariance_matrix_rejects_non_symmetric_matrix():
    covariance = sample_covariance_matrix()

    covariance.iloc[0, 1] = 0.90

    with pytest.raises(ValueError):
        validate_covariance_matrix(covariance)


def test_validate_optimization_inputs_accepts_valid_inputs():
    validate_optimization_inputs(
        sample_expected_returns(),
        sample_covariance_matrix(),
    )


def test_validate_optimization_inputs_rejects_label_mismatch():
    covariance = sample_covariance_matrix()

    covariance.index = ["X", "Y", "Z"]

    with pytest.raises(ValueError):
        validate_optimization_inputs(
            sample_expected_returns(),
            covariance,
        )


def test_validate_optimization_inputs_rejects_non_positive_semidefinite_matrix():
    covariance = pd.DataFrame(
        [
            [1.0, 2.0],
            [2.0, 1.0],
        ],
        index=["AAPL", "MSFT"],
        columns=["AAPL", "MSFT"],
    )

    returns = pd.Series(
        [0.10, 0.15],
        index=["AAPL", "MSFT"],
    )

    with pytest.raises(ValueError):
        validate_optimization_inputs(
            returns,
            covariance,
        )