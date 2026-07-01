from __future__ import annotations

from unittest.mock import patch

import pandas as pd
from fastapi import status

from app.financial_engines.simulation.models import (
    MonteCarloPortfolio,
    MonteCarloSimulationResult,
)

REQUEST = {
    "tickers": ["AAPL", "MSFT"],
    "start": "2024-01-01",
    "end": "2024-12-31",
}


def _portfolio(
    *,
    expected_return: float,
    volatility: float,
    sharpe_ratio: float,
    weights: list[float],
) -> MonteCarloPortfolio:
    return MonteCarloPortfolio(
        expected_return=expected_return,
        volatility=volatility,
        sharpe_ratio=sharpe_ratio,
        weights=pd.Series(
            weights,
            index=["AAPL", "MSFT"],
            name="weight",
        ),
    )


def test_simulation_success(client):
    portfolio_one = _portfolio(
        expected_return=0.12,
        volatility=0.18,
        sharpe_ratio=0.56,
        weights=[0.4, 0.6],
    )

    portfolio_two = _portfolio(
        expected_return=0.15,
        volatility=0.25,
        sharpe_ratio=0.52,
        weights=[0.7, 0.3],
    )

    result = MonteCarloSimulationResult(
        portfolios=[
            portfolio_one,
            portfolio_two,
        ],
        best_sharpe=portfolio_one,
        minimum_volatility=portfolio_one,
    )

    with patch(
        "app.api.v1.simulation.SimulationService.run_simulation",
        return_value=result,
    ):
        response = client.post(
            "/api/v1/simulation",
            json={
                **REQUEST,
                "simulation_count": 2,
                "risk_free_rate": 0.02,
                "seed": 42,
            },
        )

    assert response.status_code == status.HTTP_200_OK

    body = response.json()

    assert len(body["portfolios"]) == 2

    assert (
        body["best_sharpe"]["sharpe_ratio"]
        == 0.56
    )

    assert (
        body["minimum_volatility"]["volatility"]
        == 0.18
    )

    assert (
        body["portfolios"][0]["allocations"][0]["ticker"]
        == "AAPL"
    )


def test_simulation_service_error(client):
    with patch(
        "app.api.v1.simulation.SimulationService.run_simulation",
        side_effect=ValueError("Simulation failed."),
    ):
        response = client.post(
            "/api/v1/simulation",
            json={
                **REQUEST,
                "simulation_count": 100,
                "risk_free_rate": 0.02,
            },
        )

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    assert (
        response.json()["detail"]
        == "Simulation failed."
    )


def test_simulation_validation_error(client):
    response = client.post(
        "/api/v1/simulation",
        json={
            "tickers": ["AAPL"],
            "start": "2024-01-01",
            "end": "2024-12-31",
        },
    )

    assert (
        response.status_code
        == status.HTTP_422_UNPROCESSABLE_ENTITY
    )


def test_simulation_invalid_simulation_count(client):
    response = client.post(
        "/api/v1/simulation",
        json={
            **REQUEST,
            "simulation_count": 0,
        },
    )

    assert (
        response.status_code
        == status.HTTP_422_UNPROCESSABLE_ENTITY
    )


def test_simulation_accepts_null_seed(client):
    portfolio = _portfolio(
        expected_return=0.10,
        volatility=0.20,
        sharpe_ratio=0.40,
        weights=[0.5, 0.5],
    )

    result = MonteCarloSimulationResult(
        portfolios=[portfolio],
        best_sharpe=portfolio,
        minimum_volatility=portfolio,
    )

    with patch(
        "app.api.v1.simulation.SimulationService.run_simulation",
        return_value=result,
    ):
        response = client.post(
            "/api/v1/simulation",
            json={
                **REQUEST,
                "simulation_count": 1,
                "seed": None,
            },
        )

    assert response.status_code == status.HTTP_200_OK