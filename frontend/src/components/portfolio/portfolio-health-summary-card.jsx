import Card from "../common/card";

function getHealthAccent(score) {
  if (score >= 85) {
    return "rgba(34, 197, 94, 0.95)";
  }

  if (score >= 70) {
    return "rgba(56, 189, 248, 0.95)";
  }

  if (score >= 50) {
    return "rgba(251, 191, 36, 0.95)";
  }

  return "rgba(244, 63, 94, 0.95)";
}

function getHealthLabel(score) {
  if (score >= 90) {
    return "Excellent";
  }

  if (score >= 75) {
    return "Strong";
  }

  if (score >= 60) {
    return "Moderate";
  }

  if (score >= 40) {
    return "Weak";
  }

  return "Poor";
}

function PortfolioHealthSummaryCard({ result }) {
  const score = result?.overall_health_score ?? null;
  const accent = score === null ? "rgba(56, 189, 248, 0.95)" : getHealthAccent(score);

  return (
    <Card
      title="Overall portfolio health"
      subtitle="Composite portfolio diagnostic synthesized from return quality, downside risk, diversification, concentration, and optimization efficiency."
    >
      <div
        style={{
          display: "grid",
          gap: 18,
        }}
      >
        <div
          style={{
            display: "flex",
            alignItems: "flex-end",
            justifyContent: "space-between",
            gap: 20,
            flexWrap: "wrap",
          }}
        >
          <div>
            <div
              style={{
                fontSize: "3rem",
                fontWeight: 800,
                letterSpacing: "-0.04em",
                color: accent,
                lineHeight: 1,
              }}
            >
              {score === null || score === undefined ? "—" : score.toFixed(1)}
            </div>

            <div
              style={{
                marginTop: 8,
                color: "var(--text-faint)",
                fontSize: "0.95rem",
              }}
            >
              out of 100
            </div>
          </div>

          <div
            style={{
              padding: "10px 14px",
              borderRadius: 999,
              border: "1px solid var(--border-primary)",
              background: "rgba(15, 23, 42, 0.55)",
              color: "var(--text-secondary)",
              fontWeight: 700,
              letterSpacing: "0.04em",
              textTransform: "uppercase",
              fontSize: "0.78rem",
            }}
          >
            {score === null || score === undefined ? "Not analyzed" : getHealthLabel(score)}
          </div>
        </div>

        <div
          style={{
            color: "var(--text-muted)",
            lineHeight: 1.8,
          }}
        >
          {result?.summary ||
            "Run portfolio health analysis to evaluate portfolio construction quality across return, risk, diversification, and efficiency dimensions."}
        </div>
      </div>
    </Card>
  );
}

export default PortfolioHealthSummaryCard;