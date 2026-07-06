import Card from "../common/card";

function RiskMetricCard({
  title,
  value,
  format = "number",
  accent = "cyan",
  description,
}) {
  function formatValue() {
    if (value === null || value === undefined || Number.isNaN(value)) {
      return "—";
    }

    if (format === "percent") {
      return `${(Number(value) * 100).toFixed(2)}%`;
    }

    if (format === "integer") {
      return String(Math.round(Number(value)));
    }

    return Number(value).toFixed(4);
  }

  const accentColor =
    accent === "green"
      ? "rgba(34, 197, 94, 0.95)"
      : accent === "amber"
      ? "rgba(251, 191, 36, 0.95)"
      : accent === "rose"
      ? "rgba(244, 63, 94, 0.95)"
      : "rgba(56, 189, 248, 0.95)";

  return (
    <Card title={title} subtitle={description}>
      <div
        style={{
          display: "grid",
          gap: 10,
        }}
      >
        <div
          style={{
            fontSize: "2rem",
            fontWeight: 700,
            letterSpacing: "-0.03em",
            color: accentColor,
          }}
        >
          {formatValue()}
        </div>
      </div>
    </Card>
  );
}

export default RiskMetricCard;