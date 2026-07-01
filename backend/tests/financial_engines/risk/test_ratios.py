from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from app.financial_engines.market_data.annualization import (
    TRADING_DAYS_PER_YEAR,
)
from app.financial_engines.risk.ratios import (
    DEFAULT_RISK_FREE_RATE,
    calculate_sharpe_ratio,
    calculate_sortino_ratio,
)


@pytest.fixture
def returns() -> pd.Series:
    return pd.Series(
        [
            0.012,
            -0.008,
            0.015,
            0.004,
            -0.003,
            0.010,
            0.006,
            -0.005,
        ],
        name="portfolio_returns",
    )


def test_sharpe_ratio_matches_manual_calculation(
    returns: pd.Series,
) -> None:
    sharpe = calculate_sharpe_ratio(
        returns,
        risk_free_rate=0.02,
    )

    mean_daily_return = float(
        returns.mean()
    )

    daily_volatility = float(
        returns.std(ddof=1)
    )

    expected = (
        mean_daily_return
        * TRADING_DAYS_PER_YEAR
        - 0.02
    ) / (
        daily_volatility
        * np.sqrt(TRADING_DAYS_PER_YEAR)
    )

    assert sharpe == pytest.approx(
        expected
    )


def test_sortino_ratio_matches_manual_calculation(
    returns: pd.Series,
) -> None:
    sortino = calculate_sortino_ratio(
        returns,
        risk_free_rate=0.02,
    )

    mean_daily_return = float(
        returns.mean()
    )

    annualized_return = (
        mean_daily_return
        * TRADING_DAYS_PER_YEAR
    )

    daily_risk_free_rate = (
        0.02
        / TRADING_DAYS_PER_YEAR
    )

    downside_returns = returns[
        returns < daily_risk_free_rate
    ]

    downside_deviation = float(
        np.sqrt(
            (
                (
                    downside_returns
                    - daily_risk_free_rate
                ) ** 2
            ).mean()
        )
    )

    expected = (
        annualized_return
        - 0.02
    ) / (
        downside_deviation
        * np.sqrt(TRADING_DAYS_PER_YEAR)
    )

    assert sortino == pytest.approx(
        expected
    )


def test_sharpe_ratio_zero_volatility() -> None:
    returns = pd.Series(
        [0.01] * 20
    )

    assert (
        calculate_sharpe_ratio(
            returns
        )
        == 0.0
    )


def test_sortino_ratio_no_downside_returns() -> None:
    returns = pd.Series(
        [0.02] * 20
    )

    assert (
        calculate_sortino_ratio(
            returns
        )
        == 0.0
    )


def test_sortino_ratio_zero_downside_deviation() -> None:
    daily_rf = (
        DEFAULT_RISK_FREE_RATE
        / TRADING_DAYS_PER_YEAR
    )

    returns = pd.Series(
        [
            daily_rf,
            daily_rf,
            daily_rf,
            daily_rf,
        ]
    )

    assert (
        calculate_sortino_ratio(
            returns
        )
        == 0.0
    )


def test_ratios_are_deterministic(
    returns: pd.Series,
) -> None:
    sharpe_first = calculate_sharpe_ratio(
        returns
    )

    sharpe_second = calculate_sharpe_ratio(
        returns
    )

    sortino_first = calculate_sortino_ratio(
        returns
    )

    sortino_second = calculate_sortino_ratio(
        returns
    )

    assert sharpe_first == pytest.approx(
        sharpe_second
    )

    assert sortino_first == pytest.approx(
        sortino_second
    )


def test_default_risk_free_rate(
    returns: pd.Series,
) -> None:
    result = calculate_sharpe_ratio(
        returns
    )

    assert (
        DEFAULT_RISK_FREE_RATE
        == 0.02
    )

    assert isinstance(
        result,
        float,
    )