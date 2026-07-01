"""
Portfolio Health Financial Engine.

This module synthesizes outputs from the Statistics, Optimization,
Simulation, and Risk Analytics engines into deterministic portfolio
health diagnostics.

The implementation performs no statistical estimation or financial
modelling. Instead, it evaluates already-computed portfolio metrics and
returns normalized health scores together with deterministic investment
insights.
"""

from __future__ import annotations

from app.financial_engines.portfolio_health.models import (
    PortfolioHealthResult,
)
from app.financial_engines.portfolio_health.validation import (
    validate_portfolio_health_inputs,
)


def _calculate_return_score(
    expected_return: float,
) -> float:
    """
    Calculate a return score on a 0–100 scale.
    """

    if expected_return >= 0.20:
        return 100.0

    if expected_return >= 0.15:
        return 85.0

    if expected_return >= 0.10:
        return 70.0

    if expected_return >= 0.05:
        return 50.0

    if expected_return >= 0.00:
        return 30.0

    return 0.0


def _calculate_risk_score(
    *,
    sharpe_ratio: float,
    maximum_drawdown: float,
    value_at_risk: float,
) -> float:
    """
    Calculate a composite portfolio risk score.

    Higher Sharpe Ratios improve the score while larger drawdowns and
    Value-at-Risk reduce it.
    """

    sharpe_component = min(
        max(sharpe_ratio / 2.0, 0.0),
        1.0,
    )

    drawdown_penalty = min(
        maximum_drawdown / 0.50,
        1.0,
    )

    var_penalty = min(
        value_at_risk / 0.20,
        1.0,
    )

    score = (
        100.0
        * (
            0.50 * sharpe_component
            + 0.30 * (1.0 - drawdown_penalty)
            + 0.20 * (1.0 - var_penalty)
        )
    )

    return max(
        0.0,
        min(score, 100.0),
    )


def _calculate_diversification_score(
    weights: list[float],
) -> float:
    """
    Calculate a diversification score using the Herfindahl-Hirschman
    Index (HHI).

    Lower concentration corresponds to better diversification.
    """

    hhi = sum(
        weight * weight
        for weight in weights
    )

    minimum_hhi = 1.0 / len(weights)

    if minimum_hhi >= 1.0:
        return 0.0

    normalized_hhi = (
        hhi - minimum_hhi
    ) / (
        1.0 - minimum_hhi
    )

    score = 100.0 * (
        1.0 - normalized_hhi
    )

    return max(
        0.0,
        min(score, 100.0),
    )


def _calculate_concentration_score(
    weights: list[float],
) -> float:
    """
    Calculate a concentration score based on the largest portfolio
    allocation.
    """

    largest_weight = max(weights)

    if largest_weight <= 0.20:
        return 100.0

    if largest_weight <= 0.30:
        return 80.0

    if largest_weight <= 0.40:
        return 60.0

    if largest_weight <= 0.50:
        return 40.0

    return 20.0


def _generate_summary(
    overall_health_score: float,
) -> str:
    """
    Generate a deterministic portfolio health summary.
    """

    if overall_health_score >= 90.0:
        return "Excellent portfolio health."

    if overall_health_score >= 75.0:
        return (
            "Strong portfolio with manageable risk."
        )

    if overall_health_score >= 60.0:
        return (
            "Moderate portfolio health with room for improvement."
        )

    if overall_health_score >= 40.0:
        return (
            "Weak portfolio construction."
        )

    return "Poor portfolio health."


def _generate_recommendations(
    *,
    diversification_score: float,
    concentration_score: float,
    risk_score: float,
    return_score: float,
) -> tuple[str, ...]:
    """
    Generate deterministic portfolio recommendations.
    """

    recommendations: list[str] = []

    if diversification_score < 70.0:
        recommendations.append(
            "Increase portfolio diversification."
        )

    if concentration_score < 70.0:
        recommendations.append(
            "Reduce concentration in the largest holdings."
        )

    if risk_score < 70.0:
        recommendations.append(
            "Reduce downside portfolio risk."
        )

    if return_score < 70.0:
        recommendations.append(
            "Seek higher expected risk-adjusted returns."
        )

    if not recommendations:
        recommendations.append(
            "Maintain the current portfolio strategy."
        )

    return tuple(recommendations)


def analyze_portfolio_health(
    *,
    expected_return: float,
    volatility: float,
    sharpe_ratio: float,
    sortino_ratio: float,
    maximum_drawdown: float,
    value_at_risk: float,
    conditional_value_at_risk: float,
    weights: list[float],
) -> PortfolioHealthResult:
    """
    Compute deterministic portfolio health diagnostics.
    """

    validate_portfolio_health_inputs(
        expected_return=expected_return,
        volatility=volatility,
        sharpe_ratio=sharpe_ratio,
        sortino_ratio=sortino_ratio,
        maximum_drawdown=maximum_drawdown,
        value_at_risk=value_at_risk,
        conditional_value_at_risk=conditional_value_at_risk,
        weights=weights,
    )

    return_score = _calculate_return_score(
        expected_return,
    )

    risk_score = _calculate_risk_score(
        sharpe_ratio=sharpe_ratio,
        maximum_drawdown=maximum_drawdown,
        value_at_risk=value_at_risk,
    )

    diversification_score = (
        _calculate_diversification_score(
            weights,
        )
    )

    concentration_score = (
        _calculate_concentration_score(
            weights,
        )
    )

    overall_health_score = (
        0.25 * return_score
        + 0.35 * risk_score
        + 0.20 * diversification_score
        + 0.20 * concentration_score
    )

    summary = _generate_summary(
        overall_health_score,
    )

    recommendations = (
        _generate_recommendations(
            diversification_score=diversification_score,
            concentration_score=concentration_score,
            risk_score=risk_score,
            return_score=return_score,
        )
    )

    return PortfolioHealthResult(
        overall_health_score=overall_health_score,
        return_score=return_score,
        risk_score=risk_score,
        diversification_score=diversification_score,
        concentration_score=concentration_score,
        summary=summary,
        recommendations=recommendations,
    )