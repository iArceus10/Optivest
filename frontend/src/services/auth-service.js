import { apiRequest } from "./api-client";

export async function registerUser({ email, fullName, password }) {
  return apiRequest("/auth/register", {
    method: "POST",
    body: {
      email,
      full_name: fullName,
      password,
    },
  });
}

export async function loginUser({ email, password }) {
  return apiRequest("/auth/login", {
    method: "POST",
    body: {
      email,
      password,
    },
  });
}

export async function getCurrentUser() {
  return apiRequest("/auth/me");
}