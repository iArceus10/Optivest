from __future__ import annotations

import pytest

from app.financial_engines.portfolio_health.health import (
    analyze_portfolio_health,
    _calculate_concentration_score,
    _calculate_diversification_score,
    _calculate_return_score,
    _calculate_risk_score,
    _generate_recommendations,
    _generate_summary,
    _calculate_optimization_efficiency_score,
)
from app.financial_engines.portfolio_health.models import (
    PortfolioHealthResult,
)


# ---------------------------------------------------------------------
# Return Score
# ---------------------------------------------------------------------


@pytest.mark.parametrize(
    ("expected_return", "expected_score"),
    [
        (0.25, 100.0),
        (0.17, 100.0),
        (0.12, 84.0),
        (0.06, 52.0),
        (0.03, 36.0),
        (-0.01, 0.0),
    ],
)
def test_return_score_thresholds(
    expected_return: float,
    expected_score: float,
) -> None:
    assert (
        _calculate_return_score(expected_return)
        == expected_score
    )


# ---------------------------------------------------------------------
# Risk Score
# ---------------------------------------------------------------------


def test_risk_score_high_quality_portfolio() -> None:
    score = _calculate_risk_score(
        sharpe_ratio=2.0,
        maximum_drawdown=0.05,
        value_at_risk=0.02,
        max_weight=0.33,
    )

    assert score > 70.0

def test_risk_score_low_quality_portfolio() -> None:
    score = _calculate_risk_score(
        sharpe_ratio=0.10,
        maximum_drawdown=0.45,
        value_at_risk=0.18,
        max_weight=0.90,
    )

    assert score < 30.0


def test_risk_score_within_bounds() -> None:
    score = _calculate_risk_score(
        sharpe_ratio=100.0,
        maximum_drawdown=0.0,
        value_at_risk=0.0,
        max_weight=0.25,
    )

    assert 0.0 <= score <= 100.0


# ---------------------------------------------------------------------
# Diversification Score
# ---------------------------------------------------------------------


def test_diversification_score_equal_weights() -> None:
    score = _calculate_diversification_score(
        [0.25, 0.25, 0.25, 0.25]
    )

    assert score == pytest.approx(100.0)

def test_diversification_score_concentrated() -> None:
    score = _calculate_diversification_score(
        [0.85, 0.10, 0.05]
    )

    assert score == pytest.approx(39.75)


# ---------------------------------------------------------------------
# Concentration Score
# ---------------------------------------------------------------------


@pytest.mark.parametrize(
    ("weights", "expected"),
    [
        ([0.20, 0.20, 0.20, 0.20, 0.20], 100.0),
        ([0.30, 0.30, 0.20, 0.20], 80.0),
        ([0.40, 0.30, 0.30], 60.0),
        ([0.50, 0.25, 0.25], 40.0),
        ([0.70, 0.20, 0.10], 20.0),
    ],
)
def test_concentration_score_thresholds(
    weights: list[float],
    expected: float,
) -> None:
    assert (
        _calculate_concentration_score(
            weights
        )
        == expected
    )

# ---------------------------------------------------------------------
# Efficiency Score
# ---------------------------------------------------------------------


def test_optimization_efficiency_score_perfect() -> None:
    score = _calculate_optimization_efficiency_score(
        sharpe_ratio=1.50,
        best_simulated_sharpe_ratio=1.50,
    )

    assert score == pytest.approx(100.0)


def test_optimization_efficiency_score_half() -> None:
    score = _calculate_optimization_efficiency_score(
        sharpe_ratio=0.75,
        best_simulated_sharpe_ratio=1.50,
    )

    assert score == pytest.approx(50.0)


def test_optimization_efficiency_score_is_clamped() -> None:
    score = _calculate_optimization_efficiency_score(
        sharpe_ratio=2.00,
        best_simulated_sharpe_ratio=1.50,
    )

    assert score == pytest.approx(100.0)

# ---------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------


