from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from app.financial_engines.optimization.mean_variance import (
    optimize_mean_variance,
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


def test_optimize_mean_variance_returns_series():
    weights = optimize_mean_variance(
        sample_expected_returns(),
        sample_covariance_matrix(),
    )

    assert isinstance(weights, pd.Series)


def test_optimize_mean_variance_preserves_asset_order():
    weights = optimize_mean_variance(
        sample_expected_returns(),
        sample_covariance_matrix(),
    )

    assert list(weights.index) == [
        "AAPL",
        "MSFT",
        "NVDA",
    ]


def test_optimize_mean_variance_weights_sum_to_one():
    weights = optimize_mean_variance(
        sample_expected_returns(),
        sample_covariance_matrix(),
    )

    assert np.isclose(
        weights.sum(),
        1.0,
    )


def test_optimize_mean_variance_produces_long_only_weights():
    weights = optimize_mean_variance(
        sample_expected_returns(),
        sample_covariance_matrix(),
    )

    assert np.all(weights >= -1e-6)


def test_optimize_mean_variance_rejects_invalid_risk_aversion():
    with pytest.raises(ValueError):
        optimize_mean_variance(
            sample_expected_returns(),
            sample_covariance_matrix(),
            risk_aversion=0,
        )


def test_higher_risk_aversion_changes_solution():
    conservative = optimize_mean_variance(
        sample_expected_returns(),
        sample_covariance_matrix(),
        risk_aversion=10.0,
    )

    aggressive = optimize_mean_variance(
        sample_expected_returns(),
        sample_covariance_matrix(),
        risk_aversion=0.2,
    )

    assert not np.allclose(
        conservative.values,
        aggressive.values,
    )


def test_optimize_mean_variance_returns_named_series():
    weights = optimize_mean_variance(
        sample_expected_returns(),
        sample_covariance_matrix(),
    )

    assert weights.name == "weight"