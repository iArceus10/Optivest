from __future__ import annotations

from datetime import date
from unittest.mock import patch

import pandas as pd
import pytest

from app.financial_engines.portfolio_health.models import (
    PortfolioHealthResult,
)
from app.financial_engines.risk.models import (
    RiskAnalyticsResult,
)
from app.financial_engines.simulation.models import (
    MonteCarloPortfolio,
    MonteCarloSimulationResult,
)
from app.services.portfolio_health_service import (
    _PortfolioHealthInputs,
    PortfolioHealthService,
)


@pytest.fixture
def risk_result() -> RiskAnalyticsResult:
    return RiskAnalyticsResult(
        sharpe_ratio=1.25,
        sortino_ratio=1.70,
        maximum_drawdown=0.18,
        value_at_risk=0.06,
        conditional_value_at_risk=0.08,
    )


@pytest.fixture
def simulation_result() -> MonteCarloSimulationResult:
    best_portfolio = MonteCarloPortfolio(
        expected_return=0.18,
        volatility=0.14,
        sharpe_ratio=1.60,
        weights=pd.Series(
            {
                "AAPL": 0.5,
                "MSFT": 0.5,
            }
        ),
    )

    return MonteCarloSimulationResult(
        portfolios=[best_portfolio],
        best_sharpe=best_portfolio,
        minimum_volatility=best_portfolio,
    )


@pytest.fixture
def portfolio_health_result() -> PortfolioHealthResult:
    return PortfolioHealthResult(
        overall_health_score=85.0,
        return_score=75.0,
        risk_score=88.0,
        diversification_score=82.0,
        concentration_score=84.0,
        optimization_efficiency_score=78.0,
        summary="Strong portfolio with manageable risk.",
        recommendations=(
            "Maintain the current portfolio strategy.",
        ),
    )


def test_prepare_portfolio_health_inputs(
    risk_result: RiskAnalyticsResult,
    simulation_result: MonteCarloSimulationResult,
) -> None:
    with (
        patch(
            "app.services.portfolio_health_service."
            "StatisticsService.get_portfolio_expected_return",
            return_value=0.14,
        ),
        patch(
            "app.services.portfolio_health_service."
            "StatisticsService.get_portfolio_volatility",
            return_value=0.18,
        ),
        patch(
            "app.services.portfolio_health_service."
            "RiskAnalyticsService.analyze_portfolio_risk",
            return_value=risk_result,
        ),
        patch(
            "app.services.portfolio_health_service."
            "SimulationService.run_simulation",
            return_value=simulation_result,
        ),
    ):
        result = (
            PortfolioHealthService._prepare_portfolio_health_inputs(
                ["AAPL", "MSFT"],
                [0.4, 0.6],
                start=date(2024, 1, 1),
                end=date(2024, 12, 31),
                risk_free_rate=0.03,
                simulation_count=5000,
                seed=42,
            )
        )

    assert result == _PortfolioHealthInputs(
        expected_return=0.14,
        volatility=0.18,
        sharpe_ratio=1.25,
        best_simulated_sharpe_ratio=1.60,
        sortino_ratio=1.70,
        maximum_drawdown=0.18,
        value_at_risk=0.06,
        conditional_value_at_risk=0.08,
    )


def test_prepare_portfolio_health_inputs_empty_tickers() -> None:
    with pytest.raises(
        ValueError,
        match="At least one ticker must be provided.",
    ):
        PortfolioHealthService._prepare_portfolio_health_inputs(
            [],
            [],
            start=date(2024, 1, 1),
            end=date(2024, 12, 31),
            risk_free_rate=0.02,
            simulation_count=1000,
            seed=None,
        )


def test_prepare_portfolio_health_inputs_weight_mismatch() -> None:
    with pytest.raises(
        ValueError,
        match="Number of weights must match number of tickers.",
    ):
        PortfolioHealthService._prepare_portfolio_health_inputs(
            ["AAPL", "MSFT"],
            [1.0],
            start=date(2024, 1, 1),
            end=date(2024, 12, 31),
            risk_free_rate=0.02,
            simulation_count=1000,
            seed=None,
        )


def test_analyze_portfolio_health(
    portfolio_health_result: PortfolioHealthResult,
) -> None:
    prepared_inputs = _PortfolioHealthInputs(
        expected_return=0.14,
        volatility=0.18,
        sharpe_ratio=1.25,
        best_simulated_sharpe_ratio=1.60,
        sortino_ratio=1.70,
        maximum_drawdown=0.18,
        value_at_risk=0.06,
        conditional_value_at_risk=0.08,
    )

    with (
        patch(
            "app.services.portfolio_health_service."
            "PortfolioHealthService._prepare_portfolio_health_inputs",
            return_value=prepared_inputs,
        ),
        patch(
            "app.services.portfolio_health_service."
            "analyze_portfolio_health",
            return_value=portfolio_health_result,
        ) as engine_mock,
    ):
        result = (
            PortfolioHealthService.analyze_portfolio_health(
                ["AAPL", "MSFT"],
                [0.4, 0.6],
                start=date(2024, 1, 1),
                end=date(2024, 12, 31),
            )
        )

    assert result is portfolio_health_result

    engine_mock.assert_called_once_with(
        expected_return=0.14,
        volatility=0.18,
        sharpe_ratio=1.25,
        best_simulated_sharpe_ratio=1.60,
        sortino_ratio=1.70,
        maximum_drawdown=0.18,
        value_at_risk=0.06,
        conditional_value_at_risk=0.08,
        weights=[0.4, 0.6],
    )