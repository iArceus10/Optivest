from __future__ import annotations

from datetime import date
from unittest.mock import patch

import pandas as pd
import pytest

from app.financial_engines.simulation.models import (
    MonteCarloPortfolio,
    MonteCarloSimulationResult,
)
from app.services.simulation_service import (
    SimulationService,
)


@pytest.fixture
def daily_returns() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "AAPL": [0.01, 0.02, -0.01],
            "MSFT": [0.02, 0.01, 0.00],
        }
    )


@pytest.fixture
def expected_returns() -> pd.Series:
    return pd.Series(
        [0.10, 0.15],
        index=["AAPL", "MSFT"],
    )


@pytest.fixture
def covariance_matrix() -> pd.DataFrame:
    return pd.DataFrame(
        [
            [0.04, 0.01],
            [0.01, 0.09],
        ],
        index=["AAPL", "MSFT"],
        columns=["AAPL", "MSFT"],
    )


@pytest.fixture
def simulation_result() -> MonteCarloSimulationResult:
    portfolio = MonteCarloPortfolio(
        expected_return=0.12,
        volatility=0.18,
        sharpe_ratio=0.56,
        weights=pd.Series(
            [0.4, 0.6],
            index=["AAPL", "MSFT"],
            name="weight",
        ),
    )

    return MonteCarloSimulationResult(
        portfolios=[portfolio],
        best_sharpe=portfolio,
        minimum_volatility=portfolio,
    )


def test_prepare_simulation_inputs(
    daily_returns: pd.DataFrame,
    expected_returns: pd.Series,
    covariance_matrix: pd.DataFrame,
) -> None:
    with (
        patch(
            "app.services.simulation_service.MarketDataService.get_daily_returns",
            return_value=daily_returns,
        ),
        patch(
            "app.services.simulation_service.calculate_expected_annual_returns",
            return_value=expected_returns,
        ),
        patch(
            "app.services.simulation_service.calculate_annualized_covariance_matrix",
            return_value=covariance_matrix,
        ),
    ):
        result = (
            SimulationService._prepare_simulation_inputs(
                ["AAPL", "MSFT"],
                start=date(2024, 1, 1),
                end=date(2024, 12, 31),
            )
        )

    assert result == (
        expected_returns,
        covariance_matrix,
    )


def test_prepare_simulation_inputs_empty_tickers() -> None:
    with pytest.raises(
        ValueError,
        match="At least one ticker must be provided.",
    ):
        SimulationService._prepare_simulation_inputs(
            [],
            start=date(2024, 1, 1),
            end=date(2024, 12, 31),
        )


def test_run_simulation(
    daily_returns: pd.DataFrame,
    expected_returns: pd.Series,
    covariance_matrix: pd.DataFrame,
    simulation_result: MonteCarloSimulationResult,
) -> None:
    with (
        patch(
            "app.services.simulation_service.MarketDataService.get_daily_returns",
            return_value=daily_returns,
        ),
        patch(
            "app.services.simulation_service.calculate_expected_annual_returns",
            return_value=expected_returns,
        ),
        patch(
            "app.services.simulation_service.calculate_annualized_covariance_matrix",
            return_value=covariance_matrix,
        ),
        patch(
            "app.services.simulation_service.run_monte_carlo_simulation",
            return_value=simulation_result,
        ) as simulation_mock,
    ):
        result = SimulationService.run_simulation(
            ["AAPL", "MSFT"],
            start=date(2024, 1, 1),
            end=date(2024, 12, 31),
            simulation_count=500,
            risk_free_rate=0.03,
            seed=42,
        )

    assert result is simulation_result

    simulation_mock.assert_called_once_with(
        expected_returns,
        covariance_matrix,
        simulation_count=500,
        risk_free_rate=0.03,
        seed=42,
    )