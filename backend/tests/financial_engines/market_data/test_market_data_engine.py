import pandas as pd
import pytest

from app.financial_engines.market_data.market_data_engine import (
    MarketDataEngine,
)


def test_empty_ticker_list():
    with pytest.raises(ValueError):
        MarketDataEngine.get_adjusted_close_prices(
            [],
            start="2024-01-01",
            end="2024-12-31",
        )


def test_returns_dataframe(monkeypatch):
    sample = pd.DataFrame(
        {
            "Close": [100.0, 101.0, 102.0],
        }
    )

    def fake_download(*args, **kwargs):
        return sample

    monkeypatch.setattr(
        "yfinance.download",
        fake_download,
    )

    prices = MarketDataEngine.get_adjusted_close_prices(
        ["AAPL"],
        start="2024-01-01",
        end="2024-12-31",
    )

    assert isinstance(prices, pd.DataFrame)

    assert list(prices.columns) == ["AAPL"]

    assert len(prices) == 3