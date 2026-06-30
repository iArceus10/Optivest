"""
Domain models for portfolio optimization.

These immutable value objects represent the results produced by the
portfolio optimization engines.
"""

from __future__ import annotations

from dataclasses import dataclass

import pandas as pd


@dataclass(
    frozen=True,
    slots=True,
)
class OptimizedPortfolio:
    """
    Represents an optimized portfolio.

    Attributes
    ----------
    expected_return:
        Annualized expected portfolio return.

    volatility:
        Annualized portfolio volatility.

    weights:
        Portfolio allocation weights indexed by asset ticker.
    """

    expected_return: float
    volatility: float
    weights: pd.Series


@dataclass(
    frozen=True,
    slots=True,
)
class EfficientFrontierPoint:
    """
    Represents a single portfolio on the Efficient Frontier.

    Attributes
    ----------
    expected_return:
        Annualized expected portfolio return.

    volatility:
        Annualized portfolio volatility.

    weights:
        Portfolio allocation weights indexed by asset ticker.
    """

    expected_return: float
    volatility: float
    weights: pd.Series