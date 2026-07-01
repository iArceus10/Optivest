"""
Validation helpers for the Portfolio Health Financial Engine.

These functions validate numerical inputs before portfolio health
diagnostics are computed.

Validation is intentionally centralized to avoid duplication across the
Portfolio Health Engine while remaining framework-independent.
"""

from __future__ import annotations

import math

import numpy as np


def validate_portfolio_health_inputs(
    *,
    expected_return: float,
    volatility: float,
    sharpe_ratio: float,
    sortino_ratio: float,
    maximum_drawdown: float,
    value_at_risk: float,
    conditional_value_at_risk: float,
    weights: list[float],
) -> None:
    """
    Validate all numerical inputs required by the Portfolio Health
    Financial Engine.

    Parameters
    ----------
    expected_return:
        Annualized expected portfolio return.

    volatility:
        Annualized portfolio volatility.

    sharpe_ratio:
        Annualized Sharpe Ratio.

    sortino_ratio:
        Annualized Sortino Ratio.

    maximum_drawdown:
        Historical maximum drawdown.

    value_at_risk:
        Historical Value-at-Risk.

    conditional_value_at_risk:
        Historical Conditional Value-at-Risk.

    weights:
        Portfolio allocation weights.

    Raises
    ------
    ValueError
        If any supplied input is invalid.
    """

    numeric_inputs = {
        "Expected return": expected_return,
        "Volatility": volatility,
        "Sharpe ratio": sharpe_ratio,
        "Sortino ratio": sortino_ratio,
        "Maximum drawdown": maximum_drawdown,
        "Value-at-Risk": value_at_risk,
        "Conditional Value-at-Risk": (
            conditional_value_at_risk
        ),
    }

    for name, value in numeric_inputs.items():
        if not math.isfinite(value):
            raise ValueError(
                f"{name} must be a finite number."
            )

    if volatility < 0:
        raise ValueError(
            "Volatility cannot be negative."
        )

    for metric_name, metric in (
        ("Maximum drawdown", maximum_drawdown),
        ("Value-at-Risk", value_at_risk),
        (
            "Conditional Value-at-Risk",
            conditional_value_at_risk,
        ),
    ):
        if not 0.0 <= metric <= 1.0:
            raise ValueError(
                f"{metric_name} must be between 0 and 1."
            )

    if conditional_value_at_risk < value_at_risk:
        raise ValueError(
            "Conditional Value-at-Risk must be greater than or equal to Value-at-Risk."
        )

    if not weights:
        raise ValueError(
            "Portfolio weights cannot be empty."
        )

    if not all(
        math.isfinite(weight)
        for weight in weights
    ):
        raise ValueError(
            "Portfolio weights must contain only finite values."
        )

    if any(
        weight < 0
        for weight in weights
    ):
        raise ValueError(
            "Portfolio weights cannot contain negative values."
        )

    if not np.isclose(
        sum(weights),
        1.0,
        atol=1e-8,
    ):
        raise ValueError(
            "Portfolio weights must sum to 1."
        )