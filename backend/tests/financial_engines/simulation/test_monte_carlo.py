from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from app.financial_engines.simulation.monte_carlo import (
    DEFAULT_RISK_FREE_RATE,
    run_monte_carlo_simulation,
)


@pytest.fixture
def expected_returns() -> pd.Series:
    return pd.Series(
        [0.10, 0.15, 0.20],
        index=["AAPL", "MSFT", "NVDA"],
    )


@pytest.fixture
def covariance_matrix() -> pd.DataFrame:
    return pd.DataFrame(
        [
            [0.040, 0.010, 0.008],
            [0.010, 0.090, 0.015],
            [0.008, 0.015, 0.160],
        ],
        index=["AAPL", "MSFT", "NVDA"],
        columns=["AAPL", "MSFT", "NVDA"],
    )


def test_simulation_returns_requested_number_of_portfolios(
    expected_returns: pd.Series,
    covariance_matrix: pd.DataFrame,
) -> None:
    result = run_monte_carlo_simulation(
        expected_returns,
        covariance_matrix,
        simulation_count=250,
        seed=42,
    )

    assert len(result.portfolios) == 250


def test_portfolio_weights_are_normalized(
    expected_returns: pd.Series,
    covariance_matrix: pd.DataFrame,
) -> None:
    result = run_monte_carlo_simulation(
        expected_returns,
        covariance_matrix,
        simulation_count=100,
        seed=42,
    )

    for portfolio in result.portfolios:
        assert np.isclose(
            portfolio.weights.sum(),
            1.0,
        )

        assert (portfolio.weights >= 0).all()


def test_simulation_is_deterministic(
    expected_returns: pd.Series,
    covariance_matrix: pd.DataFrame,
) -> None:
    first = run_monte_carlo_simulation(
        expected_returns,
        covariance_matrix,
        simulation_count=100,
        seed=123,
    )

    second = run_monte_carlo_simulation(
        expected_returns,
        covariance_matrix,
        simulation_count=100,
        seed=123,
    )

    assert len(first.portfolios) == len(second.portfolios)

    for portfolio_a, portfolio_b in zip(
        first.portfolios,
        second.portfolios,
    ):
        np.testing.assert_allclose(
            portfolio_a.weights.to_numpy(),
            portfolio_b.weights.to_numpy(),
        )

        assert portfolio_a.expected_return == pytest.approx(
            portfolio_b.expected_return
        )

        assert portfolio_a.volatility == pytest.approx(
            portfolio_b.volatility
        )

        assert portfolio_a.sharpe_ratio == pytest.approx(
            portfolio_b.sharpe_ratio
        )


def test_different_seeds_produce_different_results(
    expected_returns: pd.Series,
    covariance_matrix: pd.DataFrame,
) -> None:
    first = run_monte_carlo_simulation(
        expected_returns,
        covariance_matrix,
        simulation_count=10,
        seed=1,
    )

    second = run_monte_carlo_simulation(
        expected_returns,
        covariance_matrix,
        simulation_count=10,
        seed=2,
    )

    assert not np.allclose(
        first.portfolios[0].weights.to_numpy(),
        second.portfolios[0].weights.to_numpy(),
    )


def test_best_sharpe_is_maximum(
    expected_returns: pd.Series,
    covariance_matrix: pd.DataFrame,
) -> None:
    result = run_monte_carlo_simulation(
        expected_returns,
        covariance_matrix,
        simulation_count=500,
        seed=42,
    )

    maximum = max(
        portfolio.sharpe_ratio
        for portfolio in result.portfolios
    )

    assert result.best_sharpe.sharpe_ratio == pytest.approx(
        maximum
    )


def test_minimum_volatility_is_minimum(
    expected_returns: pd.Series,
    covariance_matrix: pd.DataFrame,
) -> None:
    result = run_monte_carlo_simulation(
        expected_returns,
        covariance_matrix,
        simulation_count=500,
        seed=42,
    )

    minimum = min(
        portfolio.volatility
        for portfolio in result.portfolios
    )

    assert result.minimum_volatility.volatility == pytest.approx(
        minimum
    )


def test_returns_are_within_asset_return_bounds(
    expected_returns: pd.Series,
    covariance_matrix: pd.DataFrame,
) -> None:
    result = run_monte_carlo_simulation(
        expected_returns,
        covariance_matrix,
        simulation_count=100,
        seed=42,
    )

    minimum = expected_returns.min()
    maximum = expected_returns.max()

    for portfolio in result.portfolios:
        assert minimum <= portfolio.expected_return <= maximum


def test_zero_risk_free_rate(
    expected_returns: pd.Series,
    covariance_matrix: pd.DataFrame,
) -> None:
    result = run_monte_carlo_simulation(
        expected_returns,
        covariance_matrix,
        simulation_count=50,
        risk_free_rate=0.0,
        seed=42,
    )

    assert len(result.portfolios) == 50


def test_default_risk_free_rate(
    expected_returns: pd.Series,
    covariance_matrix: pd.DataFrame,
) -> None:
    result = run_monte_carlo_simulation(
        expected_returns,
        covariance_matrix,
        simulation_count=10,
        seed=42,
    )

    assert DEFAULT_RISK_FREE_RATE == 0.02
    assert len(result.portfolios) == 10