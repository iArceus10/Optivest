import Card from "../common/card";

function formatPercent(value) {
  return `${(Number(value) * 100).toFixed(2)}%`;
}

function SimulationHighlightCard({
  title,
  subtitle,
  portfolio,
  accent = "cyan",
}) {
  const accentColor =
    accent === "green"
      ? "rgba(34, 197, 94, 0.95)"
      : "rgba(56, 189, 248, 0.95)";

  return (
    <Card title={title} subtitle={subtitle}>
      {!portfolio ? (
        <div
          style={{
            color: "var(--text-muted)",
            lineHeight: 1.7,
          }}
        >
          Run the simulation to populate this portfolio.
        </div>
      ) : (
        <div
          style={{
            display: "grid",
            gap: 16,
          }}
        >
          <div
            style={{
              display: "grid",
              gap: 12,
              gridTemplateColumns: "repeat(auto-fit, minmax(140px, 1fr))",
            }}
          >
            <div>
              <div
                style={{
                  color: "var(--text-faint)",
                  fontSize: "0.82rem",
                  marginBottom: 4,
                }}
              >
                Expected return
              </div>
              <div
                style={{
                  color: accentColor,
                  fontWeight: 700,
                  fontSize: "1.2rem",
                }}
              >
                {formatPercent(portfolio.expected_return)}
              </div>
            </div>

            <div>
              <div
                style={{
                  color: "var(--text-faint)",
                  fontSize: "0.82rem",
                  marginBottom: 4,
                }}
              >
                Volatility
              </div>
              <div
                style={{
                  color: accentColor,
                  fontWeight: 700,
                  fontSize: "1.2rem",
                }}
              >
                {formatPercent(portfolio.volatility)}
              </div>
            </div>

            <div>
              <div
                style={{
                  color: "var(--text-faint)",
                  fontSize: "0.82rem",
                  marginBottom: 4,
                }}
              >
                Sharpe ratio
              </div>
              <div
                style={{
                  color: accentColor,
                  fontWeight: 700,
                  fontSize: "1.2rem",
                }}
              >
                {Number(portfolio.sharpe_ratio).toFixed(4)}
              </div>
            </div>
          </div>

          <div
            style={{
              display: "grid",
              gap: 10,
            }}
          >
            <div
              style={{
                color: "var(--text-secondary)",
                fontWeight: 600,
              }}
            >
              Allocations
            </div>

            <div
              style={{
                display: "flex",
                flexWrap: "wrap",
                gap: 10,
              }}
            >
              {portfolio.allocations.map((allocation) => (
                <div
                  key={allocation.ticker}
                  style={{
                    padding: "10px 12px",
                    borderRadius: "999px",
                    border: "1px solid var(--border-subtle)",
                    background: "rgba(255,255,255,0.03)",
                    color: "var(--text-secondary)",
                    fontSize: "0.92rem",
                  }}
                >
                  {allocation.ticker}:{" "}
                  <strong>
                    {(allocation.weight * 100).toFixed(2)}%
                  </strong>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </Card>
  );
}

export default SimulationHighlightCard;