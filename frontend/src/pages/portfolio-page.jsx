import { Activity, ArrowUpRight, ChartNoAxesCombined, ShieldAlert, Target } from "lucide-react";
import { useParams } from "react-router-dom";

import Card from "../components/common/card";

const ANALYTICS_PANELS = [
  {
    title: "Statistics",
    copy:
      "Expected return, covariance, correlation, and portfolio volatility should appear here for the selected portfolio.",
    icon: ChartNoAxesCombined,
  },
  {
    title: "Optimization",
    copy:
      "Mean-variance, minimum variance, maximum Sharpe, and efficient frontier results will be anchored to this portfolio workspace.",
    icon: Target,
  },
  {
    title: "Risk analytics",
    copy:
      "Sharpe, Sortino, drawdown, VaR, and CVaR should be visible without leaving the portfolio context.",
    icon: ShieldAlert,
  },
  {
    title: "Simulation and health",
    copy:
      "Monte Carlo outputs and portfolio health diagnostics should help evaluate the portfolio as a product-level investment idea.",
    icon: Activity,
  },
];

function PortfolioPage() {
  const { portfolioId } = useParams();

  return (
    <div>
      <section className="page-hero">
        <div className="page-hero__content">
          <div className="page-hero__eyebrow">
            <ArrowUpRight size={16} />
            Portfolio workspace shell
          </div>

          <h1 className="page-hero__title">Portfolio analytics workspace</h1>

          <p className="page-hero__copy">
            This page will become the core OptiVest experience. Every major
            backend capability — portfolio statistics, optimization, simulation,
            risk, and health analytics — should be presented as a coherent
            portfolio-centric workspace rather than as isolated endpoint demos.
          </p>

          <p
            style={{
              margin: "18px 0 0",
              color: "var(--text-faint)",
              fontSize: "0.94rem",
            }}
          >
            Current route parameter: <strong style={{ color: "var(--text-secondary)" }}>{portfolioId}</strong>
          </p>
        </div>
      </section>

      <section className="dashboard-grid">
        <div className="dashboard-grid__full">
          <Card
            title="Portfolio overview"
            subtitle="In the next batch, this section will be backed by GET /portfolios/{portfolio_id} and will surface portfolio metadata, holdings, and ownership-aware actions."
          >
            <div
              style={{
                display: "grid",
                gridTemplateColumns: "repeat(3, minmax(0, 1fr))",
                gap: 16,
              }}
            >
              {[
                {
                  label: "Portfolio identity",
                  value: "Name, description, ownership",
                },
                {
                  label: "Holdings",
                  value: "Assets and weights",
                },
                {
                  label: "Analytics status",
                  value: "Ready for statistics, risk, optimization, simulation, health",
                },
              ].map((item) => (
                <div
                  key={item.label}
                  style={{
                    padding: "18px",
                    borderRadius: "var(--radius-sm)",
                    border: "1px solid var(--border-subtle)",
                    background: "rgba(9, 14, 23, 0.72)",
                  }}
                >
                  <p
                    style={{
                      margin: 0,
                      color: "var(--text-faint)",
                      fontSize: "0.84rem",
                      textTransform: "uppercase",
                      letterSpacing: "0.06em",
                    }}
                  >
                    {item.label}
                  </p>

                  <p
                    style={{
                      margin: "12px 0 0",
                      color: "var(--text-secondary)",
                      lineHeight: 1.7,
                      fontWeight: 600,
                    }}
                  >
                    {item.value}
                  </p>
                </div>
              ))}
            </div>
          </Card>
        </div>

        {ANALYTICS_PANELS.map((panel) => {
          const Icon = panel.icon;

          return (
            <div key={panel.title} className="dashboard-grid__span-6">
              <Card minHeight={230}>
                <div
                  style={{
                    width: 48,
                    height: 48,
                    display: "grid",
                    placeItems: "center",
                    borderRadius: 16,
                    background: "var(--gradient-brand-soft)",
                    border: "1px solid rgba(34, 197, 94, 0.18)",
                    marginBottom: 18,
                  }}
                >
                  <Icon size={22} />
                </div>

                <h3
                  style={{
                    margin: 0,
                    fontSize: "1.08rem",
                    fontWeight: 800,
                    letterSpacing: "-0.02em",
                  }}
                >
                  {panel.title}
                </h3>

                <p
                  style={{
                    margin: "12px 0 0",
                    color: "var(--text-muted)",
                    lineHeight: 1.7,
                    fontSize: "0.95rem",
                  }}
                >
                  {panel.copy}
                </p>
              </Card>
            </div>
          );
        })}
      </section>
    </div>
  );
}

export default PortfolioPage;