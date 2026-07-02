import { Activity, BrainCircuit, ChartSpline, Shield } from "lucide-react";

import AuthForm from "../components/auth/auth-form";

function RegisterPage() {
  return (
    <div className="auth-page">
      <div className="auth-page__layout">
        <section className="auth-page__hero">
          <div>
            <div className="auth-page__eyebrow">
              <Activity size={16} />
              Portfolio engineering workspace
            </div>

            <h1 className="auth-page__hero-title">
              Create your <span>OptiVest terminal</span> and start building a modern analytics portfolio.
            </h1>

            <p className="auth-page__hero-copy">
              From portfolio construction and historical return analysis to
              optimization, simulation, risk, and portfolio health scoring,
              OptiVest turns the backend you built into a product you can
              actually present.
            </p>
          </div>

          <div className="auth-page__hero-grid">
            <div className="auth-page__hero-card">
              <h3 className="auth-page__hero-card-title">Portfolio management</h3>
              <p className="auth-page__hero-card-copy">
                Organize multiple investment ideas and preserve a clean portfolio-centric workflow.
              </p>
            </div>

            <div className="auth-page__hero-card">
              <h3 className="auth-page__hero-card-title">Statistics engine</h3>
              <p className="auth-page__hero-card-copy">
                Surface expected returns, covariance, correlation, and portfolio volatility from historical data.
              </p>
            </div>

            <div className="auth-page__hero-card">
              <h3 className="auth-page__hero-card-title">Simulation and health</h3>
              <p className="auth-page__hero-card-copy">
                Compare current allocations against simulated alternatives and health diagnostics built on top of existing engines.
              </p>
            </div>

            <div className="auth-page__hero-card">
              <h3 className="auth-page__hero-card-title">Serious frontend productization</h3>
              <p className="auth-page__hero-card-copy">
                Present the system as a cohesive fintech application rather than a collection of disconnected APIs.
              </p>
            </div>
          </div>

          <div
            style={{
              display: "flex",
              flexWrap: "wrap",
              gap: 14,
              marginTop: 20,
            }}
          >
            {[
              { icon: ChartSpline, label: "Statistics" },
              { icon: BrainCircuit, label: "Simulation" },
              { icon: Shield, label: "Health diagnostics" },
            ].map((item) => {
              const Icon = item.icon;

              return (
                <div
                  key={item.label}
                  style={{
                    display: "inline-flex",
                    alignItems: "center",
                    gap: 10,
                    padding: "12px 16px",
                    borderRadius: "var(--radius-pill)",
                    border: "1px solid var(--border-subtle)",
                    background: "rgba(10, 15, 24, 0.58)",
                    color: "var(--text-secondary)",
                  }}
                >
                  <Icon size={16} />
                  <span style={{ fontSize: "0.92rem", fontWeight: 600 }}>
                    {item.label}
                  </span>
                </div>
              );
            })}
          </div>
        </section>

        <section className="auth-card">
          <AuthForm mode="register" />
        </section>
      </div>
    </div>
  );
}

export default RegisterPage;