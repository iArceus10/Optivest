import Card from "../common/card";

function formatDate(value) {
  if (!value) {
    return "Not available";
  }

  const date = new Date(value);

  if (Number.isNaN(date.getTime())) {
    return "Not available";
  }

  return new Intl.DateTimeFormat("en-IN", {
    day: "2-digit",
    month: "short",
    year: "numeric",
  }).format(date);
}

function PortfolioOverviewCard({ portfolio }) {
  return (
    <Card
      title="Portfolio overview"
      subtitle="This workspace is anchored to the selected portfolio. Analytics requests in the current phase are run against a user-specified analysis universe of tickers and a date range."
    >
      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(2, minmax(0, 1fr))",
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
            Portfolio name
          </p>

          <p
            style={{
              margin: "12px 0 0",
              color: "var(--text-secondary)",
              fontWeight: 700,
              fontSize: "1.05rem",
              lineHeight: 1.6,
            }}
          >
            {portfolio.name}
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
            Portfolio id
          </p>

          <p
            style={{
              margin: "12px 0 0",
              color: "var(--text-secondary)",
              fontWeight: 600,
              lineHeight: 1.6,
              wordBreak: "break-word",
            }}
          >
            {portfolio.id}
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
            Created
          </p>

          <p
            style={{
              margin: "12px 0 0",
              color: "var(--text-secondary)",
              fontWeight: 700,
              fontSize: "1rem",
            }}
          >
            {formatDate(portfolio.created_at)}
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
            Last updated
          </p>

          <p
            style={{
              margin: "12px 0 0",
              color: "var(--text-secondary)",
              fontWeight: 700,
              fontSize: "1rem",
            }}
          >
            {formatDate(portfolio.updated_at)}
          </p>
        </div>
      </div>

      <div
        style={{
          marginTop: 18,
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
          Description
        </p>

        <p
          style={{
            margin: "12px 0 0",
            color: "var(--text-secondary)",
            lineHeight: 1.8,
          }}
        >
          {portfolio.description?.trim()
            ? portfolio.description
            : "No portfolio description provided."}
        </p>
      </div>
    </Card>
  );
}

export default PortfolioOverviewCard;