from datetime import date

import pandas as pd
import pytest

from app.services.statistics_service import (
    StatisticsService,
)


def sample_returns() -> pd.DataFrame:
    """
    Sample daily returns for testing.
    """

    return pd.DataFrame(
        {
            "AAPL": [0.01, 0.02, -0.01],
            "MSFT": [0.02, 0.01, 0.00],
        }
    )


def test_expected_returns(monkeypatch):
    """
    StatisticsService should delegate daily return retrieval and
    compute annualized expected returns.
    """

    monkeypatch.setattr(
        "app.services.statistics_service.MarketDataService.get_daily_returns",
        lambda **kwargs: sample_returns(),
    )

    result = StatisticsService.get_expected_returns(
        tickers=["AAPL", "MSFT"],
        start=date(2024, 1, 1),
        end=date(2024, 12, 31),
    )

    assert list(result.index) == [
        "AAPL",
        "MSFT",
    ]


def test_covariance_matrix(monkeypatch):
    """
    StatisticsService should return an annualized covariance matrix.
    """

    monkeypatch.setattr(
        "app.services.statistics_service.MarketDataService.get_daily_returns",
        lambda **kwargs: sample_returns(),
    )

    result = StatisticsService.get_covariance_matrix(
        tickers=["AAPL", "MSFT"],
        start=date(2024, 1, 1),
        end=date(2024, 12, 31),
    )

    assert result.shape == (2, 2)

    assert list(result.columns) == [
        "AAPL",
        "MSFT",
    ]


def test_correlation_matrix(monkeypatch):
    """
    StatisticsService should return a correlation matrix.
    """

    monkeypatch.setattr(
        "app.services.statistics_service.MarketDataService.get_daily_returns",
        lambda **kwargs: sample_returns(),
    )

    result = StatisticsService.get_correlation_matrix(
        tickers=["AAPL", "MSFT"],
        start=date(2024, 1, 1),
        end=date(2024, 12, 31),
    )

    assert result.shape == (2, 2)

    assert result.loc["AAPL", "AAPL"] == pytest.approx(
        1.0
    )


def test_portfolio_volatility(monkeypatch):
    """
    StatisticsService should compute portfolio volatility.
    """

    monkeypatch.setattr(
        "app.services.statistics_service.MarketDataService.get_daily_returns",
        lambda **kwargs: sample_returns(),
    )

    volatility = StatisticsService.get_portfolio_volatility(
        tickers=["AAPL", "MSFT"],
        weights=[0.5, 0.5],
        start=date(2024, 1, 1),
        end=date(2024, 12, 31),
    )

    assert volatility > 0


def test_weight_count_validation():
    """
    A portfolio must provide one weight per ticker.
    """

    with pytest.raises(ValueError):
        StatisticsService.get_portfolio_volatility(
            tickers=["AAPL", "MSFT"],
            weights=[1.0],
            start=date(2024, 1, 1),
            end=date(2024, 12, 31),
        )