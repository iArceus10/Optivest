import { ArrowRight, BriefcaseBusiness, ShieldCheck, Sparkles, TrendingUp } from "lucide-react";
import { Link } from "react-router-dom";

import Card from "../components/common/card";
import Button from "../components/common/button";

const CAPABILITY_CARDS = [
  {
    title: "Portfolio management",
    copy:
      "Create, update, and manage multiple portfolios through the authenticated OptiVest workspace.",
    icon: BriefcaseBusiness,
  },
  {
    title: "Optimization workflows",
    copy:
      "Expose mean-variance, minimum variance, maximum Sharpe, and efficient frontier outputs through a portfolio-centric UI.",
    icon: TrendingUp,
  },
  {
    title: "Risk and health diagnostics",
    copy:
      "Review drawdown, VaR, CVaR, Sharpe, Sortino, and higher-level portfolio health scoring in one product surface.",
    icon: ShieldCheck,
  },
];

function DashboardPage() {
  return (
    <div>
      <section className="page-hero">
        <div className="page-hero__content">
          <div className="page-hero__eyebrow">
            <Sparkles size={16} />
            Phase 9 productization workspace
          </div>

          <h1 className="page-hero__title">
            OptiVest turns a strong quant backend into a portfolio analytics product.
          </h1>

          <p className="page-hero__copy">
            This dashboard is the portfolio command center for OptiVest. From here,
            users should be able to create portfolios, inspect holdings, and launch
            optimization, simulation, risk, and health workflows without leaving
            the portfolio context.
          </p>
        </div>

        <div
          style={{
            display: "flex",
            alignItems: "center",
            gap: 12,
            flexWrap: "wrap",
          }}
        >
          <Link to="/portfolios/demo-workspace">
            <Button variant="primary" size="lg" style={{ width: "auto" }}>
              Explore workspace
            </Button>
          </Link>

          <Button variant="secondary" size="lg" style={{ width: "auto" }}>
            Portfolio CRUD next
          </Button>
        </div>
      </section>

      <section className="dashboard-grid">
        <div className="dashboard-grid__span-8">
          <Card
            title="Phase 9 implementation direction"
            subtitle="The dashboard is intentionally portfolio-centric. Analytics should hang off a selected portfolio rather than becoming disconnected standalone calculators."
            minHeight={280}
          >
            <div
              style={{
                display: "grid",
                gap: 18,
              }}
            >
              {[
                "Authenticated users land in a premium dashboard rather than a plain CRUD page.",
                "Portfolio detail pages will become the primary analytics workspace for statistics, optimization, simulation, risk, and health.",
                "Frontend services will map one-to-one with backend capability areas to keep integration clean and interview-defensible.",
                "Visual polish is treated as a product concern, not an afterthought, because the frontend is the presentation layer of the project.",
              ].map((point) => (
                <div
                  key={point}
                  style={{
                    display: "flex",
                    gap: 12,
                    alignItems: "flex-start",
                    color: "var(--text-secondary)",
                    lineHeight: 1.7,
                  }}
                >
                  <span
                    style={{
                      width: 8,
                      height: 8,
                      borderRadius: "50%",
                      background: "var(--accent-primary)",
                      marginTop: 10,
                      flexShrink: 0,
                    }}
                  />
                  <span>{point}</span>
                </div>
              ))}
            </div>
          </Card>
        </div>

        <div className="dashboard-grid__span-4">
          <Card
            title="Backend status"
            subtitle="Phase 8 backend foundation already complete."
            minHeight={280}
          >
            <div
              style={{
                display: "grid",
                gap: 14,
              }}
            >
              {[
                "Authentication",
                "Portfolio CRUD",
                "Market Data",
                "Statistics",
                "Optimization",
                "Monte Carlo Simulation",
                "Risk Analytics",
                "Portfolio Health",
              ].map((item) => (
                <div
                  key={item}
                  style={{
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "space-between",
                    gap: 12,
                    padding: "12px 14px",
                    borderRadius: "var(--radius-sm)",
                    border: "1px solid var(--border-subtle)",
                    background: "rgba(9, 14, 23, 0.72)",
                  }}
                >
                  <span style={{ color: "var(--text-secondary)" }}>{item}</span>
                  <span
                    style={{
                      color: "var(--accent-primary)",
                      fontWeight: 700,
                      fontSize: "0.9rem",
                    }}
                  >
                    Ready
                  </span>
                </div>
              ))}
            </div>
          </Card>
        </div>

        {CAPABILITY_CARDS.map((item) => {
          const Icon = item.icon;

          return (
            <div key={item.title} className="dashboard-grid__span-4">
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
                    fontSize: "1.06rem",
                    fontWeight: 800,
                    letterSpacing: "-0.02em",
                  }}
                >
                  {item.title}
                </h3>

                <p
                  style={{
                    margin: "12px 0 0",
                    color: "var(--text-muted)",
                    lineHeight: 1.7,
                    fontSize: "0.95rem",
                  }}
                >
                  {item.copy}
                </p>
              </Card>
            </div>
          );
        })}

        <div className="dashboard-grid__full">
          <Card
            title="What comes next"
            subtitle="The next implementation slice will replace dashboard placeholders with real portfolio CRUD integration and then turn the portfolio workspace into the main analytics surface."
          >
            <div
              style={{
                display: "grid",
                gap: 16,
              }}
            >
              {[
                "Wire dashboard to GET /portfolios and POST /portfolios.",
                "Add portfolio cards, create portfolio flow, and delete actions.",
                "Build a real portfolio detail workspace backed by portfolio lookup APIs.",
                "Integrate statistics, risk, health, optimization, and simulation panels one by one against the existing backend.",
              ].map((item) => (
                <div
                  key={item}
                  style={{
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "space-between",
                    gap: 12,
                    padding: "16px 18px",
                    borderRadius: "var(--radius-sm)",
                    border: "1px solid var(--border-subtle)",
                    background: "rgba(9, 14, 23, 0.72)",
                  }}
                >
                  <span
                    style={{
                      color: "var(--text-secondary)",
                      lineHeight: 1.6,
                    }}
                  >
                    {item}
                  </span>

                  <ArrowRight size={18} color="var(--text-faint)" />
                </div>
              ))}
            </div>
          </Card>
        </div>
      </section>
    </div>
  );
}

export default DashboardPage;