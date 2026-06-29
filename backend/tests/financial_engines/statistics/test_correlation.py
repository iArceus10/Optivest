import pandas as pd
import pytest

from app.financial_engines.statistics.correlation import (
    calculate_correlation_matrix,
)


@pytest.fixture
def sample_returns():
    return pd.DataFrame(
        {
            "AAPL": [0.01, 0.02, -0.01, 0.03],
            "MSFT": [0.005, 0.01, 0.0, 0.015],
        }
    )


def test_correlation_matrix(sample_returns):
    result = calculate_correlation_matrix(
        sample_returns
    )

    pd.testing.assert_frame_equal(
        result,
        sample_returns.corr(),
    )


def test_correlation_empty_dataframe():
    with pytest.raises(ValueError):
        calculate_correlation_matrix(
            pd.DataFrame()
        )