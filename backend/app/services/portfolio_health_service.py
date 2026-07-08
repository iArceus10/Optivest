from __future__ import annotations

from datetime import date
from typing import NamedTuple

from app.financial_engines.portfolio_health import (
    PortfolioHealthResult,
    analyze_portfolio_health,
)
from app.services.risk_analytics_service import (
    RiskAnalyticsService,
)
from app.services.simulation_service import (
    SimulationService,
)
from app.services.statistics_service import (
    StatisticsService,
)
from app.services.market_data_service import (
    MarketDataService,
)


class _PortfolioHealthInputs(NamedTuple):
    """
    Internal container for prepared portfolio health inputs.

    This type is intentionally private to the service layer and is not
    exposed outside the module.
    """

    expected_return: float
    volatility: float
    sharpe_ratio: float
    best_simulated_sharpe_ratio: float
    sortino_ratio: float
    maximum_drawdown: float
    value_at_risk: float
    conditional_value_at_risk: float


class PortfolioHealthService:
    """
    Service responsible for orchestrating portfolio health analysis.

    Responsibilities
    ----------------
    * Perform business-level validation.
    * Coordinate Statistics, Risk Analytics and Simulation services.
    * Prepare inputs for the Portfolio Health Financial Engine.
    * Delegate portfolio health evaluation to the Financial Engine.

    This service intentionally performs no financial calculations.
    """

    @staticmethod
    def _prepare_portfolio_health_inputs(
        tickers: list[str],
        weights: list[float],
        *,
        start: date,
        end: date,
        risk_free_rate: float,
        simulation_count: int,
        seed: int | None,
    ) -> _PortfolioHealthInputs:
        """
        Prepare all inputs required by the Portfolio Health Financial
        Engine.
        """

        if not tickers:
            raise ValueError(
                "At least one ticker must be provided."
            )

        if len(tickers) != len(weights):
            raise ValueError(
                "Number of weights must match number of tickers."
            )

        daily_returns = MarketDataService.get_daily_returns(
            tickers=tickers,
            start=start,
            end=end,
        )

        portfolio_expected_return = (
            StatisticsService.get_portfolio_expected_return_from_returns(
                daily_returns,
                weights,
            )
        )

        portfolio_volatility = (
            StatisticsService.get_portfolio_volatility_from_returns(
                daily_returns,
                weights,
            )
        )

        risk_result = (
            RiskAnalyticsService.analyze_portfolio_risk_from_returns(
                daily_returns,
                weights,
                risk_free_rate=risk_free_rate,
            )
        )

        simulation_result = (
            SimulationService.run_simulation_from_returns(
                daily_returns,
                simulation_count=simulation_count,
                risk_free_rate=risk_free_rate,
                seed=seed,
            )
        )
        
        return _PortfolioHealthInputs(
            expected_return=portfolio_expected_return,
            volatility=portfolio_volatility,
            sharpe_ratio=risk_result.sharpe_ratio,
            best_simulated_sharpe_ratio=(
                simulation_result.best_sharpe.sharpe_ratio
            ),
            sortino_ratio=risk_result.sortino_ratio,
            maximum_drawdown=risk_result.maximum_drawdown,
            value_at_risk=risk_result.value_at_risk,
            conditional_value_at_risk=(
                risk_result.conditional_value_at_risk
            ),
        )

    @staticmethod
    def analyze_portfolio_health(
        tickers: list[str],
        weights: list[float],
        *,
        start: date,
        end: date,
        risk_free_rate: float = 0.02,
        simulation_count: int = 10_000,
        seed: int | None = None,
    ) -> PortfolioHealthResult:
        """
        Analyze overall portfolio health.

        Parameters
        ----------
        tickers:
            Portfolio asset tickers.

        weights:
            Portfolio allocation weights.

        start:
            Historical data start date.

        end:
            Historical data end date.

        risk_free_rate:
            Annualized risk-free rate used for risk metrics and Monte
            Carlo simulation.

        simulation_count:
            Number of Monte Carlo portfolios to simulate.

        seed:
            Optional random seed for deterministic simulations.

        Returns
        -------
        PortfolioHealthResult
            Deterministic portfolio health diagnostics.
        """

        prepared_inputs = (
            PortfolioHealthService._prepare_portfolio_health_inputs(
                tickers=tickers,
                weights=weights,
                start=start,
                end=end,
                risk_free_rate=risk_free_rate,
                simulation_count=simulation_count,
                seed=seed,
            )
        )

        return analyze_portfolio_health(
            expected_return=prepared_inputs.expected_return,
            volatility=prepared_inputs.volatility,
            sharpe_ratio=prepared_inputs.sharpe_ratio,
            best_simulated_sharpe_ratio=(
                prepared_inputs.best_simulated_sharpe_ratio
            ),
            sortino_ratio=prepared_inputs.sortino_ratio,
            maximum_drawdown=prepared_inputs.maximum_drawdown,
            value_at_risk=prepared_inputs.value_at_risk,
            conditional_value_at_risk=(
                prepared_inputs.conditional_value_at_risk
            ),
            weights=weights,
        )