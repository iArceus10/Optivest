from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from app.financial_engines.risk.validation import (
    DEFAULT_CONFIDENCE_LEVEL,
)
from app.financial_engines.risk.value_at_risk import (
    calculate_historical_conditional_value_at_risk,
    calculate_historical_value_at_risk,
)


@pytest.fixture
def returns() -> pd.Series:
    return pd.Series(
        [
            0.020,
            -0.030,
            0.015,
            -0.050,
            0.010,
            -0.020,
            0.030,
            -0.040,
            0.005,
            -0.010,
        ],
        name="portfolio_returns",
    )


def test_historical_value_at_risk_matches_manual_calculation(
    returns: pd.Series,
) -> None:
    percentile = (
        1.0 - DEFAULT_CONFIDENCE_LEVEL
    ) * 100.0

    expected = max(
        0.0,
        -float(
            np.percentile(
                returns.to_numpy(),
                percentile,
            )
        ),
    )

    result = calculate_historical_value_at_risk(
        returns
    )

    assert result == pytest.approx(
        expected
    )


def test_historical_conditional_value_at_risk_matches_manual_calculation(
    returns: pd.Series,
) -> None:
    var = calculate_historical_value_at_risk(
        returns
    )

    tail_losses = returns[
        returns <= -var
    ]

    expected = max(
        0.0,
        -float(
            tail_losses.mean()
        ),
    )

    result = (
        calculate_historical_conditional_value_at_risk(
            returns
        )
    )

    assert result == pytest.approx(
        expected
    )


def test_conditional_value_at_risk_is_at_least_value_at_risk(
    returns: pd.Series,
) -> None:
    var = calculate_historical_value_at_risk(
        returns
    )

    cvar = (
        calculate_historical_conditional_value_at_risk(
            returns
        )
    )

    assert cvar >= var


def test_var_changes_with_confidence_level(
    returns: pd.Series,
) -> None:
    var_95 = calculate_historical_value_at_risk(
        returns,
        confidence_level=0.95,
    )

    var_99 = calculate_historical_value_at_risk(
        returns,
        confidence_level=0.99,
    )

    assert var_99 >= var_95


def test_cvar_changes_with_confidence_level(
    returns: pd.Series,
) -> None:
    cvar_95 = (
        calculate_historical_conditional_value_at_risk(
            returns,
            confidence_level=0.95,
        )
    )

    cvar_99 = (
        calculate_historical_conditional_value_at_risk(
            returns,
            confidence_level=0.99,
        )
    )

    assert cvar_99 >= cvar_95


def test_positive_returns_have_zero_var() -> None:
    returns = pd.Series(
        [
            0.01,
            0.02,
            0.03,
            0.015,
        ]
    )

    assert (
        calculate_historical_value_at_risk(
            returns
        )
        == 0.0
    )


def test_positive_returns_have_zero_cvar() -> None:
    returns = pd.Series(
        [
            0.01,
            0.02,
            0.03,
            0.015,
        ]
    )

    assert (
        calculate_historical_conditional_value_at_risk(
            returns
        )
        == 0.0
    )


def test_var_is_deterministic(
    returns: pd.Series,
) -> None:
    first = calculate_historical_value_at_risk(
        returns
    )

    second = calculate_historical_value_at_risk(
        returns
    )

    assert first == pytest.approx(
        second
    )


def test_cvar_is_deterministic(
    returns: pd.Series,
) -> None:
    first = (
        calculate_historical_conditional_value_at_risk(
            returns
        )
    )

    second = (
        calculate_historical_conditional_value_at_risk(
            returns
        )
    )

    assert first == pytest.approx(
        second
    )