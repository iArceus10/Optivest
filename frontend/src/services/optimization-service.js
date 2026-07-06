import { apiRequest } from "./api-client";

export async function runMeanVarianceOptimization({
  tickers,
  start,
  end,
  riskAversion,
}) {
  return apiRequest("/optimization/mean-variance", {
    method: "POST",
    body: {
      tickers,
      start,
      end,
      risk_aversion: Number(riskAversion),
    },
  });
}

export async function runMinimumVarianceOptimization({
  tickers,
  start,
  end,
}) {
  return apiRequest("/optimization/minimum-variance", {
    method: "POST",
    body: {
      tickers,
      start,
      end,
    },
  });
}

export async function runMaximumSharpeOptimization({
  tickers,
  start,
  end,
  riskFreeRate,
}) {
  return apiRequest("/optimization/maximum-sharpe", {
    method: "POST",
    body: {
      tickers,
      start,
      end,
      risk_free_rate: Number(riskFreeRate),
    },
  });
}

export async function runEfficientFrontier({
  tickers,
  start,
  end,
  numPoints,
}) {
  return apiRequest("/optimization/efficient-frontier", {
    method: "POST",
    body: {
      tickers,
      start,
      end,
      num_points: Number(numPoints),
    },
  });
}