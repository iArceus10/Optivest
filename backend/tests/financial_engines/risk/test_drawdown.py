from __future__ import annotations

import pandas as pd
import pytest

from app.financial_engines.risk.drawdown import (
    calculate_maximum_drawdown,
)


def test_maximum_drawdown_matches_manual_calculation() -> None:
    returns = pd.Series(
        [
            0.10,
            -0.20,
            0.05,
            -0.10,
            0.08,
        ]
    )

    cumulative = (1.0 + returns).cumprod()
    running_peak = cumulative.cummax()
    drawdowns = cumulative / running_peak - 1.0

    expected = float(
        -drawdowns.min()
    )

    result = calculate_maximum_drawdown(
        returns
    )

    assert result == pytest.approx(
        expected
    )


def test_maximum_drawdown_zero_for_monotonic_growth() -> None:
    returns = pd.Series(
        [
            0.01,
            0.02,
            0.015,
            0.005,
        ]
    )

    result = calculate_maximum_drawdown(
        returns
    )

    assert result == pytest.approx(
        0.0
    )


def test_maximum_drawdown_positive_after_loss() -> None:
    returns = pd.Series(
        [
            0.10,
            -0.30,
            0.05,
        ]
    )

    result = calculate_maximum_drawdown(
        returns
    )

    assert result > 0.0


def test_maximum_drawdown_all_losses() -> None:
    returns = pd.Series(
        [
            -0.10,
            -0.05,
            -0.20,
        ]
    )

    result = calculate_maximum_drawdown(
        returns
    )

    assert result > 0.0
    assert result <= 1.0


def test_maximum_drawdown_single_large_loss() -> None:
    returns = pd.Series(
        [
            0.05,
            -0.50,
            0.10,
        ]
    )

    result = calculate_maximum_drawdown(
        returns
    )

    assert result == pytest.approx(
        0.50
    )


def test_maximum_drawdown_is_deterministic() -> None:
    returns = pd.Series(
        [
            0.02,
            -0.01,
            0.03,
            -0.04,
            0.01,
        ]
    )

    first = calculate_maximum_drawdown(
        returns
    )

    second = calculate_maximum_drawdown(
        returns
    )

    assert first == pytest.approx(
        second
    )