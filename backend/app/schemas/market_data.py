from __future__ import annotations

from datetime import date

from pydantic import BaseModel


class HistoricalPriceRecord(BaseModel):
    """
    Historical adjusted close prices for a single trading day.
    """

    date: date

    values: dict[str, float]


class HistoricalPricesResponse(BaseModel):
    """
    Historical adjusted close prices for one or more assets.
    """

    tickers: list[str]

    records: list[HistoricalPriceRecord]


class DailyReturnRecord(BaseModel):
    """
    Daily percentage returns for a single trading day.
    """

    date: date

    values: dict[str, float]


class DailyReturnsResponse(BaseModel):
    """
    Historical daily returns for one or more assets.
    """

    tickers: list[str]

    records: list[DailyReturnRecord]