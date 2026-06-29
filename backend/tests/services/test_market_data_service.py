from datetime import date

import pandas as pd
import pytest

from app.services.market_data_service import (
    MarketDataService,
)


def test_empty_ticker_list():
    with pytest.raises(ValueError):
        MarketDataService.get_historical_prices(
            [],
            start=date(2024, 1, 1),
            end=date(2024, 12, 31),
        )


def test_invalid_date_range():
    with pytest.raises(ValueError):
        MarketDataService.get_historical_prices(
            ["AAPL"],
            start=date(2024, 12, 31),
            end=date(2024, 1, 1),
        )


def test_normalizes_tickers(monkeypatch):
    captured = {}

    def fake_get_prices(
        tickers,
        *,
        start,
        end,
    ):
        captured["tickers"] = tickers

        return pd.DataFrame(
            {
                "AAPL": [100, 101],
            }
        )

    monkeypatch.setattr(
        "app.services.market_data_service.MarketDataEngine.get_adjusted_close_prices",
        fake_get_prices,
    )

    MarketDataService.get_historical_prices(
        [" aapl ", "AAPL"],
        start=date(2024, 1, 1),
        end=date(2024, 12, 31),
    )

    assert captured["tickers"] == ["AAPL"]