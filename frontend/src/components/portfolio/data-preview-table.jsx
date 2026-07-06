import Card from "../common/card";

function formatCellValue(value) {
  if (value === null || value === undefined) {
    return "—";
  }

  if (typeof value === "number") {
    return Number.isInteger(value) ? value : value.toFixed(6);
  }

  return String(value);
}

function DataPreviewTable({
  title,
  subtitle,
  columns,
  rows,
  emptyMessage = "No data available.",
}) {
  return (
    <Card title={title} subtitle={subtitle}>
      {rows.length === 0 ? (
        <div
          style={{
            minHeight: 120,
            display: "grid",
            placeItems: "center",
            color: "var(--text-muted)",
            textAlign: "center",
          }}
        >
          {emptyMessage}
        </div>
      ) : (
        <div
          style={{
            overflowX: "auto",
            borderRadius: "var(--radius-sm)",
            border: "1px solid var(--border-subtle)",
            background: "rgba(9, 14, 23, 0.72)",
          }}
        >
          <table
            style={{
              width: "100%",
              borderCollapse: "collapse",
              minWidth: 720,
            }}
          >
            <thead>
              <tr>
                {columns.map((column) => (
                  <th
                    key={column.key}
                    style={{
                      textAlign: "left",
                      padding: "14px 16px",
                      color: "var(--text-faint)",
                      fontSize: "0.82rem",
                      textTransform: "uppercase",
                      letterSpacing: "0.06em",
                      borderBottom: "1px solid var(--border-subtle)",
                      background: "rgba(6, 11, 18, 0.86)",
                    }}
                  >
                    {column.label}
                  </th>
                ))}
              </tr>
            </thead>

            <tbody>
              {rows.map((row, index) => (
                <tr key={row.id ?? `${title}-${index}`}>
                  {columns.map((column) => (
                    <td
                      key={column.key}
                      style={{
                        padding: "14px 16px",
                        color: "var(--text-secondary)",
                        borderBottom:
                          index === rows.length - 1
                            ? "none"
                            : "1px solid rgba(255, 255, 255, 0.04)",
                        verticalAlign: "top",
                        lineHeight: 1.6,
                      }}
                    >
                      {formatCellValue(row[column.key])}
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </Card>
  );
}

export default DataPreviewTable;