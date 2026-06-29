import pandas as pd
import pytest

from app.financial_engines.market_data.validation import (
    validate_price_data,
)


def test_valid_dataframe():
    prices = pd.DataFrame(
        {
            "AAPL": [100, 101],
        }
    )

    validate_price_data(prices)


def test_empty_dataframe():
    with pytest.raises(ValueError):
        validate_price_data(pd.DataFrame())


def test_all_nan_dataframe():
    prices = pd.DataFrame(
        {
            "AAPL": [None, None],
        }
    )

    with pytest.raises(ValueError):
        validate_price_data(prices)


def test_insufficient_rows():
    prices = pd.DataFrame(
        {
            "AAPL": [100],
        }
    )

    with pytest.raises(ValueError):
        validate_price_data(prices)