import numpy as np
import pandas as pd
import pytest

from app.financial_engines.statistics.volatility import (
    calculate_portfolio_volatility,
)


@pytest.fixture
def sample_returns():
    return pd.DataFrame(
        {
            "AAPL": [0.01, 0.02, -0.01, 0.03],
            "MSFT": [0.005, 0.01, 0.0, 0.015],
        }
    )


def test_portfolio_volatility(sample_returns):
    weights = np.array([0.5, 0.5])

    result = calculate_portfolio_volatility(
        sample_returns,
        weights,
    )

    assert isinstance(result, float)
    assert result >= 0


def test_weights_wrong_length(sample_returns):
    with pytest.raises(ValueError):
        calculate_portfolio_volatility(
            sample_returns,
            np.array([1.0]),
        )


def test_weights_not_sum_to_one(sample_returns):
    with pytest.raises(ValueError):
        calculate_portfolio_volatility(
            sample_returns,
            np.array([0.7, 0.7]),
        )


def test_nan_weights(sample_returns):
    with pytest.raises(ValueError):
        calculate_portfolio_volatility(
            sample_returns,
            np.array([0.5, np.nan]),
        )