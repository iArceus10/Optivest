from __future__ import annotations

from unittest.mock import patch

from fastapi import status

from app.financial_engines.risk.models import (
    RiskAnalyticsResult,
)

REQUEST = {
    "tickers": ["AAPL", "MSFT"],
    "weights": [0.4, 0.6],
    "start": "2024-01-01",
    "end": "2024-12-31",
}


def test_risk_analytics_success(client):
    result = RiskAnalyticsResult(
        sharpe_ratio=1.24,
        sortino_ratio=1.68,
        maximum_drawdown=0.18,
        value_at_risk=0.06,
        conditional_value_at_risk=0.08,
    )

    with patch(
        "app.api.v1.risk.RiskAnalyticsService.analyze_portfolio_risk",
        return_value=result,
    ):
        response = client.post(
            "/api/v1/risk",
            json={
                **REQUEST,
                "risk_free_rate": 0.02,
                "confidence_level": 0.95,
            },
        )

    assert response.status_code == status.HTTP_200_OK

    assert response.json() == {
        "sharpe_ratio": 1.24,
        "sortino_ratio": 1.68,
        "maximum_drawdown": 0.18,
        "value_at_risk": 0.06,
        "conditional_value_at_risk": 0.08,
    }


def test_risk_analytics_service_error(client):
    with patch(
        "app.api.v1.risk.RiskAnalyticsService.analyze_portfolio_risk",
        side_effect=ValueError("Risk analysis failed."),
    ):
        response = client.post(
            "/api/v1/risk",
            json={
                **REQUEST,
                "risk_free_rate": 0.02,
                "confidence_level": 0.95,
            },
        )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert (
        response.json()["detail"]
        == "Risk analysis failed."
    )


def test_risk_validation_error_missing_weights(client):
    response = client.post(
        "/api/v1/risk",
        json={
            "tickers": ["AAPL", "MSFT"],
            "start": "2024-01-01",
            "end": "2024-12-31",
        },
    )

    assert (
        response.status_code
        == status.HTTP_422_UNPROCESSABLE_ENTITY
    )


def test_risk_validation_error_single_ticker(client):
    response = client.post(
        "/api/v1/risk",
        json={
            "tickers": ["AAPL"],
            "weights": [1.0],
            "start": "2024-01-01",
            "end": "2024-12-31",
        },
    )

    assert (
        response.status_code
        == status.HTTP_422_UNPROCESSABLE_ENTITY
    )


def test_risk_validation_error_invalid_confidence_level(
    client,
):
    response = client.post(
        "/api/v1/risk",
        json={
            **REQUEST,
            "confidence_level": 1.5,
        },
    )

    assert (
        response.status_code
        == status.HTTP_422_UNPROCESSABLE_ENTITY
    )


def test_risk_validation_error_empty_weights(
    client,
):
    response = client.post(
        "/api/v1/risk",
        json={
            "tickers": ["AAPL", "MSFT"],
            "weights": [],
            "start": "2024-01-01",
            "end": "2024-12-31",
        },
    )

    assert (
        response.status_code
        == status.HTTP_422_UNPROCESSABLE_ENTITY
    )