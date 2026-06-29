import pandas as pd
import pytest

from app.financial_engines.statistics.covariance import (
    calculate_annualized_covariance_matrix,
    calculate_daily_covariance_matrix,
)


@pytest.fixture
def sample_returns():
    return pd.DataFrame(
        {
            "AAPL": [0.01, 0.02, -0.01, 0.03],
            "MSFT": [0.005, 0.01, 0.0, 0.015],
        }
    )


def test_daily_covariance(sample_returns):
    result = calculate_daily_covariance_matrix(
        sample_returns
    )

    pd.testing.assert_frame_equal(
        result,
        sample_returns.cov(),
    )


def test_annualized_covariance(sample_returns):
    result = calculate_annualized_covariance_matrix(
        sample_returns
    )

    pd.testing.assert_frame_equal(
        result,
        sample_returns.cov() * 252,
    )


def test_covariance_empty_dataframe():
    with pytest.raises(ValueError):
        calculate_daily_covariance_matrix(
            pd.DataFrame()
        )