import { ArrowRight, ShieldCheck, Sparkles, TrendingUp } from "lucide-react";

import AuthForm from "../components/auth/auth-form";

function LoginPage() {
  return (
    <div className="auth-page">
      <div className="auth-page__layout">
        <section className="auth-page__hero">
          <div>
            <div className="auth-page__eyebrow">
              <Sparkles size={16} />
              Quantitative portfolio intelligence
            </div>

            <h1 className="auth-page__hero-title">
              Build, optimize, and explain portfolios with a <span>real analytics stack</span>.
            </h1>

            <p className="auth-page__hero-copy">
              OptiVest combines portfolio construction, optimization, simulation,
              risk analytics, and health diagnostics into a single fintech
              workspace designed to be both technically rigorous and visually
              impressive.
            </p>
          </div>

          <div className="auth-page__hero-grid">
            <div className="auth-page__hero-card">
              <h3 className="auth-page__hero-card-title">Optimization-ready</h3>
              <p className="auth-page__hero-card-copy">
                Mean-variance, minimum variance, maximum Sharpe, and efficient
                frontier workflows on top of a tested backend engine.
              </p>
            </div>

            <div className="auth-page__hero-card">
              <h3 className="auth-page__hero-card-title">Risk-first analytics</h3>
              <p className="auth-page__hero-card-copy">
                Evaluate drawdown, Value-at-Risk, Conditional Value-at-Risk,
                Sharpe ratio, and Sortino ratio in one workspace.
              </p>
            </div>

            <div className="auth-page__hero-card">
              <h3 className="auth-page__hero-card-title">Simulation-backed</h3>
              <p className="auth-page__hero-card-copy">
                Compare portfolios against simulated opportunity sets and use
                Monte Carlo outputs to reason about efficiency.
              </p>
            </div>

            <div className="auth-page__hero-card">
              <h3 className="auth-page__hero-card-title">Interview-defensible</h3>
              <p className="auth-page__hero-card-copy">
                Showcase clean software architecture, quantitative finance, and
                product thinking in one coherent system.
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
              { icon: TrendingUp, label: "Optimization" },
              { icon: ShieldCheck, label: "Risk analytics" },
              { icon: ArrowRight, label: "Portfolio health" },
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
          <AuthForm mode="login" />
        </section>
      </div>
    </div>
  );
}

export default LoginPage;