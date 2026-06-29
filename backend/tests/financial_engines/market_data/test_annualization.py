import math

from app.financial_engines.market_data.annualization import (
    TRADING_DAYS_PER_YEAR,
    annualize_mean_return,
    annualize_volatility,
)


def test_annualize_mean_return():
    daily_return = 0.001

    annual_return = annualize_mean_return(daily_return)

    assert annual_return == daily_return * TRADING_DAYS_PER_YEAR


def test_annualize_zero_return():
    assert annualize_mean_return(0.0) == 0.0


def test_annualize_volatility():
    daily_volatility = 0.02

    annual_volatility = annualize_volatility(daily_volatility)

    expected = daily_volatility * math.sqrt(TRADING_DAYS_PER_YEAR)

    assert math.isclose(
        annual_volatility,
        expected,
        rel_tol=1e-9,
    )


def test_zero_volatility():
    assert annualize_volatility(0.0) == 0.0