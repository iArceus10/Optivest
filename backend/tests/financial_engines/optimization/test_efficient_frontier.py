from __future__ import annotations

import numpy as np
import pandas as pd

from app.financial_engines.optimization.efficient_frontier import (
    DEFAULT_FRONTIER_POINTS,
    EfficientFrontierPoint,
    generate_efficient_frontier,
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


def test_generate_efficient_frontier_returns_list():
    frontier = generate_efficient_frontier(
        sample_expected_returns(),
        sample_covariance_matrix(),
    )

    assert isinstance(frontier, list)


def test_generate_efficient_frontier_returns_expected_number_of_points():
    frontier = generate_efficient_frontier(
        sample_expected_returns(),
        sample_covariance_matrix(),
    )

    assert len(frontier) == DEFAULT_FRONTIER_POINTS


def test_frontier_contains_frontier_points():
    frontier = generate_efficient_frontier(
        sample_expected_returns(),
        sample_covariance_matrix(),
    )

    assert all(
        isinstance(point, EfficientFrontierPoint)
        for point in frontier
    )


def test_frontier_weights_are_fully_invested():
    frontier = generate_efficient_frontier(
        sample_expected_returns(),
        sample_covariance_matrix(),
    )

    for point in frontier:
        assert np.isclose(
            point.weights.sum(),
            1.0,
        )


def test_frontier_weights_are_long_only():
    frontier = generate_efficient_frontier(
        sample_expected_returns(),
        sample_covariance_matrix(),
    )

    for point in frontier:
        assert (point.weights >= -1e-10).all()


def test_frontier_preserves_asset_order():
    frontier = generate_efficient_frontier(
        sample_expected_returns(),
        sample_covariance_matrix(),
    )

    for point in frontier:
        assert list(point.weights.index) == [
            "AAPL",
            "MSFT",
            "NVDA",
        ]


def test_frontier_returns_are_non_decreasing():
    frontier = generate_efficient_frontier(
        sample_expected_returns(),
        sample_covariance_matrix(),
    )

    returns = [
        point.expected_return
        for point in frontier
    ]

    assert np.all(
        np.diff(returns) >= -1e-10
    )


def test_frontier_volatility_is_non_negative():
    frontier = generate_efficient_frontier(
        sample_expected_returns(),
        sample_covariance_matrix(),
    )

    for point in frontier:
        assert point.volatility >= 0.0


def test_custom_number_of_points():
    frontier = generate_efficient_frontier(
        sample_expected_returns(),
        sample_covariance_matrix(),
        num_points=10,
    )

    assert len(frontier) == 10


def test_single_frontier_point_when_returns_are_equal():
    returns = pd.Series(
        [0.10, 0.10, 0.10],
        index=["AAPL", "MSFT", "NVDA"],
    )

    frontier = generate_efficient_frontier(
        returns,
        sample_covariance_matrix(),
    )

    assert len(frontier) == 1