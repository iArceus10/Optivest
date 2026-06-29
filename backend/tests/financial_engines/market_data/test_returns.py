import pandas as pd
import math

from app.financial_engines.market_data.returns import (
    calculate_daily_returns,
)


def test_daily_returns_shape():
    prices = pd.DataFrame(
        {
            "AAPL": [100, 110, 121],
            "MSFT": [50, 55, 60.5],
        }
    )

    returns = calculate_daily_returns(prices)

    assert returns.shape == (2, 2)


def test_daily_returns_values():
    prices = pd.DataFrame(
        {
            "AAPL": [100, 110, 121],
        }
    )

    returns = calculate_daily_returns(prices)

    assert math.isclose(
        returns.iloc[0, 0],
        0.10,
        rel_tol=1e-9,
    )

    assert math.isclose(
        returns.iloc[1, 0],
        0.10,
        rel_tol=1e-9,
    )


def test_returns_contains_no_nan():
    prices = pd.DataFrame(
        {
            "AAPL": [100, 105, 110],
        }
    )

    returns = calculate_daily_returns(prices)

    assert not returns.isna().any().any()