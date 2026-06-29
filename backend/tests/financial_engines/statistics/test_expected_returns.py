import pandas as pd
import pytest

from app.financial_engines.statistics.expected_returns import (
    calculate_expected_annual_returns,
    calculate_mean_daily_returns,
)


@pytest.fixture
def sample_returns() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "AAPL": [0.01, 0.02, -0.01, 0.03],
            "MSFT": [0.005, 0.01, 0.0, 0.015],
        }
    )


def test_calculate_mean_daily_returns(sample_returns):
    result = calculate_mean_daily_returns(sample_returns)

    assert isinstance(result, pd.Series)
    assert result.index.tolist() == ["AAPL", "MSFT"]


def test_calculate_expected_annual_returns(sample_returns):
    result = calculate_expected_annual_returns(sample_returns)

    assert isinstance(result, pd.Series)

    expected = sample_returns.mean() * 252

    pd.testing.assert_series_equal(
        result,
        expected,
    )


def test_expected_returns_empty_dataframe():
    with pytest.raises(ValueError):
        calculate_expected_annual_returns(
            pd.DataFrame()
        )