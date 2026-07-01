"""
Immutable domain models for the Portfolio Health Financial Engine.

These models represent the synthesized portfolio diagnostics produced by
the Portfolio Health Engine.

The models are intentionally framework-independent and contain no
business logic. They provide a stable interface between the Financial
Engine and higher architectural layers.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class PortfolioHealthResult:
    """
    Immutable collection of portfolio health diagnostics.

    Attributes
    ----------
    overall_health_score:
        Overall portfolio health score on a 0–100 scale.

    return_score:
        Score reflecting the portfolio's expected return.

    risk_score:
        Score reflecting the portfolio's risk-adjusted performance and
        downside risk.

    diversification_score:
        Score reflecting diversification based on portfolio weights.

    concentration_score:
        Score reflecting concentration risk based on the largest
        portfolio allocation.

    summary:
        Deterministic textual summary of the overall portfolio health.

    recommendations:
        Deterministic recommendations for improving portfolio health.
    """

    overall_health_score: float
    return_score: float
    risk_score: float
    diversification_score: float
    concentration_score: float
    summary: str
    recommendations: tuple[str, ...]