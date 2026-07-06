function AnalyticsTabs({ tabs, activeTab, onChange }) {
  return (
    <div
      style={{
        display: "flex",
        flexWrap: "wrap",
        gap: 12,
        padding: "10px",
        borderRadius: "calc(var(--radius-md) + 4px)",
        border: "1px solid var(--border-subtle)",
        background:
          "linear-gradient(180deg, rgba(10, 16, 26, 0.94), rgba(7, 12, 20, 0.9))",
        boxShadow: "var(--shadow-soft)",
      }}
    >
      {tabs.map((tab) => {
        const isActive = activeTab === tab.id;

        return (
          <button
            key={tab.id}
            type="button"
            onClick={() => onChange(tab.id)}
            style={{
              appearance: "none",
              border: isActive
                ? "1px solid rgba(34, 211, 238, 0.34)"
                : "1px solid transparent",
              background: isActive
                ? "linear-gradient(135deg, rgba(34, 211, 238, 0.2), rgba(59, 130, 246, 0.14))"
                : "rgba(255, 255, 255, 0.02)",
              color: isActive
                ? "var(--text-primary)"
                : "var(--text-muted)",
              borderRadius: "999px",
              padding: "12px 18px",
              minHeight: 46,
              cursor: "pointer",
              transition: "all 160ms ease",
              display: "flex",
              alignItems: "center",
              gap: 10,
              boxShadow: isActive
                ? "0 0 0 1px rgba(34, 211, 238, 0.08), 0 12px 28px rgba(34, 211, 238, 0.12)"
                : "none",
              fontWeight: 600,
              letterSpacing: "0.01em",
            }}
          >
            <span style={{ fontSize: "0.95rem" }}>{tab.label}</span>
          </button>
        );
      })}
    </div>
  );
}

export default AnalyticsTabs;