@pytest.mark.parametrize(
    ("score", "summary"),
    [
        (
            95.0,
            "Excellent portfolio health.",
        ),
        (
            80.0,
            "Strong portfolio with manageable risk.",
        ),
        (
            65.0,
            "Moderate portfolio health with room for improvement.",
        ),
        (
            50.0,
            "Weak portfolio construction.",
        ),
        (
            20.0,
            "Poor portfolio health.",
        ),
    ],
)
def test_summary_generation(
    score: float,
    summary: str,
) -> None:
    assert (
        _generate_summary(score)
        == summary
    )


# ---------------------------------------------------------------------
# Recommendations
# ---------------------------------------------------------------------


def test_no_recommendations_needed() -> None:
    recommendations = (
        _generate_recommendations(
            diversification_score=90.0,
            concentration_score=90.0,
            risk_score=90.0,
            return_score=90.0,
        )
    )

    assert recommendations == (
        "Maintain the current portfolio strategy.",
    )


def test_all_recommendations_generated() -> None:
    recommendations = (
        _generate_recommendations(
            diversification_score=50.0,
            concentration_score=50.0,
            risk_score=50.0,
            return_score=50.0,
        )
    )

    assert len(recommendations) == 4

    assert (
        "Increase portfolio diversification."
        in recommendations
    )

    assert (
        "Reduce concentration in the largest holdings."
        in recommendations
    )

    assert (
        "Reduce downside portfolio risk."
        in recommendations
    )

    assert (
        "Seek higher expected risk-adjusted returns."
        in recommendations
    )


# ---------------------------------------------------------------------
# Complete Engine
# ---------------------------------------------------------------------


def test_analyze_portfolio_health_returns_domain_model() -> None:
    result = analyze_portfolio_health(
        expected_return=0.15,
        volatility=0.18,
        sharpe_ratio=1.5,
        best_simulated_sharpe_ratio=1.60,
        sortino_ratio=2.0,
        maximum_drawdown=0.12,
        value_at_risk=0.05,
        conditional_value_at_risk=0.08,
        weights=[0.40, 0.35, 0.25],
    )

    assert isinstance(
        result,
        PortfolioHealthResult,
    )

    assert (
        0.0
        <= result.overall_health_score
        <= 100.0
    )

    assert (
        0.0
        <= result.return_score
        <= 100.0
    )

    assert (
        0.0
        <= result.risk_score
        <= 100.0
    )

    assert (
        0.0
        <= result.diversification_score
        <= 100.0
    )

    assert (
        0.0
        <= result.concentration_score
        <= 100.0
    )
    
    assert (
        0.0
        <= result.optimization_efficiency_score
        <= 100.0
    )

    assert isinstance(
        result.summary,
        str,
    )

    assert isinstance(
        result.recommendations,
        tuple,
    )


def test_analyze_portfolio_health_is_deterministic() -> None:
    kwargs = dict(
        expected_return=0.12,
        volatility=0.20,
        sharpe_ratio=1.2,
        best_simulated_sharpe_ratio=1.60,
        sortino_ratio=1.8,
        maximum_drawdown=0.18,
        value_at_risk=0.07,
        conditional_value_at_risk=0.10,
        weights=[0.40, 0.35, 0.25],
    )

    first = analyze_portfolio_health(
        **kwargs
    )

    second = analyze_portfolio_health(
        **kwargs
    )

    assert first == second


def test_excellent_portfolio_scores_high() -> None:
    result = analyze_portfolio_health(
        expected_return=0.25,
        volatility=0.12,
        sharpe_ratio=2.0,
        best_simulated_sharpe_ratio=1.60,
        sortino_ratio=2.5,
        maximum_drawdown=0.05,
        value_at_risk=0.02,
        conditional_value_at_risk=0.03,
        weights=[0.25, 0.25, 0.25, 0.25],
    )

    assert result.overall_health_score > 80.0


def test_poor_portfolio_scores_low() -> None:
    result = analyze_portfolio_health(
        expected_return=-0.05,
        volatility=0.45,
        sharpe_ratio=0.10,
        best_simulated_sharpe_ratio=1.60,
        sortino_ratio=0.20,
        maximum_drawdown=0.45,
        value_at_risk=0.18,
        conditional_value_at_risk=0.25,
        weights=[0.85, 0.10, 0.05],
    )

    assert result.overall_health_score < 40.0