from __future__ import annotations

from datetime import date
from unittest.mock import patch

import pandas as pd
from fastapi import status

from app.financial_engines.optimization.models import (
    EfficientFrontierPoint,
)


REQUEST = {
    "tickers": ["AAPL", "MSFT"],
    "start": "2024-01-01",
    "end": "2024-12-31",
}


def test_mean_variance_success(client):
    weights = pd.Series(
        [0.6, 0.4],
        index=["AAPL", "MSFT"],
        name="weight",
    )

    with patch(
        "app.api.v1.optimization.OptimizationService.get_mean_variance_portfolio",
        return_value=weights,
    ):
        response = client.post(
            "/api/v1/optimization/mean-variance",
            json={
                **REQUEST,
                "risk_aversion": 1.0,
            },
        )

    assert response.status_code == status.HTTP_200_OK

    body = response.json()

    assert body == {
        "allocations": [
            {
                "ticker": "AAPL",
                "weight": 0.6,
            },
            {
                "ticker": "MSFT",
                "weight": 0.4,
            },
        ]
    }


def test_mean_variance_service_error(client):
    with patch(
        "app.api.v1.optimization.OptimizationService.get_mean_variance_portfolio",
        side_effect=ValueError("Optimization failed."),
    ):
        response = client.post(
            "/api/v1/optimization/mean-variance",
            json={
                **REQUEST,
                "risk_aversion": 1.0,
            },
        )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == "Optimization failed."


def test_minimum_variance_success(client):
    weights = pd.Series(
        [0.3, 0.7],
        index=["AAPL", "MSFT"],
        name="weight",
    )

    with patch(
        "app.api.v1.optimization.OptimizationService.get_minimum_variance_portfolio",
        return_value=weights,
    ):
        response = client.post(
            "/api/v1/optimization/minimum-variance",
            json=REQUEST,
        )

    assert response.status_code == status.HTTP_200_OK

    allocations = response.json()["allocations"]

    assert len(allocations) == 2
    assert allocations[0]["ticker"] == "AAPL"


def test_maximum_sharpe_success(client):
    weights = pd.Series(
        [0.45, 0.55],
        index=["AAPL", "MSFT"],
        name="weight",
    )

    with patch(
        "app.api.v1.optimization.OptimizationService.get_maximum_sharpe_portfolio",
        return_value=weights,
    ):
        response = client.post(
            "/api/v1/optimization/maximum-sharpe",
            json={
                **REQUEST,
                "risk_free_rate": 0.02,
            },
        )

    assert response.status_code == status.HTTP_200_OK

    allocations = response.json()["allocations"]

    assert allocations[1]["weight"] == 0.55


def test_efficient_frontier_success(client):
    frontier = [
        EfficientFrontierPoint(
            expected_return=0.12,
            volatility=0.18,
            weights=pd.Series(
                [0.5, 0.5],
                index=["AAPL", "MSFT"],
                name="weight",
            ),
        ),
        EfficientFrontierPoint(
            expected_return=0.15,
            volatility=0.23,
            weights=pd.Series(
                [0.7, 0.3],
                index=["AAPL", "MSFT"],
                name="weight",
            ),
        ),
    ]

    with patch(
        "app.api.v1.optimization.OptimizationService.get_efficient_frontier",
        return_value=frontier,
    ):
        response = client.post(
            "/api/v1/optimization/efficient-frontier",
            json={
                **REQUEST,
                "num_points": 2,
            },
        )

    assert response.status_code == status.HTTP_200_OK

    body = response.json()

    assert len(body["frontier"]) == 2
    assert body["frontier"][0]["expected_return"] == 0.12
    assert body["frontier"][1]["volatility"] == 0.23


def test_efficient_frontier_service_error(client):
    with patch(
        "app.api.v1.optimization.OptimizationService.get_efficient_frontier",
        side_effect=ValueError("Frontier generation failed."),
    ):
        response = client.post(
            "/api/v1/optimization/efficient-frontier",
            json={
                **REQUEST,
                "num_points": 10,
            },
        )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert (
        response.json()["detail"]
        == "Frontier generation failed."
    )


def test_mean_variance_validation_error(client):
    response = client.post(
        "/api/v1/optimization/mean-variance",
        json={
            "tickers": ["AAPL"],
            "start": "2024-01-01",
            "end": "2024-12-31",
            "risk_aversion": 1.0,
        },
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_efficient_frontier_validation_error(client):
    response = client.post(
        "/api/v1/optimization/efficient-frontier",
        json={
            **REQUEST,
            "num_points": 0,
        },
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY