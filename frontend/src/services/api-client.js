import { getStoredAccessToken } from "../utils/auth-storage";
import { API_BASE_URL } from "../utils/constants";

function buildHeaders(extraHeaders = {}, hasBody = false) {
  const headers = { ...extraHeaders };

  if (hasBody && !headers["Content-Type"]) {
    headers["Content-Type"] = "application/json";
  }

  const token = getStoredAccessToken();

  if (token) {
    headers.Authorization = `Bearer ${token}`;
  }

  return headers;
}

async function parseResponse(response) {
  const contentType = response.headers.get("content-type") ?? "";
  const isJson = contentType.includes("application/json");

  if (response.status === 204) {
    return null;
  }

  if (isJson) {
    return response.json();
  }

  return response.text();
}

function normalizeErrorMessage(payload, fallbackMessage) {
  if (!payload) {
    return fallbackMessage;
  }

  if (typeof payload === "string" && payload.trim()) {
    return payload;
  }

  if (typeof payload === "object" && payload !== null) {
    if (typeof payload.detail === "string" && payload.detail.trim()) {
      return payload.detail;
    }

    if (Array.isArray(payload.detail)) {
      return "Request validation failed.";
    }
  }

  return fallbackMessage;
}

export async function apiRequest(path, options = {}) {
  const { method = "GET", body, headers = {} } = options;

  const response = await fetch(`${API_BASE_URL}${path}`, {
    method,
    headers: buildHeaders(headers, body !== undefined),
    body: body !== undefined ? JSON.stringify(body) : undefined,
  });

  const payload = await parseResponse(response);

  if (!response.ok) {
    const error = new Error(
      normalizeErrorMessage(payload, "Request failed.")
    );
    error.status = response.status;
    error.payload = payload;
    throw error;
  }

  return payload;
}