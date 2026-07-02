from __future__ import annotations

from datetime import date
from unittest.mock import patch

from fastapi.testclient import TestClient

from app.financial_engines.portfolio_health.models import (
    PortfolioHealthResult,
)
from app.main import app

client = TestClient(app)


def test_analyze_portfolio_health_success() -> None:
    result = PortfolioHealthResult(
        overall_health_score=84.0,
        return_score=72.0,
        risk_score=86.0,
        diversification_score=80.0,
        concentration_score=78.0,
        optimization_efficiency_score=88.0,
        summary="Strong portfolio with manageable risk.",
        recommendations=(
            "Maintain the current portfolio strategy.",
        ),
    )

    with patch(
        "app.api.v1.portfolio_health."
        "PortfolioHealthService.analyze_portfolio_health",
        return_value=result,
    ) as service_mock:
        response = client.post(
            "/api/v1/portfolio-health",
            json={
                "tickers": ["AAPL", "MSFT", "NVDA"],
                "weights": [0.4, 0.35, 0.25],
                "start": "2024-01-01",
                "end": "2024-12-31",
                "risk_free_rate": 0.03,
                "simulation_count": 5000,
                "seed": 42,
            },
        )

    assert response.status_code == 200
    assert response.json() == {
        "overall_health_score": 84.0,
        "return_score": 72.0,
        "risk_score": 86.0,
        "diversification_score": 80.0,
        "concentration_score": 78.0,
        "optimization_efficiency_score": 88.0,
        "summary": "Strong portfolio with manageable risk.",
        "recommendations": [
            "Maintain the current portfolio strategy.",
        ],
    }

    service_mock.assert_called_once_with(
        tickers=["AAPL", "MSFT", "NVDA"],
        weights=[0.4, 0.35, 0.25],
        start=date(2024, 1, 1),
        end=date(2024, 12, 31),
        risk_free_rate=0.03,
        simulation_count=5000,
        seed=42,
    )


def test_analyze_portfolio_health_uses_defaults() -> None:
    result = PortfolioHealthResult(
        overall_health_score=80.0,
        return_score=70.0,
        risk_score=82.0,
        diversification_score=78.0,
        concentration_score=76.0,
        optimization_efficiency_score=84.0,
        summary="Moderate portfolio health with room for improvement.",
        recommendations=(
            "Improve diversification across holdings.",
        ),
    )

    with patch(
        "app.api.v1.portfolio_health."
        "PortfolioHealthService.analyze_portfolio_health",
        return_value=result,
    ) as service_mock:
        response = client.post(
            "/api/v1/portfolio-health",
            json={
                "tickers": ["AAPL", "MSFT"],
                "weights": [0.5, 0.5],
                "start": "2024-01-01",
                "end": "2024-12-31",
            },
        )

    assert response.status_code == 200

    service_mock.assert_called_once_with(
        tickers=["AAPL", "MSFT"],
        weights=[0.5, 0.5],
        start=date(2024, 1, 1),
        end=date(2024, 12, 31),
        risk_free_rate=0.02,
        simulation_count=10_000,
        seed=None,
    )


def test_analyze_portfolio_health_validation_error() -> None:
    with patch(
        "app.api.v1.portfolio_health."
        "PortfolioHealthService.analyze_portfolio_health",
        side_effect=ValueError(
            "Number of weights must match number of tickers."
        ),
    ):
        response = client.post(
            "/api/v1/portfolio-health",
            json={
                "tickers": ["AAPL", "MSFT", "NVDA"],
                "weights": [0.5, 0.5],
                "start": "2024-01-01",
                "end": "2024-12-31",
            },
        )

    assert response.status_code == 400
    assert response.json() == {
        "detail": "Number of weights must match number of tickers."
    }


def test_analyze_portfolio_health_invalid_request_body() -> None:
    response = client.post(
        "/api/v1/portfolio-health",
        json={
            "tickers": ["AAPL"],
            "weights": [1.0],
            "start": "2024-01-01",
            "end": "2024-12-31",
        },
    )

    assert response.status_code == 422


def test_analyze_portfolio_health_rejects_extra_fields() -> None:
    response = client.post(
        "/api/v1/portfolio-health",
        json={
            "tickers": ["AAPL", "MSFT"],
            "weights": [0.5, 0.5],
            "start": "2024-01-01",
            "end": "2024-12-31",
            "unexpected": "field",
        },
    )

    assert response.status_code == 422