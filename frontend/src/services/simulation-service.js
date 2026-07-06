import { apiRequest } from "./api-client";

export async function runMonteCarloSimulation({
  tickers,
  start,
  end,
  simulationCount,
  riskFreeRate,
  seed,
}) {
  const body = {
    tickers,
    start,
    end,
    simulation_count: Number(simulationCount),
    risk_free_rate: Number(riskFreeRate),
  };

  if (seed !== "" && seed !== null && seed !== undefined) {
    body.seed = Number(seed);
  }

  return apiRequest("/simulation", {
    method: "POST",
    body,
  });
}