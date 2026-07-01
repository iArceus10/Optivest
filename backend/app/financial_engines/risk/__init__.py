"""
Risk Analytics Financial Engine.

This package provides deterministic, framework-independent portfolio
risk metrics for evaluating historical portfolio performance.

Public API:

- RiskAnalyticsResult
- calculate_sharpe_ratio
- calculate_sortino_ratio
- calculate_maximum_drawdown
- calculate_historical_value_at_risk
- calculate_historical_conditional_value_at_risk
"""

from .drawdown import (
    calculate_maximum_drawdown,
)
from .models import (
    RiskAnalyticsResult,
)
from .validation import (
    DEFAULT_CONFIDENCE_LEVEL,
)
from .ratios import (
    calculate_sharpe_ratio,
    calculate_sortino_ratio,
)
from .value_at_risk import (
    calculate_historical_conditional_value_at_risk,
    calculate_historical_value_at_risk,
)


def calculate_risk_metrics(
    returns,
    *,
    risk_free_rate: float = 0.02,
    confidence_level: float = DEFAULT_CONFIDENCE_LEVEL,
) -> RiskAnalyticsResult:
    """
    Compute the complete collection of portfolio risk metrics.

    Parameters
    ----------
    returns:
        Historical portfolio return series.

    risk_free_rate:
        Annualized risk-free rate.

    confidence_level:
        Confidence level used for VaR and CVaR.

    Returns
    -------
    RiskAnalyticsResult
        Immutable collection of portfolio risk metrics.
    """

    return RiskAnalyticsResult(
        sharpe_ratio=calculate_sharpe_ratio(
            returns,
            risk_free_rate=risk_free_rate,
        ),
        sortino_ratio=calculate_sortino_ratio(
            returns,
            risk_free_rate=risk_free_rate,
        ),
        maximum_drawdown=calculate_maximum_drawdown(
            returns,
        ),
        value_at_risk=calculate_historical_value_at_risk(
            returns,
            confidence_level=confidence_level,
        ),
        conditional_value_at_risk=(
            calculate_historical_conditional_value_at_risk(
                returns,
                confidence_level=confidence_level,
            )
        ),
    )



__all__ = [
    "RiskAnalyticsResult",
    "calculate_sharpe_ratio",
    "calculate_sortino_ratio",
    "calculate_maximum_drawdown",
    "calculate_historical_value_at_risk",
    "calculate_historical_conditional_value_at_risk",
    "calculate_risk_metrics",
]