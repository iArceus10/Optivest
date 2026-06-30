from __future__ import annotations

import numpy as np
import pandas as pd

from app.financial_engines.optimization.maximum_sharpe import (
    optimize_maximum_sharpe,
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


def test_optimize_maximum_sharpe_returns_series():
    weights = optimize_maximum_sharpe(
        sample_expected_returns(),
        sample_covariance_matrix(),
    )

    assert isinstance(weights, pd.Series)


def test_optimize_maximum_sharpe_preserves_asset_order():
    weights = optimize_maximum_sharpe(
        sample_expected_returns(),
        sample_covariance_matrix(),
    )

    assert list(weights.index) == [
        "AAPL",
        "MSFT",
        "NVDA",
    ]


def test_optimize_maximum_sharpe_weights_sum_to_one():
    weights = optimize_maximum_sharpe(
        sample_expected_returns(),
        sample_covariance_matrix(),
    )

    assert np.isclose(
        weights.sum(),
        1.0,
    )


def test_optimize_maximum_sharpe_is_long_only():
    weights = optimize_maximum_sharpe(
        sample_expected_returns(),
        sample_covariance_matrix(),
    )

    assert np.all(weights >= -1e-6)


def test_optimize_maximum_sharpe_returns_named_series():
    weights = optimize_maximum_sharpe(
        sample_expected_returns(),
        sample_covariance_matrix(),
    )

    assert weights.name == "weight"


def test_higher_risk_free_rate_changes_solution():
    low_rf = optimize_maximum_sharpe(
        sample_expected_returns(),
        sample_covariance_matrix(),
        risk_free_rate=0.01,
    )

    high_rf = optimize_maximum_sharpe(
        sample_expected_returns(),
        sample_covariance_matrix(),
        risk_free_rate=0.08,
    )

    assert not np.allclose(
        low_rf.values,
        high_rf.values,
    )


def test_maximum_sharpe_is_deterministic():
    first = optimize_maximum_sharpe(
        sample_expected_returns(),
        sample_covariance_matrix(),
    )

    second = optimize_maximum_sharpe(
        sample_expected_returns(),
        sample_covariance_matrix(),
    )

    assert np.allclose(
        first.values,
        second.values,
    )

def test_risk_free_rate_greater_than_all_expected_returns():
    returns = pd.Series(
        [0.02, 0.03, 0.04],
        index=["AAPL", "MSFT", "NVDA"],
    )

    weights = optimize_maximum_sharpe(
        returns,
        sample_covariance_matrix(),
        risk_free_rate=0.10,
    )

    assert np.isclose(
        weights.sum(),
        1.0,
    )

    assert (weights >= -1e-10).all()