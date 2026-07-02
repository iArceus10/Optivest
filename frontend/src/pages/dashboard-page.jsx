import { BriefcaseBusiness, Sparkles } from "lucide-react";
import { useEffect, useState } from "react";

import Card from "../components/common/card";
import CreatePortfolioForm from "../components/portfolio/create-portfolio-form";
import PortfolioCard from "../components/portfolio/portfolio-card";
import {
  createPortfolio,
  deletePortfolio,
  getPortfolios,
} from "../services/portfolio-service";

function DashboardPage() {
  const [portfolios, setPortfolios] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [loadError, setLoadError] = useState("");
  const [isCreatingPortfolio, setIsCreatingPortfolio] = useState(false);
  const [deletingPortfolioId, setDeletingPortfolioId] = useState(null);

  useEffect(() => {
    loadPortfolioDashboard();
  }, []);

  async function loadPortfolioDashboard() {
    try {
      setIsLoading(true);
      setLoadError("");

      const portfolioResponse = await getPortfolios();
      setPortfolios(portfolioResponse);
    } catch (error) {
      setLoadError(
        error.message || "Unable to load your portfolios right now."
      );
    } finally {
      setIsLoading(false);
    }
  }

  async function handleCreatePortfolio(payload) {
    try {
      setIsCreatingPortfolio(true);

      const createdPortfolio = await createPortfolio(payload);

      setPortfolios((previousPortfolios) => [
        createdPortfolio,
        ...previousPortfolios,
      ]);
    } finally {
      setIsCreatingPortfolio(false);
    }
  }

  async function handleDeletePortfolio(portfolioId) {
    const shouldDelete = window.confirm(
      "Delete this portfolio? This action cannot be undone."
    );

    if (!shouldDelete) {
      return;
    }

    try {
      setDeletingPortfolioId(portfolioId);

      await deletePortfolio(portfolioId);

      setPortfolios((previousPortfolios) =>
        previousPortfolios.filter(
          (portfolio) => portfolio.id !== portfolioId
        )
      );
    } catch (error) {
      window.alert(
        error.message || "Unable to delete portfolio right now."
      );
    } finally {
      setDeletingPortfolioId(null);
    }
  }

  return (
    <div>
      <section className="page-hero">
        <div className="page-hero__content">
          <div className="page-hero__eyebrow">
            <Sparkles size={16} />
            Portfolio command center
          </div>

          <h1 className="page-hero__title">
            Build and manage your OptiVest portfolios.
          </h1>

          <p className="page-hero__copy">
            Create portfolio containers, organize investment ideas, and
            enter the analytics workspace for optimization, simulation,
            risk, and portfolio health workflows powered by the completed
            backend platform.
          </p>
        </div>
      </section>

      <section className="dashboard-grid" style={{ marginBottom: 24 }}>
        <div className="dashboard-grid__span-8">
          <CreatePortfolioForm
            onCreatePortfolio={handleCreatePortfolio}
            isSubmitting={isCreatingPortfolio}
          />
        </div>

        <div className="dashboard-grid__span-4">
          <Card
            title="Portfolio dashboard status"
            subtitle="The dashboard is now wired to the real backend portfolio CRUD contract."
            minHeight={360}
          >
            <div
              style={{
                display: "grid",
                gap: 16,
              }}
            >
              <div
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
                    fontSize: "0.82rem",
                    textTransform: "uppercase",
                    letterSpacing: "0.06em",
                  }}
                >
                  Total portfolios
                </p>

                <p
                  style={{
                    margin: "12px 0 0",
                    fontSize: "2rem",
                    fontWeight: 800,
                    letterSpacing: "-0.04em",
                  }}
                >
                  {portfolios.length}
                </p>
              </div>

              <div
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
                    fontSize: "0.82rem",
                    textTransform: "uppercase",
                    letterSpacing: "0.06em",
                  }}
                >
                  Current dashboard scope
                </p>

                <p
                  style={{
                    margin: "12px 0 0",
                    color: "var(--text-secondary)",
                    lineHeight: 1.7,
                    fontWeight: 600,
                  }}
                >
                  Portfolio metadata management, authentication, and
                  workspace routing are live.
                </p>
              </div>

              <div
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
                    fontSize: "0.82rem",
                    textTransform: "uppercase",
                    letterSpacing: "0.06em",
                  }}
                >
                  Next milestone
                </p>

                <p
                  style={{
                    margin: "12px 0 0",
                    color: "var(--text-secondary)",
                    lineHeight: 1.7,
                    fontWeight: 600,
                  }}
                >
                  Replace the portfolio workspace placeholder with real
                  portfolio detail + analytics integrations.
                </p>
              </div>
            </div>
          </Card>
        </div>
      </section>

      <section className="dashboard-grid">
        <div className="dashboard-grid__full">
          <Card
            title="Your portfolios"
            subtitle="Open any portfolio to move into the analytics workspace."
          >
            {isLoading ? (
              <div
                style={{
                  minHeight: 220,
                  display: "grid",
                  placeItems: "center",
                  color: "var(--text-muted)",
                  textAlign: "center",
                  lineHeight: 1.7,
                }}
              >
                Loading your portfolios…
              </div>
            ) : loadError ? (
              <div
                style={{
                  minHeight: 220,
                  display: "grid",
                  placeItems: "center",
                  padding: 24,
                  borderRadius: "var(--radius-sm)",
                  border: "1px solid rgba(239, 68, 68, 0.24)",
                  background: "rgba(127, 29, 29, 0.12)",
                  color: "#fecaca",
                  textAlign: "center",
                  lineHeight: 1.7,
                }}
              >
                {loadError}
              </div>
            ) : portfolios.length === 0 ? (
              <div
                style={{
                  minHeight: 220,
                  display: "grid",
                  placeItems: "center",
                  padding: 24,
                  borderRadius: "var(--radius-sm)",
                  border: "1px dashed var(--border-strong)",
                  background: "rgba(9, 14, 23, 0.52)",
                  color: "var(--text-muted)",
                  textAlign: "center",
                  lineHeight: 1.8,
                }}
              >
                <div>
                  <BriefcaseBusiness
                    size={32}
                    style={{ marginBottom: 12 }}
                  />
                  <div style={{ fontWeight: 700, color: "var(--text-secondary)" }}>
                    No portfolios yet
                  </div>
                  <div style={{ marginTop: 8 }}>
                    Create your first portfolio from the panel above to start
                    using the OptiVest analytics workspace.
                  </div>
                </div>
              </div>
            ) : (
              <div className="dashboard-grid">
                {portfolios.map((portfolio) => (
                  <div
                    key={portfolio.id}
                    className="dashboard-grid__span-4"
                  >
                    <PortfolioCard
                      portfolio={portfolio}
                      onDeletePortfolio={handleDeletePortfolio}
                      isDeleting={deletingPortfolioId === portfolio.id}
                    />
                  </div>
                ))}
              </div>
            )}
          </Card>
        </div>
      </section>
    </div>
  );
}

export default DashboardPage;