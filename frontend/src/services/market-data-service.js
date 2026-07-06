import { apiRequest } from "./api-client";

function buildMarketDataQuery({ tickers, start, end }) {
  const searchParams = new URLSearchParams({
    tickers: tickers.join(","),
    start,
    end,
  });

  return searchParams.toString();
}

export async function getHistoricalPrices({ tickers, start, end }) {
  const query = buildMarketDataQuery({ tickers, start, end });
  return apiRequest(`/market-data/history?${query}`);
}

export async function getDailyReturns({ tickers, start, end }) {
  const query = buildMarketDataQuery({ tickers, start, end });
  return apiRequest(`/market-data/returns?${query}`);
}