"""
Domain models for Monte Carlo portfolio simulation.

These immutable value objects represent the results produced by the
Monte Carlo simulation engine.
"""

from __future__ import annotations

from dataclasses import dataclass

import pandas as pd


@dataclass(
    frozen=True,
    slots=True,
)
class MonteCarloPortfolio:
    """
    Represents a single simulated portfolio.

    Attributes
    ----------
    expected_return:
        Annualized expected portfolio return.

    volatility:
        Annualized portfolio volatility.

    sharpe_ratio:
        Portfolio Sharpe ratio.

    weights:
        Portfolio allocation weights indexed by asset ticker.
    """

    expected_return: float
    volatility: float
    sharpe_ratio: float
    weights: pd.Series


@dataclass(
    frozen=True,
    slots=True,
)
class MonteCarloSimulationResult:
    """
    Represents the complete Monte Carlo simulation.

    Attributes
    ----------
    portfolios:
        All simulated portfolios.

    best_sharpe:
        Portfolio with the highest Sharpe ratio.

    minimum_volatility:
        Portfolio with the lowest annualized volatility.
    """

    portfolios: list[MonteCarloPortfolio]
    best_sharpe: MonteCarloPortfolio
    minimum_volatility: MonteCarloPortfolio