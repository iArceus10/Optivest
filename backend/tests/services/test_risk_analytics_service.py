from __future__ import annotations

from datetime import date
from unittest.mock import patch

import pandas as pd
import pytest

from app.financial_engines.risk.models import (
    RiskAnalyticsResult,
)
from app.services.risk_analytics_service import (
    RiskAnalyticsService,
)


@pytest.fixture
def daily_returns() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "AAPL": [0.01, 0.02, -0.01],
            "MSFT": [0.02, 0.01, 0.00],
        }
    )


@pytest.fixture
def weights() -> list[float]:
    return [0.4, 0.6]


@pytest.fixture
def portfolio_returns() -> pd.Series:
    return pd.Series(
        [
            0.016,
            0.014,
            -0.004,
        ],
        name="portfolio_return",
    )


@pytest.fixture
def risk_result() -> RiskAnalyticsResult:
    return RiskAnalyticsResult(
        sharpe_ratio=1.25,
        sortino_ratio=1.70,
        maximum_drawdown=0.18,
        value_at_risk=0.06,
        conditional_value_at_risk=0.08,
    )


def test_prepare_portfolio_returns(
    daily_returns: pd.DataFrame,
    weights: list[float],
    portfolio_returns: pd.Series,
) -> None:
    with patch(
        "app.services.risk_analytics_service.MarketDataService.get_daily_returns",
        return_value=daily_returns,
    ):
        result = (
            RiskAnalyticsService._prepare_portfolio_returns(
                ["AAPL", "MSFT"],
                weights,
                start=date(2024, 1, 1),
                end=date(2024, 12, 31),
            )
        )

    expected = daily_returns @ pd.Series(
        weights,
        index=daily_returns.columns,
        dtype=float,
    )

    pd.testing.assert_series_equal(
        result,
        expected,
    )


def test_prepare_portfolio_returns_empty_tickers() -> None:
    with pytest.raises(
        ValueError,
        match="At least one ticker must be provided.",
    ):
        RiskAnalyticsService._prepare_portfolio_returns(
            [],
            [],
            start=date(2024, 1, 1),
            end=date(2024, 12, 31),
        )


def test_prepare_portfolio_returns_weight_mismatch() -> None:
    with pytest.raises(
        ValueError,
        match="Number of weights must match number of tickers.",
    ):
        RiskAnalyticsService._prepare_portfolio_returns(
            ["AAPL", "MSFT"],
            [1.0],
            start=date(2024, 1, 1),
            end=date(2024, 12, 31),
        )


def test_analyze_portfolio_risk(
    daily_returns: pd.DataFrame,
    weights: list[float],
    risk_result: RiskAnalyticsResult,
) -> None:
    expected_portfolio_returns = (
        daily_returns
        @ pd.Series(
            weights,
            index=daily_returns.columns,
            dtype=float,
        )
    )

    with (
        patch(
            "app.services.risk_analytics_service.MarketDataService.get_daily_returns",
            return_value=daily_returns,
        ),
        patch(
            "app.services.risk_analytics_service.calculate_risk_metrics",
            return_value=risk_result,
        ) as risk_mock,
    ):
        result = (
            RiskAnalyticsService.analyze_portfolio_risk(
                ["AAPL", "MSFT"],
                weights,
                start=date(2024, 1, 1),
                end=date(2024, 12, 31),
                risk_free_rate=0.03,
                confidence_level=0.99,
            )
        )

    assert result is risk_result

    risk_mock.assert_called_once()

    args, kwargs = risk_mock.call_args

    pd.testing.assert_series_equal(
        args[0],
        expected_portfolio_returns,
    )

    assert kwargs["risk_free_rate"] == pytest.approx(
        0.03
    )

    assert kwargs["confidence_level"] == pytest.approx(
        0.99
    )

def test_analyze_portfolio_risk_from_returns() -> None:
    returns = pd.DataFrame(
        {
            "AAPL": [0.01, -0.01, 0.02, 0.005],
            "MSFT": [0.005, -0.002, 0.015, 0.01],
        }
    )

    result = RiskAnalyticsService.analyze_portfolio_risk_from_returns(
        returns,
        [0.5, 0.5],
        risk_free_rate=0.02,
    )

    assert isinstance(result, RiskAnalyticsResult)