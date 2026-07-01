from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from app.financial_engines.simulation.validation import (
    validate_random_seed,
    validate_risk_free_rate,
    validate_simulation_count,
    validate_simulation_inputs,
)


@pytest.fixture
def expected_returns() -> pd.Series:
    return pd.Series(
        [0.10, 0.15],
        index=["AAPL", "MSFT"],
    )


@pytest.fixture
def covariance_matrix() -> pd.DataFrame:
    return pd.DataFrame(
        [
            [0.04, 0.01],
            [0.01, 0.09],
        ],
        index=["AAPL", "MSFT"],
        columns=["AAPL", "MSFT"],
    )


def test_validate_simulation_inputs_success(
    expected_returns: pd.Series,
    covariance_matrix: pd.DataFrame,
) -> None:
    validate_simulation_inputs(
        expected_returns,
        covariance_matrix,
        simulation_count=1000,
        risk_free_rate=0.02,
        seed=42,
    )


def test_validate_simulation_count_zero() -> None:
    with pytest.raises(
        ValueError,
        match="Simulation count must be greater than zero.",
    ):
        validate_simulation_count(0)


def test_validate_simulation_count_negative() -> None:
    with pytest.raises(
        ValueError,
        match="Simulation count must be greater than zero.",
    ):
        validate_simulation_count(-10)


def test_validate_risk_free_rate_nan() -> None:
    with pytest.raises(
        ValueError,
        match="Risk-free rate must be a finite number.",
    ):
        validate_risk_free_rate(np.nan)


def test_validate_risk_free_rate_infinite() -> None:
    with pytest.raises(
        ValueError,
        match="Risk-free rate must be a finite number.",
    ):
        validate_risk_free_rate(np.inf)


def test_validate_random_seed_none() -> None:
    validate_random_seed(None)


def test_validate_random_seed_integer() -> None:
    validate_random_seed(123)


def test_validate_random_seed_invalid_type() -> None:
    with pytest.raises(
        ValueError,
        match="Random seed must be an integer or None.",
    ):
        validate_random_seed("42")  # type: ignore[arg-type]


def test_validate_simulation_inputs_non_finite_expected_returns(
    covariance_matrix: pd.DataFrame,
) -> None:
    expected_returns = pd.Series(
        [0.10, np.inf],
        index=["AAPL", "MSFT"],
    )

    with pytest.raises(
        ValueError,
        match="Expected returns contain non-finite values.",
    ):
        validate_simulation_inputs(
            expected_returns,
            covariance_matrix,
            simulation_count=100,
            risk_free_rate=0.02,
            seed=None,
        )


def test_validate_simulation_inputs_non_finite_covariance(
    expected_returns: pd.Series,
) -> None:
    covariance = pd.DataFrame(
        [
            [0.04, np.nan],
            [0.01, 0.09],
        ],
        index=["AAPL", "MSFT"],
        columns=["AAPL", "MSFT"],
    )

    with pytest.raises(
        ValueError,
    ):
        validate_simulation_inputs(
            expected_returns,
            covariance,
            simulation_count=100,
            risk_free_rate=0.02,
            seed=None,
        )