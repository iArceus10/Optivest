import { apiRequest } from "./api-client";

export async function analyzePortfolioHealth(payload) {
  return apiRequest("/portfolio-health", {
    method: "POST",
    body: {
      tickers: payload.tickers,
      weights: payload.weights,
      start: payload.start,
      end: payload.end,
      risk_free_rate: payload.riskFreeRate,
      simulation_count: payload.simulationCount,
      seed: payload.seed === "" ? null : payload.seed,
    },
  });
}