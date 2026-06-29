from __future__ import annotations

from datetime import date

import pandas as pd
from fastapi import APIRouter, HTTPException, Query, status

from app.schemas.market_data import (
    DailyReturnRecord,
    DailyReturnsResponse,
    HistoricalPriceRecord,
    HistoricalPricesResponse,
)
from app.services.market_data_service import MarketDataService

router = APIRouter(
    prefix="/market-data",
    tags=["Market Data"],
)


def _parse_tickers(
    tickers: str,
) -> list[str]:
    """
    Parse a comma-separated ticker string into a cleaned list.
    """

    return [
        ticker.strip()
        for ticker in tickers.split(",")
        if ticker.strip()
    ]


def _serialize_prices(
    prices: pd.DataFrame,
) -> HistoricalPricesResponse:
    """
    Convert a historical price DataFrame into an API response.
    """

    records = [
        HistoricalPriceRecord(
            date=index.date(),
            values=row.to_dict(),
        )
        for index, row in prices.iterrows()
    ]

    return HistoricalPricesResponse(
        tickers=list(prices.columns),
        records=records,
    )


def _serialize_returns(
    returns: pd.DataFrame,
) -> DailyReturnsResponse:
    """
    Convert a daily returns DataFrame into an API response.
    """

    records = [
        DailyReturnRecord(
            date=index.date(),
            values=row.to_dict(),
        )
        for index, row in returns.iterrows()
    ]

    return DailyReturnsResponse(
        tickers=list(returns.columns),
        records=records,
    )


@router.get(
    "/history",
    response_model=HistoricalPricesResponse,
    summary="Retrieve historical adjusted closing prices",
)
def get_historical_prices(
    tickers: str = Query(
        ...,
        description="Comma-separated ticker symbols (e.g. AAPL,MSFT,NVDA).",
        examples=["AAPL,MSFT,NVDA"],
    ),
    start: date = Query(
        ...,
        description="Inclusive start date (YYYY-MM-DD).",
    ),
    end: date = Query(
        ...,
        description="Exclusive end date (YYYY-MM-DD).",
    ),
) -> HistoricalPricesResponse:
    """
    Retrieve historical adjusted closing prices for one or more assets.
    """

    try:
        dataframe = MarketDataService.get_historical_prices(
            tickers=_parse_tickers(tickers),
            start=start,
            end=end,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    return _serialize_prices(dataframe)


@router.get(
    "/returns",
    response_model=DailyReturnsResponse,
    summary="Retrieve historical daily returns",
)
def get_daily_returns(
    tickers: str = Query(
        ...,
        description="Comma-separated ticker symbols (e.g. AAPL,MSFT,NVDA).",
        examples=["AAPL,MSFT,NVDA"],
    ),
    start: date = Query(
        ...,
        description="Inclusive start date (YYYY-MM-DD).",
    ),
    end: date = Query(
        ...,
        description="Exclusive end date (YYYY-MM-DD).",
    ),
) -> DailyReturnsResponse:
    """
    Retrieve historical daily percentage returns for one or more assets.
    """

    try:
        dataframe = MarketDataService.get_daily_returns(
            tickers=_parse_tickers(tickers),
            start=start,
            end=end,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    return _serialize_returns(dataframe)