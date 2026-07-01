from __future__ import annotations

from datetime import date

from app.financial_engines.simulation.monte_carlo import (
    DEFAULT_RISK_FREE_RATE,
    DEFAULT_SIMULATION_COUNT,
    run_monte_carlo_simulation,
)
from app.financial_engines.simulation.models import (
    MonteCarloSimulationResult,
)
from app.financial_engines.statistics.covariance import (
    calculate_annualized_covariance_matrix,
)
from app.financial_engines.statistics.expected_returns import (
    calculate_expected_annual_returns,
)
from app.services.market_data_service import MarketDataService

import pandas as pd


class SimulationService:
    """
    Service responsible for orchestrating Monte Carlo portfolio
    simulation.

    Responsibilities
    ----------------
    * Perform business-level validation.
    * Retrieve historical market data.
    * Prepare simulation inputs.
    * Delegate simulation to the Financial Engine.

    This service intentionally performs no mathematical computation.
    """

    def _prepare_simulation_inputs(
        tickers: list[str],
        *,
        start: date,
        end: date,
    ) -> tuple[pd.Series, pd.DataFrame]:
        """
        Retrieve historical returns and prepare simulation inputs.

        Returns
        -------
        tuple[pd.Series, pd.DataFrame]
            Annualized expected returns and covariance matrix.
        """

        if not tickers:
            raise ValueError(
                "At least one ticker must be provided."
            )

        returns = MarketDataService.get_daily_returns(
            tickers=tickers,
            start=start,
            end=end,
        )

        expected_returns = calculate_expected_annual_returns(
            returns
        )

        covariance_matrix = (
            calculate_annualized_covariance_matrix(
                returns
            )
        )

        return (
            expected_returns,
            covariance_matrix,
        )

    @staticmethod
    def run_simulation(
        tickers: list[str],
        *,
        start: date,
        end: date,
        simulation_count: int = DEFAULT_SIMULATION_COUNT,
        risk_free_rate: float = DEFAULT_RISK_FREE_RATE,
        seed: int | None = None,
    ) -> MonteCarloSimulationResult:
        """
        Execute Monte Carlo portfolio simulation.
        """

        (
            expected_returns,
            covariance_matrix,
        ) = (
            SimulationService._prepare_simulation_inputs(
                tickers,
                start=start,
                end=end,
            )
        )

        return run_monte_carlo_simulation(
            expected_returns,
            covariance_matrix,
            simulation_count=simulation_count,
            risk_free_rate=risk_free_rate,
            seed=seed,
        )