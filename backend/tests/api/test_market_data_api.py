from datetime import date

import pandas as pd

from app.services.market_data_service import MarketDataService


def test_get_historical_prices(client, monkeypatch):
    sample = pd.DataFrame(
        {
            "AAPL": [100.0, 101.0],
            "MSFT": [200.0, 201.0],
        },
        index=pd.to_datetime(
            [
                "2024-01-01",
                "2024-01-02",
            ]
        ),
    )

    monkeypatch.setattr(
        MarketDataService,
        "get_historical_prices",
        lambda **kwargs: sample,
    )

    response = client.get(
        "/api/v1/market-data/history",
        params={
            "tickers": "AAPL,MSFT",
            "start": "2024-01-01",
            "end": "2024-12-31",
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["tickers"] == [
        "AAPL",
        "MSFT",
    ]

    assert len(body["records"]) == 2


def test_get_daily_returns(client, monkeypatch):
    sample = pd.DataFrame(
        {
            "AAPL": [0.01, 0.02],
            "MSFT": [0.03, 0.04],
        },
        index=pd.to_datetime(
            [
                "2024-01-02",
                "2024-01-03",
            ]
        ),
    )

    monkeypatch.setattr(
        MarketDataService,
        "get_daily_returns",
        lambda **kwargs: sample,
    )

    response = client.get(
        "/api/v1/market-data/returns",
        params={
            "tickers": "AAPL,MSFT",
            "start": "2024-01-01",
            "end": "2024-12-31",
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["tickers"] == [
        "AAPL",
        "MSFT",
    ]

    assert len(body["records"]) == 2



def test_invalid_dates(client):
    response = client.get(
        "/api/v1/market-data/history",
        params={
            "tickers": "AAPL",
            "start": "2024-12-31",
            "end": "2024-01-01",
        },
    )

    assert response.status_code == 400

def test_missing_tickers(client):
    response = client.get(
        "/api/v1/market-data/history",
        params={
            "start": "2024-01-01",
            "end": "2024-12-31",
        },
    )

    assert response.status_code == 422