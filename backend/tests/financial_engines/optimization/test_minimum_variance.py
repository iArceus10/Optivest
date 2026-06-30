from __future__ import annotations

import numpy as np
import pandas as pd

from app.financial_engines.optimization.minimum_variance import (
    optimize_minimum_variance,
)


def sample_expected_returns() -> pd.Series:
    return pd.Series(
        [0.10, 0.15, 0.20],
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


def test_optimize_minimum_variance_returns_series():
    weights = optimize_minimum_variance(
        sample_expected_returns(),
        sample_covariance_matrix(),
    )

    assert isinstance(weights, pd.Series)


def test_optimize_minimum_variance_preserves_asset_order():
    weights = optimize_minimum_variance(
        sample_expected_returns(),
        sample_covariance_matrix(),
    )

    assert list(weights.index) == [
        "AAPL",
        "MSFT",
        "NVDA",
    ]


def test_optimize_minimum_variance_weights_sum_to_one():
    weights = optimize_minimum_variance(
        sample_expected_returns(),
        sample_covariance_matrix(),
    )

    assert np.isclose(
        weights.sum(),
        1.0,
    )


def test_optimize_minimum_variance_is_long_only():
    weights = optimize_minimum_variance(
        sample_expected_returns(),
        sample_covariance_matrix(),
    )

    assert np.all(weights >= -1e-6)


def test_optimize_minimum_variance_returns_named_series():
    weights = optimize_minimum_variance(
        sample_expected_returns(),
        sample_covariance_matrix(),
    )

    assert weights.name == "weight"


def test_minimum_variance_is_deterministic():
    first = optimize_minimum_variance(
        sample_expected_returns(),
        sample_covariance_matrix(),
    )

    second = optimize_minimum_variance(
        sample_expected_returns(),
        sample_covariance_matrix(),
    )

    assert np.allclose(
        first.values,
        second.values,
    )