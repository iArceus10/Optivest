import Button from "../common/button";
import Card from "../common/card";

function RiskControlsCard({
  tickers,
  values,
  onChange,
  onAnalyze,
  isLoading = false,
}) {
  return (
    <Card
      title="Risk analytics controls"
      subtitle="Configure portfolio weights and downside-risk assumptions for the selected analysis universe."
    >
      <div
        style={{
          display: "grid",
          gap: 18,
        }}
      >
        <div
          style={{
            display: "grid",
            gap: 16,
            gridTemplateColumns: "repeat(auto-fit, minmax(180px, 1fr))",
          }}
        >
          {tickers.map((ticker, index) => (
            <label
              key={ticker}
              style={{
                display: "grid",
                gap: 8,
              }}
            >
              <span
                style={{
                  fontSize: "0.9rem",
                  fontWeight: 600,
                  color: "var(--text-secondary)",
                }}
              >
                {ticker} weight
              </span>

              <input
                type="number"
                min="0"
                max="1"
                step="0.01"
                value={values.weights[index] ?? ""}
                onChange={(event) =>
                  onChange("weight", {
                    index,
                    value: event.target.value,
                  })
                }
                style={{
                  minHeight: 46,
                  borderRadius: "var(--radius-sm)",
                  border: "1px solid var(--border-subtle)",
                  background: "rgba(255, 255, 255, 0.03)",
                  color: "var(--text-primary)",
                  padding: "0 14px",
                  outline: "none",
                }}
              />
            </label>
          ))}
        </div>

        <div
          style={{
            display: "grid",
            gap: 16,
            gridTemplateColumns: "repeat(auto-fit, minmax(220px, 1fr))",
          }}
        >
          <label
            style={{
              display: "grid",
              gap: 8,
            }}
          >
            <span
              style={{
                fontSize: "0.9rem",
                fontWeight: 600,
                color: "var(--text-secondary)",
              }}
            >
              Risk-free rate
            </span>

            <input
              type="number"
              step="0.005"
              value={values.riskFreeRate}
              onChange={(event) =>
                onChange("riskFreeRate", event.target.value)
              }
              style={{
                minHeight: 46,
                borderRadius: "var(--radius-sm)",
                border: "1px solid var(--border-subtle)",
                background: "rgba(255, 255, 255, 0.03)",
                color: "var(--text-primary)",
                padding: "0 14px",
                outline: "none",
              }}
            />
          </label>

          <label
            style={{
              display: "grid",
              gap: 8,
            }}
          >
            <span
              style={{
                fontSize: "0.9rem",
                fontWeight: 600,
                color: "var(--text-secondary)",
              }}
            >
              Confidence level
            </span>

            <input
              type="number"
              min="0.5"
              max="0.999"
              step="0.01"
              value={values.confidenceLevel}
              onChange={(event) =>
                onChange("confidenceLevel", event.target.value)
              }
              style={{
                minHeight: 46,
                borderRadius: "var(--radius-sm)",
                border: "1px solid var(--border-subtle)",
                background: "rgba(255, 255, 255, 0.03)",
                color: "var(--text-primary)",
                padding: "0 14px",
                outline: "none",
              }}
            />
          </label>
        </div>

        <div
          style={{
            padding: "14px 16px",
            borderRadius: "var(--radius-sm)",
            border: "1px solid var(--border-subtle)",
            background: "rgba(255, 255, 255, 0.025)",
            color: "var(--text-muted)",
            lineHeight: 1.75,
          }}
        >
          Weight sum:{" "}
          <strong style={{ color: "var(--text-secondary)" }}>
            {values.weights
              .reduce(
                (sum, weight) => sum + (Number(weight) || 0),
                0
              )
              .toFixed(4)}
          </strong>
          . For the cleanest results, keep the portfolio fully invested
          with weights summing to 1.00.
        </div>

        <div
          style={{
            display: "flex",
            justifyContent: "flex-end",
          }}
        >
          <Button
            variant="primary"
            size="md"
            onClick={onAnalyze}
            isLoading={isLoading}
          >
            Run risk analytics
          </Button>
        </div>
      </div>
    </Card>
  );
}

export default RiskControlsCard;