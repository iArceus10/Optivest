from datetime import date

import pandas as pd
from fastapi import status

from app.services.statistics_service import (
    StatisticsService,
)


# ------------------------------------------------------------------
# Authentication helpers
# ------------------------------------------------------------------


def register_user(client):
    payload = {
        "email": "statistics@example.com",
        "full_name": "Statistics User",
        "password": "SecurePassword123!",
    }

    response = client.post(
        "/api/v1/auth/register",
        json=payload,
    )

    assert response.status_code == status.HTTP_201_CREATED

    return payload


def login_user(client, payload):
    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": payload["email"],
            "password": payload["password"],
        },
    )

    assert response.status_code == status.HTTP_200_OK

    return response.json()["access_token"]


def auth_headers(token):
    return {
        "Authorization": f"Bearer {token}",
    }


# ------------------------------------------------------------------
# Expected Returns
# ------------------------------------------------------------------


def test_get_expected_returns(client, monkeypatch):
    sample = pd.Series(
        {
            "AAPL": 0.18,
            "MSFT": 0.22,
        }
    )

    monkeypatch.setattr(
        StatisticsService,
        "get_expected_returns",
        lambda **kwargs: sample,
    )

    payload = register_user(client)
    token = login_user(client, payload)

    response = client.get(
        "/api/v1/statistics/returns",
        params={
            "tickers": ["AAPL", "MSFT"],
            "start": "2024-01-01",
            "end": "2024-12-31",
        },
        headers=auth_headers(token),
    )

    assert response.status_code == status.HTTP_200_OK

    body = response.json()

    assert body["expected_returns"] == {
        "AAPL": 0.18,
        "MSFT": 0.22,
    }


# ------------------------------------------------------------------
# Covariance Matrix
# ------------------------------------------------------------------


def test_get_covariance_matrix(client, monkeypatch):
    sample = pd.DataFrame(
        {
            "AAPL": {
                "AAPL": 0.10,
                "MSFT": 0.02,
            },
            "MSFT": {
                "AAPL": 0.02,
                "MSFT": 0.08,
            },
        }
    )

    monkeypatch.setattr(
        StatisticsService,
        "get_covariance_matrix",
        lambda **kwargs: sample,
    )

    payload = register_user(client)
    token = login_user(client, payload)

    response = client.get(
        "/api/v1/statistics/covariance",
        params={
            "tickers": ["AAPL", "MSFT"],
            "start": "2024-01-01",
            "end": "2024-12-31",
        },
        headers=auth_headers(token),
    )

    assert response.status_code == status.HTTP_200_OK

    body = response.json()

    assert body["covariance_matrix"]["AAPL"]["AAPL"] == 0.10
    assert body["covariance_matrix"]["MSFT"]["MSFT"] == 0.08


# ------------------------------------------------------------------
# Correlation Matrix
# ------------------------------------------------------------------


def test_get_correlation_matrix(client, monkeypatch):
    sample = pd.DataFrame(
        {
            "AAPL": {
                "AAPL": 1.0,
                "MSFT": 0.73,
            },
            "MSFT": {
                "AAPL": 0.73,
                "MSFT": 1.0,
            },
        }
    )

    monkeypatch.setattr(
        StatisticsService,
        "get_correlation_matrix",
        lambda **kwargs: sample,
    )

    payload = register_user(client)
    token = login_user(client, payload)

    response = client.get(
        "/api/v1/statistics/correlation",
        params={
            "tickers": ["AAPL", "MSFT"],
            "start": "2024-01-01",
            "end": "2024-12-31",
        },
        headers=auth_headers(token),
    )

    assert response.status_code == status.HTTP_200_OK

    body = response.json()

    assert body["correlation_matrix"]["AAPL"]["AAPL"] == 1.0
    assert body["correlation_matrix"]["MSFT"]["MSFT"] == 1.0


# ------------------------------------------------------------------
# Portfolio Volatility
# ------------------------------------------------------------------


def test_get_portfolio_volatility(client, monkeypatch):
    monkeypatch.setattr(
        StatisticsService,
        "get_portfolio_volatility",
        lambda **kwargs: 0.2145,
    )

    payload = register_user(client)
    token = login_user(client, payload)

    response = client.get(
        "/api/v1/statistics/volatility",
        params={
            "tickers": ["AAPL", "MSFT"],
            "weights": [0.5, 0.5],
            "start": "2024-01-01",
            "end": "2024-12-31",
        },
        headers=auth_headers(token),
    )

    assert response.status_code == status.HTTP_200_OK

    body = response.json()

    assert body["portfolio_volatility"] == 0.2145


# ------------------------------------------------------------------
# Authentication
# ------------------------------------------------------------------


def test_statistics_requires_authentication(client):
    response = client.get(
        "/api/v1/statistics/returns",
        params={
            "tickers": ["AAPL"],
            "start": "2024-01-01",
            "end": "2024-12-31",
        },
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


# ------------------------------------------------------------------
# Business Errors
# ------------------------------------------------------------------


def test_statistics_validation_error(client, monkeypatch):
    def fake_service(**kwargs):
        raise ValueError("Invalid portfolio.")

    monkeypatch.setattr(
        StatisticsService,
        "get_expected_returns",
        fake_service,
    )

    payload = register_user(client)
    token = login_user(client, payload)

    response = client.get(
        "/api/v1/statistics/returns",
        params={
            "tickers": ["AAPL"],
            "start": "2024-12-31",
            "end": "2024-01-01",
        },
        headers=auth_headers(token),
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == "Invalid portfolio."