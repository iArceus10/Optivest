"""
Monte Carlo portfolio simulation.

Generates random long-only portfolios using annualized expected returns
and covariance matrices produced by the Statistics Engine.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from app.financial_engines.simulation.models import (
    MonteCarloPortfolio,
    MonteCarloSimulationResult,
)
from app.financial_engines.simulation.validation import (
    validate_simulation_inputs,
)

DEFAULT_SIMULATION_COUNT = 10_000
DEFAULT_RISK_FREE_RATE = 0.02


def _generate_random_weights(
    rng: np.random.Generator,
    number_of_assets: int,
) -> np.ndarray:
    """
    Generate a random long-only fully invested portfolio.
    """

    weights = rng.random(number_of_assets)
    weights /= weights.sum()

    return weights


def _compute_portfolio_return(
    expected_returns: np.ndarray,
    weights: np.ndarray,
) -> float:
    """
    Compute annualized expected portfolio return.
    """

    return float(
        expected_returns @ weights
    )


def _compute_portfolio_volatility(
    covariance_matrix: np.ndarray,
    weights: np.ndarray,
) -> float:
    """
    Compute annualized portfolio volatility.
    """

    variance = float(
        weights.T @ covariance_matrix @ weights
    )

    variance = max(
        variance,
        0.0,
    )

    return float(np.sqrt(variance))


def _compute_sharpe_ratio(
    expected_return: float,
    volatility: float,
    risk_free_rate: float,
) -> float:
    """
    Compute the annualized Sharpe ratio.
    """

    if np.isclose(volatility, 0.0):
        return 0.0

    return (
        expected_return - risk_free_rate
    ) / volatility


def run_monte_carlo_simulation(
    expected_returns: pd.Series,
    covariance_matrix: pd.DataFrame,
    *,
    simulation_count: int = DEFAULT_SIMULATION_COUNT,
    risk_free_rate: float = DEFAULT_RISK_FREE_RATE,
    seed: int | None = None,
) -> MonteCarloSimulationResult:
    """
    Execute Monte Carlo portfolio simulation.

    Parameters
    ----------
    expected_returns:
        Annualized expected returns.

    covariance_matrix:
        Annualized covariance matrix.

    simulation_count:
        Number of random portfolios to simulate.

    risk_free_rate:
        Annual risk-free rate expressed as a decimal.

    seed:
        Optional random seed for deterministic execution.

    Returns
    -------
    MonteCarloSimulationResult
        Complete simulation result.
    """

    validate_simulation_inputs(
        expected_returns,
        covariance_matrix,
        simulation_count=simulation_count,
        risk_free_rate=risk_free_rate,
        seed=seed,
    )

    rng = np.random.default_rng(seed)

    asset_index = expected_returns.index.copy()

    expected_return_vector = (
        expected_returns.to_numpy(dtype=float)
    )

    covariance = covariance_matrix.to_numpy(
        dtype=float
    )

    portfolios: list[
        MonteCarloPortfolio
    ] = []

    for _ in range(simulation_count):

        weights = _generate_random_weights(
            rng,
            len(asset_index),
        )

        portfolio_return = (
            _compute_portfolio_return(
                expected_return_vector,
                weights,
            )
        )

        portfolio_volatility = (
            _compute_portfolio_volatility(
                covariance,
                weights,
            )
        )

        sharpe_ratio = (
            _compute_sharpe_ratio(
                portfolio_return,
                portfolio_volatility,
                risk_free_rate,
            )
        )

        portfolios.append(
            MonteCarloPortfolio(
                expected_return=portfolio_return,
                volatility=portfolio_volatility,
                sharpe_ratio=sharpe_ratio,
                weights=pd.Series(
                    weights,
                    index=asset_index,
                    name="weight",
                ),
            )
        )

    best_sharpe = max(
        portfolios,
        key=lambda portfolio: portfolio.sharpe_ratio,
    )

    minimum_volatility = min(
        portfolios,
        key=lambda portfolio: portfolio.volatility,
    )

    return MonteCarloSimulationResult(
        portfolios=portfolios,
        best_sharpe=best_sharpe,
        minimum_volatility=minimum_volatility,
    )