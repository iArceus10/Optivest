from __future__ import annotations

from dataclasses import FrozenInstanceError

import pytest

from app.financial_engines.risk.models import (
    RiskAnalyticsResult,
)


def test_risk_analytics_result_fields() -> None:
    result = RiskAnalyticsResult(
        sharpe_ratio=1.24,
        sortino_ratio=1.81,
        maximum_drawdown=0.18,
        value_at_risk=0.07,
        conditional_value_at_risk=0.11,
    )

    assert result.sharpe_ratio == pytest.approx(1.24)
    assert result.sortino_ratio == pytest.approx(1.81)
    assert result.maximum_drawdown == pytest.approx(0.18)
    assert result.value_at_risk == pytest.approx(0.07)
    assert (
        result.conditional_value_at_risk
        == pytest.approx(0.11)
    )


def test_risk_analytics_result_is_immutable() -> None:
    result = RiskAnalyticsResult(
        sharpe_ratio=1.0,
        sortino_ratio=1.2,
        maximum_drawdown=0.15,
        value_at_risk=0.05,
        conditional_value_at_risk=0.08,
    )

    with pytest.raises(FrozenInstanceError):
        result.sharpe_ratio = 2.0  # type: ignore[misc]