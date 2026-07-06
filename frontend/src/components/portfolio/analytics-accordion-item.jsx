import { ChevronDown, ChevronUp } from "lucide-react";

function getStatusStyles(status) {
  switch (status) {
    case "loaded":
      return {
        label: "Loaded",
        color: "#86efac",
        background: "rgba(22, 101, 52, 0.18)",
        border: "1px solid rgba(34, 197, 94, 0.24)",
      };
    case "error":
      return {
        label: "Error",
        color: "#fecaca",
        background: "rgba(127, 29, 29, 0.18)",
        border: "1px solid rgba(239, 68, 68, 0.24)",
      };
    default:
      return {
        label: "Not run",
        color: "var(--text-faint)",
        background: "rgba(255, 255, 255, 0.04)",
        border: "1px solid var(--border-subtle)",
      };
  }
}

function AnalyticsAccordionItem({
  title,
  description,
  status = "idle",
  isOpen,
  onToggle,
  children,
}) {
  const statusStyles = getStatusStyles(status);

  return (
    <div
      style={{
        borderRadius: "var(--radius-md)",
        border: "1px solid var(--border-subtle)",
        background:
          "linear-gradient(180deg, rgba(10, 16, 26, 0.94), rgba(7, 12, 20, 0.9))",
        boxShadow: "var(--shadow-soft)",
        overflow: "hidden",
      }}
    >
      <button
        type="button"
        onClick={onToggle}
        style={{
          width: "100%",
          appearance: "none",
          border: "none",
          background: "transparent",
          padding: "20px 22px",
          cursor: "pointer",
          display: "flex",
          alignItems: "flex-start",
          justifyContent: "space-between",
          gap: 18,
          textAlign: "left",
        }}
      >
        <div style={{ minWidth: 0, flex: 1 }}>
          <div
            style={{
              display: "flex",
              flexWrap: "wrap",
              alignItems: "center",
              gap: 12,
              marginBottom: 10,
            }}
          >
            <h3
              style={{
                margin: 0,
                color: "var(--text-primary)",
                fontSize: "1.02rem",
                fontWeight: 700,
              }}
            >
              {title}
            </h3>

            <span
              style={{
                display: "inline-flex",
                alignItems: "center",
                minHeight: 28,
                padding: "0 12px",
                borderRadius: "999px",
                fontSize: "0.8rem",
                fontWeight: 700,
                color: statusStyles.color,
                background: statusStyles.background,
                border: statusStyles.border,
                letterSpacing: "0.01em",
              }}
            >
              {statusStyles.label}
            </span>
          </div>

          <p
            style={{
              margin: 0,
              color: "var(--text-muted)",
              lineHeight: 1.75,
              maxWidth: 900,
            }}
          >
            {description}
          </p>
        </div>

        <div
          style={{
            width: 42,
            height: 42,
            borderRadius: "999px",
            display: "grid",
            placeItems: "center",
            background: "rgba(255, 255, 255, 0.04)",
            border: "1px solid var(--border-subtle)",
            flexShrink: 0,
            color: "var(--text-secondary)",
          }}
        >
          {isOpen ? <ChevronUp size={18} /> : <ChevronDown size={18} />}
        </div>
      </button>

      {isOpen ? (
        <div
          style={{
            padding: "0 22px 22px",
            borderTop: "1px solid rgba(255, 255, 255, 0.05)",
          }}
        >
          <div style={{ paddingTop: 20 }}>{children}</div>
        </div>
      ) : null}
    </div>
  );
}

export default AnalyticsAccordionItem;