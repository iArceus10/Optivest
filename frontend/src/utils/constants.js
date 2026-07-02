export const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL ?? "http://127.0.0.1:8000/api/v1";

export const ACCESS_TOKEN_KEY = "optivest_access_token";

export const APP_NAV_ITEMS = [
  {
    label: "Dashboard",
    href: "/dashboard",
    description: "Portfolio workspace",
  },
];

export const AUTH_PAGE_COPY = {
  login: {
    title: "Access your OptiVest workspace.",
    subtitle:
      "Sign in to manage portfolios, run optimization workflows, inspect risk, and monitor portfolio health from a single analytics dashboard.",
    submitLabel: "Sign in to OptiVest",
    alternateLabel: "Need an account?",
    alternateHref: "/register",
    alternateAction: "Create one",
  },
  register: {
    title: "Create your OptiVest account.",
    subtitle:
      "Set up your analytics workspace to build portfolios, evaluate risk, compare optimization outputs, and present a polished fintech product in interviews.",
    submitLabel: "Create account",
    alternateLabel: "Already have an account?",
    alternateHref: "/login",
    alternateAction: "Sign in",
  },
};