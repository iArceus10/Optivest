import { ArrowUpRight, CalendarDays, Trash2 } from "lucide-react";
import { Link } from "react-router-dom";

import Button from "../common/button";
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

function PortfolioCard({
  portfolio,
  onDeletePortfolio,
  isDeleting = false,
}) {
  return (
    <Card
      minHeight={280}
      title={portfolio.name}
      subtitle={
        portfolio.description?.trim()
          ? portfolio.description
          : "No portfolio description provided."
      }
      action={
        <button
          type="button"
          onClick={() => onDeletePortfolio(portfolio.id)}
          disabled={isDeleting}
          title="Delete portfolio"
          aria-label={`Delete ${portfolio.name}`}
          style={{
            width: 42,
            height: 42,
            display: "grid",
            placeItems: "center",
            borderRadius: 14,
            border: "1px solid rgba(239, 68, 68, 0.2)",
            background: "rgba(127, 29, 29, 0.12)",
            color: "var(--accent-red)",
            opacity: isDeleting ? 0.7 : 1,
          }}
        >
          <Trash2 size={16} />
        </button>
      }
    >
      <div
        style={{
          display: "grid",
          gap: 16,
        }}
      >
        <div
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(2, minmax(0, 1fr))",
            gap: 14,
          }}
        >
          <div
            style={{
              padding: "16px",
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
                margin: "10px 0 0",
                fontSize: "1rem",
                fontWeight: 700,
                color: "var(--text-secondary)",
              }}
            >
              {formatDate(portfolio.created_at)}
            </p>
          </div>

          <div
            style={{
              padding: "16px",
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
              Updated
            </p>

            <p
              style={{
                margin: "10px 0 0",
                fontSize: "1rem",
                fontWeight: 700,
                color: "var(--text-secondary)",
              }}
            >
              {formatDate(portfolio.updated_at)}
            </p>
          </div>
        </div>

        <div
          style={{
            padding: "16px",
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
            Portfolio status
          </p>

          <p
            style={{
              margin: "10px 0 0",
              color: "var(--text-secondary)",
              lineHeight: 1.7,
              fontWeight: 600,
            }}
          >
            Portfolio metadata is configured. Open the workspace to run
            analytics, optimization, simulation, risk, and portfolio
            health workflows.
          </p>
        </div>

        <Link to={`/portfolios/${portfolio.id}`}>
          <Button variant="primary" size="md">
            Open workspace <ArrowUpRight size={16} />
          </Button>
        </Link>
      </div>
    </Card>
  );
}

export default PortfolioCard;