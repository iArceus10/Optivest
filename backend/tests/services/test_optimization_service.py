from datetime import date

import numpy as np
import pandas as pd
import pytest

from app.financial_engines.optimization.efficient_frontier import (
    EfficientFrontierPoint,
)
from app.services.market_data_service import MarketDataService
from app.services.optimization_service import OptimizationService


@pytest.fixture
def sample_returns() -> pd.DataFrame:
    """
    Sample daily returns for three assets.
    """

    return pd.DataFrame(
        {
            "AAPL": [
                0.010,
                0.020,
                -0.010,
                0.015,
                0.005,
            ],
            "MSFT": [
                0.008,
                0.018,
                -0.005,
                0.010,
                0.004,
            ],
            "NVDA": [
                0.020,
                0.030,
                -0.015,
                0.025,
                0.010,
            ],
        }
    )


@pytest.fixture
def optimization_dates():
    """
    Common date range used throughout the tests.
    """

    return (
        date(2024, 1, 1),
        date(2025, 1, 1),
    )


def test_prepare_optimization_inputs(
    monkeypatch,
    sample_returns,
    optimization_dates,
):
    """
    Optimization inputs should be computed from daily returns.
    """

    start, end = optimization_dates

    monkeypatch.setattr(
        MarketDataService,
        "get_daily_returns",
        lambda **kwargs: sample_returns,
    )

    expected_returns, covariance = (
        OptimizationService._prepare_optimization_inputs(
            ["AAPL", "MSFT", "NVDA"],
            start=start,
            end=end,
        )
    )

    assert isinstance(expected_returns, pd.Series)
    assert isinstance(covariance, pd.DataFrame)

    assert list(expected_returns.index) == [
        "AAPL",
        "MSFT",
        "NVDA",
    ]

    assert covariance.shape == (3, 3)


def test_mean_variance_portfolio(
    monkeypatch,
    sample_returns,
    optimization_dates,
):
    """
    Mean-Variance optimization should produce a valid portfolio.
    """

    start, end = optimization_dates

    monkeypatch.setattr(
        MarketDataService,
        "get_daily_returns",
        lambda **kwargs: sample_returns,
    )

    weights = (
        OptimizationService.get_mean_variance_portfolio(
            ["AAPL", "MSFT", "NVDA"],
            start=start,
            end=end,
        )
    )

    assert isinstance(weights, pd.Series)
    assert np.isclose(weights.sum(), 1.0)
    assert (weights >= 0).all()


def test_minimum_variance_portfolio(
    monkeypatch,
    sample_returns,
    optimization_dates,
):
    """
    Minimum Variance optimization should produce a valid portfolio.
    """

    start, end = optimization_dates

    monkeypatch.setattr(
        MarketDataService,
        "get_daily_returns",
        lambda **kwargs: sample_returns,
    )

    weights = (
        OptimizationService.get_minimum_variance_portfolio(
            ["AAPL", "MSFT", "NVDA"],
            start=start,
            end=end,
        )
    )

    assert isinstance(weights, pd.Series)
    assert np.isclose(weights.sum(), 1.0)
    assert (weights >= 0).all()


def test_maximum_sharpe_portfolio(
    monkeypatch,
    sample_returns,
    optimization_dates,
):
    """
    Maximum Sharpe optimization should produce a valid portfolio.
    """

    start, end = optimization_dates

    monkeypatch.setattr(
        MarketDataService,
        "get_daily_returns",
        lambda **kwargs: sample_returns,
    )

    weights = (
        OptimizationService.get_maximum_sharpe_portfolio(
            ["AAPL", "MSFT", "NVDA"],
            start=start,
            end=end,
        )
    )

    assert isinstance(weights, pd.Series)
    assert np.isclose(weights.sum(), 1.0)
    assert (weights >= 0).all()


def test_generate_efficient_frontier(
    monkeypatch,
    sample_returns,
    optimization_dates,
):
    """
    Efficient Frontier generation should return the requested number
    of frontier points.
    """

    start, end = optimization_dates

    monkeypatch.setattr(
        MarketDataService,
        "get_daily_returns",
        lambda **kwargs: sample_returns,
    )

    frontier = (
        OptimizationService.get_efficient_frontier(
            ["AAPL", "MSFT", "NVDA"],
            start=start,
            end=end,
            num_points=10,
        )
    )

    assert len(frontier) == 10

    for point in frontier:
        assert isinstance(
            point,
            EfficientFrontierPoint,
        )

        assert isinstance(
            point.weights,
            pd.Series,
        )

        assert np.isclose(
            point.weights.sum(),
            1.0,
        )

        assert np.all(point.weights >= -1e-6)


def test_market_data_error_is_propagated(
    monkeypatch,
    optimization_dates,
):
    """
    Service should propagate business validation errors raised by
    MarketDataService.
    """

    start, end = optimization_dates

    def raise_error(**kwargs):
        raise ValueError("Invalid ticker.")

    monkeypatch.setattr(
        MarketDataService,
        "get_daily_returns",
        raise_error,
    )

    with pytest.raises(ValueError):
        OptimizationService.get_mean_variance_portfolio(
            ["INVALID"],
            start=start,
            end=end,
        )


def test_invalid_risk_aversion(
    monkeypatch,
    sample_returns,
    optimization_dates,
):
    """
    Invalid risk aversion should be propagated from the optimization
    engine.
    """

    start, end = optimization_dates

    monkeypatch.setattr(
        MarketDataService,
        "get_daily_returns",
        lambda **kwargs: sample_returns,
    )

    with pytest.raises(ValueError):
        OptimizationService.get_mean_variance_portfolio(
            ["AAPL", "MSFT", "NVDA"],
            start=start,
            end=end,
            risk_aversion=0,
        )


def test_invalid_frontier_points(
    monkeypatch,
    sample_returns,
    optimization_dates,
):
    """
    Invalid frontier size should be propagated.
    """

    start, end = optimization_dates

    monkeypatch.setattr(
        MarketDataService,
        "get_daily_returns",
        lambda **kwargs: sample_returns,
    )

    with pytest.raises(ValueError):
        OptimizationService.get_efficient_frontier(
            ["AAPL", "MSFT", "NVDA"],
            start=start,
            end=end,
            num_points=0,
        )