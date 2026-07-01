from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from app.financial_engines.risk.validation import (
    DEFAULT_CONFIDENCE_LEVEL,
    validate_confidence_level,
    validate_return_series,
    validate_risk_free_rate,
    validate_risk_inputs,
)


@pytest.fixture
def returns() -> pd.Series:
    return pd.Series(
        [0.01, -0.02, 0.015, 0.005],
        name="portfolio_returns",
    )


def test_validate_return_series_success(
    returns: pd.Series,
) -> None:
    result = validate_return_series(
        returns,
    )

    pd.testing.assert_series_equal(
        result,
        returns,
    )


def test_validate_return_series_empty() -> None:
    with pytest.raises(
        ValueError,
        match="Portfolio returns are empty.",
    ):
        validate_return_series(
            pd.Series(dtype=float),
        )


def test_validate_return_series_all_nan() -> None:
    with pytest.raises(
        ValueError,
        match="Portfolio returns contain no usable observations.",
    ):
        validate_return_series(
            pd.Series(
                [np.nan, np.nan],
            ),
        )


def test_validate_return_series_too_few_observations() -> None:
    with pytest.raises(
        ValueError,
        match=(
            "At least two observations are required "
            "for risk analysis."
        ),
    ):
        validate_return_series(
            pd.Series([0.02]),
        )


def test_validate_return_series_non_numeric() -> None:
    with pytest.raises(
        ValueError,
        match=(
            "Portfolio returns must contain only "
            "numeric values."
        ),
    ):
        validate_return_series(
            pd.Series(
                ["A", "B"],
            ),
        )


def test_validate_return_series_non_finite() -> None:
    with pytest.raises(
        ValueError,
        match=(
            "Portfolio returns contain "
            "non-finite values."
        ),
    ):
        validate_return_series(
            pd.Series(
                [0.01, np.inf],
            ),
        )


def test_validate_risk_free_rate_success() -> None:
    validate_risk_free_rate(
        0.02,
    )


def test_validate_risk_free_rate_nan() -> None:
    with pytest.raises(
        ValueError,
        match="Risk-free rate must be a finite number.",
    ):
        validate_risk_free_rate(
            np.nan,
        )


def test_validate_risk_free_rate_infinite() -> None:
    with pytest.raises(
        ValueError,
        match="Risk-free rate must be a finite number.",
    ):
        validate_risk_free_rate(
            np.inf,
        )


def test_validate_confidence_level_success() -> None:
    validate_confidence_level(
        DEFAULT_CONFIDENCE_LEVEL,
    )


@pytest.mark.parametrize(
    "confidence_level",
    [
        0.0,
        1.0,
        -0.1,
        1.2,
    ],
)
def test_validate_confidence_level_invalid_range(
    confidence_level: float,
) -> None:
    with pytest.raises(
        ValueError,
        match=(
            "Confidence level must be between 0 and 1."
        ),
    ):
        validate_confidence_level(
            confidence_level,
        )


def test_validate_confidence_level_non_finite() -> None:
    with pytest.raises(
        ValueError,
        match=(
            "Confidence level must be a finite number."
        ),
    ):
        validate_confidence_level(
            np.nan,
        )


def test_validate_risk_inputs_success(
    returns: pd.Series,
) -> None:
    result = validate_risk_inputs(
        returns,
        risk_free_rate=0.02,
        confidence_level=0.95,
    )

    pd.testing.assert_series_equal(
        result,
        returns,
    )