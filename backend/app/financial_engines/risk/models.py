"""
Immutable domain models for the Risk Analytics Financial Engine.

These models represent the outputs produced by the Risk Analytics Engine
and provide a stable interface between the Financial Engine and higher
architectural layers.

The models are intentionally framework-independent and contain no
business logic.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class RiskAnalyticsResult:
    """
    Immutable collection of portfolio risk metrics.

    Attributes
    ----------
    sharpe_ratio:
        Annualized Sharpe ratio.

    sortino_ratio:
        Annualized Sortino ratio.

    maximum_drawdown:
        Maximum historical portfolio drawdown expressed as a decimal.

    value_at_risk:
        Historical Value-at-Risk (VaR) at the selected confidence level,
        expressed as a positive loss.

    conditional_value_at_risk:
        Historical Conditional Value-at-Risk (CVaR), also known as
        Expected Shortfall, expressed as a positive loss.
    """

    sharpe_ratio: float
    sortino_ratio: float
    maximum_drawdown: float
    value_at_risk: float
    conditional_value_at_risk: float