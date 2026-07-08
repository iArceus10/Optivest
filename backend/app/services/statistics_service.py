from __future__ import annotations

from datetime import date

import pandas as pd

from app.financial_engines.statistics.correlation import (
    calculate_correlation_matrix,
)
from app.financial_engines.statistics.covariance import (
    calculate_annualized_covariance_matrix,
)
from app.financial_engines.statistics.expected_returns import (
    calculate_expected_annual_returns,
)
from app.financial_engines.statistics.volatility import (
    calculate_portfolio_volatility,
)
from app.services.market_data_service import MarketDataService


class StatisticsService:
    """
    Service responsible for orchestrating portfolio statistics.

    This service performs business-level validation and delegates all
    numerical computations to the Statistics Financial Engine.
    """

    @staticmethod
    def _get_daily_returns(
        tickers: list[str],
        *,
        start: date,
        end: date,
    ) -> pd.DataFrame:
        """
        Retrieve historical daily returns for the supplied tickers.
        """

        return MarketDataService.get_daily_returns(
            tickers=tickers,
            start=start,
            end=end,
        )
    
    @staticmethod
    def get_expected_returns_from_returns(
        returns: pd.DataFrame,
    ) -> pd.Series:
        """
        Compute annualized expected returns from a precomputed daily
        returns matrix.

        This helper exists for orchestration paths that already hold
        historical returns and need to avoid redundant market-data
        retrieval.
        """

        return calculate_expected_annual_returns(returns)

    @staticmethod
    def get_portfolio_expected_return_from_returns(
        returns: pd.DataFrame,
        weights: list[float],
    ) -> float:
        """
        Compute annualized portfolio expected return from a precomputed
        daily returns matrix.
        """

        if returns.empty:
            raise ValueError(
                "Daily returns data cannot be empty."
            )

        if len(returns.columns) != len(weights):
            raise ValueError(
                "Number of weights must match number of return series."
            )

        expected_returns = (
            StatisticsService.get_expected_returns_from_returns(
                returns
            )
        )

        return float(expected_returns.dot(weights))

    @staticmethod
    def get_portfolio_volatility_from_returns(
        returns: pd.DataFrame,
        weights: list[float],
    ) -> float:
        """
        Compute annualized portfolio volatility from a precomputed daily
        returns matrix.
        """

        if returns.empty:
            raise ValueError(
                "Daily returns data cannot be empty."
            )

        if len(returns.columns) != len(weights):
            raise ValueError(
                "Number of weights must match number of return series."
            )

        return calculate_portfolio_volatility(
            returns,
            weights,
        )


    @staticmethod
    def get_expected_returns(
        tickers: list[str],
        *,
        start: date,
        end: date,
    ) -> pd.Series:
        """
        Compute annualized expected returns.
        """

        returns = StatisticsService._get_daily_returns(
            tickers,
            start=start,
            end=end,
        )

        return StatisticsService.get_expected_returns_from_returns(
            returns
        )
    
    @staticmethod
    def get_portfolio_expected_return(
        tickers: list[str],
        weights: list[float],
        *,
        start: date,
        end: date,
    ) -> float:
        """
        Compute the annualized expected portfolio return.
        """

        if len(tickers) != len(weights):
            raise ValueError(
                "Number of weights must match number of tickers."
            )

        returns = StatisticsService._get_daily_returns(
            tickers,
            start=start,
            end=end,
        )

        return (
            StatisticsService
            .get_portfolio_expected_return_from_returns(
                returns,
                weights,
            )
        )

    @staticmethod
    def get_covariance_matrix(
        tickers: list[str],
        *,
        start: date,
        end: date,
    ) -> pd.DataFrame:
        """
        Compute the annualized covariance matrix.
        """

        returns = StatisticsService._get_daily_returns(
            tickers,
            start=start,
            end=end,
        )

        return calculate_annualized_covariance_matrix(
            returns
        )

    @staticmethod
    def get_correlation_matrix(
        tickers: list[str],
        *,
        start: date,
        end: date,
    ) -> pd.DataFrame:
        """
        Compute the correlation matrix.
        """

        returns = StatisticsService._get_daily_returns(
            tickers,
            start=start,
            end=end,
        )

        return calculate_correlation_matrix(returns)

    @staticmethod
    def get_portfolio_volatility(
        tickers: list[str],
        weights: list[float],
        *,
        start: date,
        end: date,
    ) -> float:
        """
        Compute annualized portfolio volatility.
        """

        if len(tickers) != len(weights):
            raise ValueError(
                "Number of weights must match number of tickers."
            )

        returns = StatisticsService._get_daily_returns(
            tickers,
            start=start,
            end=end,
        )

        return (
            StatisticsService.get_portfolio_volatility_from_returns(
                returns,
                weights,
            )
        )
    

