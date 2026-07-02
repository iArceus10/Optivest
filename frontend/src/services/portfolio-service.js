import { apiRequest } from "./api-client";

export async function getPortfolios() {
  return apiRequest("/portfolios");
}

export async function createPortfolio({ name, description }) {
  return apiRequest("/portfolios", {
    method: "POST",
    body: {
      name,
      description,
    },
  });
}

export async function getPortfolioById(portfolioId) {
  return apiRequest(`/portfolios/${portfolioId}`);
}

export async function updatePortfolio(portfolioId, payload) {
  return apiRequest(`/portfolios/${portfolioId}`, {
    method: "PATCH",
    body: payload,
  });
}

export async function deletePortfolio(portfolioId) {
  return apiRequest(`/portfolios/${portfolioId}`, {
    method: "DELETE",
  });
}