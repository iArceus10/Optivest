from __future__ import annotations

from dataclasses import FrozenInstanceError

import pytest

from app.financial_engines.portfolio_health.models import (
    PortfolioHealthResult,
)


def test_portfolio_health_result_fields() -> None:
    result = PortfolioHealthResult(
        overall_health_score=84.5,
        return_score=70.0,
        risk_score=88.0,
        diversification_score=80.0,
        concentration_score=85.0,
        optimization_efficiency_score=90.0,
        summary="Strong portfolio with manageable risk.",
        recommendations=(
            "Maintain the current portfolio strategy.",
        ),
    )

    assert result.overall_health_score == pytest.approx(
        84.5
    )
    assert result.return_score == pytest.approx(
        70.0
    )
    assert result.risk_score == pytest.approx(
        88.0
    )
    assert result.diversification_score == pytest.approx(
        80.0
    )
    assert result.concentration_score == pytest.approx(
        85.0
    )
    assert (
        result.summary
        == "Strong portfolio with manageable risk."
    )
    assert result.recommendations == (
        "Maintain the current portfolio strategy.",
    )


def test_portfolio_health_result_is_immutable() -> None:
    result = PortfolioHealthResult(
        overall_health_score=80.0,
        return_score=70.0,
        risk_score=75.0,
        diversification_score=90.0,
        concentration_score=80.0,
        optimization_efficiency_score=90.0,
        summary="Excellent portfolio health.",
        recommendations=(
            "Maintain the current portfolio strategy.",
        ),
    )

    with pytest.raises(FrozenInstanceError):
        result.overall_health_score = 90.0  # type: ignore[misc]