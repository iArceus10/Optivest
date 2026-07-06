import { apiRequest } from "./api-client";

function buildQueryString(params) {
  const searchParams = new URLSearchParams();

  Object.entries(params).forEach(([key, value]) => {
    if (Array.isArray(value)) {
      value.forEach((item) => {
        searchParams.append(key, item);
      });
      return;
    }

    if (value !== undefined && value !== null && value !== "") {
      searchParams.append(key, String(value));
    }
  });

  return searchParams.toString();
}

export async function getExpectedReturns({ tickers, start, end }) {
  const query = buildQueryString({
    tickers,
    start,
    end,
  });

  return apiRequest(`/statistics/returns?${query}`);
}

export async function getCovarianceMatrix({ tickers, start, end }) {
  const query = buildQueryString({
    tickers,
    start,
    end,
  });

  return apiRequest(`/statistics/covariance?${query}`);
}

export async function getCorrelationMatrix({ tickers, start, end }) {
  const query = buildQueryString({
    tickers,
    start,
    end,
  });

  return apiRequest(`/statistics/correlation?${query}`);
}

export async function getPortfolioVolatility({
  tickers,
  weights,
  start,
  end,
}) {
  const query = buildQueryString({
    tickers,
    weights,
    start,
    end,
  });

  return apiRequest(`/statistics/volatility?${query}`);
}