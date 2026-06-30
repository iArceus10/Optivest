from __future__ import annotations

from datetime import date

import pandas as pd

from app.financial_engines.optimization.efficient_frontier import (
    DEFAULT_FRONTIER_POINTS,
)
from app.financial_engines.optimization.maximum_sharpe import (
    DEFAULT_RISK_FREE_RATE,
    optimize_maximum_sharpe,
)
from app.financial_engines.optimization.mean_variance import (
    DEFAULT_RISK_AVERSION,
    optimize_mean_variance,
)
from app.financial_engines.optimization.minimum_variance import (
    optimize_minimum_variance,
)
from app.financial_engines.optimization.models import (
    EfficientFrontierPoint,
)
from app.financial_engines.optimization.efficient_frontier import (
    generate_efficient_frontier,
)
from app.financial_engines.statistics.covariance import (
    calculate_annualized_covariance_matrix,
)
from app.financial_engines.statistics.expected_returns import (
    calculate_expected_annual_returns,
)
from app.services.market_data_service import MarketDataService


class OptimizationService:
    """
    Service responsible for orchestrating portfolio optimization.

    Responsibilities
    ----------------
    * Perform business-level validation.
    * Retrieve historical market data.
    * Prepare optimization inputs.
    * Delegate optimization to the Financial Engine.

    This service intentionally performs no mathematical optimization.
    """

    @staticmethod
    def _prepare_optimization_inputs(
        tickers: list[str],
        *,
        start: date,
        end: date,
    ) -> tuple[pd.Series, pd.DataFrame]:
        """
        Retrieve historical returns and prepare optimization inputs.

        Returns
        -------
        tuple[pd.Series, pd.DataFrame]
            Annualized expected returns and annualized covariance matrix.
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
    def get_mean_variance_portfolio(
        tickers: list[str],
        *,
        start: date,
        end: date,
        risk_aversion: float = DEFAULT_RISK_AVERSION,
    ) -> pd.Series:
        """
        Compute the Mean-Variance optimal portfolio.
        """

        (
            expected_returns,
            covariance_matrix,
        ) = OptimizationService._prepare_optimization_inputs(
            tickers,
            start=start,
            end=end,
        )

        return optimize_mean_variance(
            expected_returns,
            covariance_matrix,
            risk_aversion=risk_aversion,
        )

    @staticmethod
    def get_minimum_variance_portfolio(
        tickers: list[str],
        *,
        start: date,
        end: date,
    ) -> pd.Series:
        """
        Compute the Minimum Variance portfolio.
        """

        (
            expected_returns,
            covariance_matrix,
        ) = OptimizationService._prepare_optimization_inputs(
            tickers,
            start=start,
            end=end,
        )

        return optimize_minimum_variance(
            expected_returns,
            covariance_matrix,
        )

    @staticmethod
    def get_maximum_sharpe_portfolio(
        tickers: list[str],
        *,
        start: date,
        end: date,
        risk_free_rate: float = DEFAULT_RISK_FREE_RATE,
    ) -> pd.Series:
        """
        Compute the Maximum Sharpe Ratio portfolio.
        """

        (
            expected_returns,
            covariance_matrix,
        ) = OptimizationService._prepare_optimization_inputs(
            tickers,
            start=start,
            end=end,
        )

        return optimize_maximum_sharpe(
            expected_returns,
            covariance_matrix,
            risk_free_rate=risk_free_rate,
        )

    @staticmethod
    def get_efficient_frontier(
        tickers: list[str],
        *,
        start: date,
        end: date,
        num_points: int = DEFAULT_FRONTIER_POINTS,
    ) -> list[EfficientFrontierPoint]:
        """
        Generate the Efficient Frontier.
        """

        (
            expected_returns,
            covariance_matrix,
        ) = OptimizationService._prepare_optimization_inputs(
            tickers,
            start=start,
            end=end,
        )

        return generate_efficient_frontier(
            expected_returns,
            covariance_matrix,
            num_points=num_points,
        )