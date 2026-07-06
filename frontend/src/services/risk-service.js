import { apiRequest } from "./api-client";

export async function analyzePortfolioRisk({
  tickers,
  weights,
  start,
  end,
  riskFreeRate,
  confidenceLevel,
}) {
  return apiRequest("/risk", {
    method: "POST",
    body: {
      tickers,
      weights,
      start,
      end,
      risk_free_rate: Number(riskFreeRate),
      confidence_level: Number(confidenceLevel),
    },
  });
}