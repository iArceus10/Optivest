from __future__ import annotations

import pytest

from app.financial_engines.portfolio_health.validation import (
    validate_portfolio_health_inputs,
)


@pytest.fixture
def valid_inputs() -> dict[str, object]:
    return {
        "expected_return": 0.12,
        "volatility": 0.18,
        "sharpe_ratio": 1.30,
        "best_simulated_sharpe_ratio": 1.60,
        "sortino_ratio": 1.80,
        "maximum_drawdown": 0.15,
        "value_at_risk": 0.06,
        "conditional_value_at_risk": 0.09,
        "weights": [0.40, 0.35, 0.25],
    }


def test_validate_portfolio_health_inputs_success(
    valid_inputs: dict[str, object],
) -> None:
    validate_portfolio_health_inputs(
        **valid_inputs,
    )


@pytest.mark.parametrize(
    ("field", "value", "message"),
    [
        (
            "expected_return",
            float("nan"),
            "Expected return must be a finite number.",
        ),
        (
            "volatility",
            float("inf"),
            "Volatility must be a finite number.",
        ),
        (
            "sharpe_ratio",
            float("nan"),
            "Sharpe ratio must be a finite number.",
        ),
        (
            "sortino_ratio",
            float("-inf"),
            "Sortino ratio must be a finite number.",
        ),
    ],
)
def test_non_finite_numeric_inputs(
    valid_inputs: dict[str, object],
    field: str,
    value: float,
    message: str,
) -> None:
    valid_inputs[field] = value

    with pytest.raises(
        ValueError,
        match=message,
    ):
        validate_portfolio_health_inputs(
            **valid_inputs,
        )


def test_negative_volatility(
    valid_inputs: dict[str, object],
) -> None:
    valid_inputs["volatility"] = -0.10

    with pytest.raises(
        ValueError,
        match="Volatility cannot be negative.",
    ):
        validate_portfolio_health_inputs(
            **valid_inputs,
        )


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("maximum_drawdown", -0.01),
        ("maximum_drawdown", 1.10),
        ("value_at_risk", -0.01),
        ("value_at_risk", 1.20),
        ("conditional_value_at_risk", -0.01),
        ("conditional_value_at_risk", 1.10),
    ],
)
def test_probability_metrics_out_of_range(
    valid_inputs: dict[str, object],
    field: str,
    value: float,
) -> None:
    valid_inputs[field] = value

    with pytest.raises(
        ValueError,
        match="must be between 0 and 1.",
    ):
        validate_portfolio_health_inputs(
            **valid_inputs,
        )


def test_cvar_less_than_var(
    valid_inputs: dict[str, object],
) -> None:
    valid_inputs["value_at_risk"] = 0.10
    valid_inputs["conditional_value_at_risk"] = 0.08

    with pytest.raises(
        ValueError,
        match=(
            "Conditional Value-at-Risk "
            "must be greater than or equal "
            "to Value-at-Risk."
        ),
    ):
        validate_portfolio_health_inputs(
            **valid_inputs,
        )


def test_empty_weights() -> None:
    with pytest.raises(
        ValueError,
        match="Portfolio weights cannot be empty.",
    ):
        validate_portfolio_health_inputs(
            expected_return=0.10,
            volatility=0.15,
            sharpe_ratio=1.20,
            best_simulated_sharpe_ratio=1.50,
            sortino_ratio=1.60,
            maximum_drawdown=0.12,
            value_at_risk=0.05,
            conditional_value_at_risk=0.08,
            weights=[],
        )


def test_negative_weight(
    valid_inputs: dict[str, object],
) -> None:
    valid_inputs["weights"] = [0.60, -0.10, 0.50]

    with pytest.raises(
        ValueError,
        match=(
            "Portfolio weights cannot contain "
            "negative values."
        ),
    ):
        validate_portfolio_health_inputs(
            **valid_inputs,
        )


def test_non_finite_weight(
    valid_inputs: dict[str, object],
) -> None:
    valid_inputs["weights"] = [
        0.50,
        float("nan"),
        0.50,
    ]

    with pytest.raises(
        ValueError,
        match=(
            "Portfolio weights must contain "
            "only finite values."
        ),
    ):
        validate_portfolio_health_inputs(
            **valid_inputs,
        )


def test_weights_do_not_sum_to_one(
    valid_inputs: dict[str, object],
) -> None:
    valid_inputs["weights"] = [
        0.40,
        0.40,
        0.40,
    ]

    with pytest.raises(
        ValueError,
        match="Portfolio weights must sum to 1.",
    ):
        validate_portfolio_health_inputs(
            **valid_inputs,
        )

def test_best_simulated_sharpe_must_be_positive(
    valid_inputs: dict[str, object],
) -> None:
    valid_inputs[
        "best_simulated_sharpe_ratio"
    ] = 0.0

    with pytest.raises(
        ValueError,
        match=(
            "Best simulated Sharpe ratio "
            "must be positive."
        ),
    ):
        validate_portfolio_health_inputs(
            **valid_inputs,
        )