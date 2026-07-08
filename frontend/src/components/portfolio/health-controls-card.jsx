import Button from "../common/button";
import Card from "../common/card";
import Input from "../common/input";

function HealthControlsCard({
  tickers,
  values,
  onChange,
  onAnalyze,
  isLoading = false,
}) {
  const weights = Array.isArray(values.weights) ? values.weights : [];

  const totalWeight = weights.reduce(
    (sum, weight) => sum + (Number.isFinite(Number(weight)) ? Number(weight) : 0),
    0
  );

  return (
    <Card
      title="Portfolio health controls"
      subtitle="Configure the portfolio weights and simulation settings used by the health analytics backend."
    >
      <div
        style={{
          display: "grid",
          gap: 20,
        }}
      >
        <div
          style={{
            display: "grid",
            gap: 14,
          }}
        >
          <div
            style={{
              fontSize: "0.82rem",
              letterSpacing: "0.08em",
              textTransform: "uppercase",
              color: "var(--text-faint)",
              fontWeight: 700,
            }}
          >
            Portfolio weights
          </div>

          <div
            style={{
              display: "grid",
              gap: 12,
              gridTemplateColumns: "repeat(auto-fit, minmax(180px, 1fr))",
            }}
          >
            {tickers.map((ticker, index) => (
              <Input
                key={ticker}
                label={`${ticker} weight`}
                type="number"
                min="0"
                max="1"
                step="0.01"
                value={weights[index] ?? ""}
                onChange={(event) =>
                  onChange("weight", {
                    index,
                    value: Number(event.target.value),
                  })
                }
              />
            ))}
          </div>

          <div
            style={{
              padding: "12px 14px",
              borderRadius: "var(--radius-sm)",
              border: "1px solid var(--border-primary)",
              background: "rgba(15, 23, 42, 0.5)",
              color:
                Math.abs(totalWeight - 1) < 0.001
                  ? "var(--success)"
                  : "var(--warning)",
              fontSize: "0.92rem",
              fontWeight: 600,
            }}
          >
            Weight sum: {totalWeight.toFixed(4)}
          </div>
        </div>

        <div
          style={{
            display: "grid",
            gap: 12,
            gridTemplateColumns: "repeat(auto-fit, minmax(180px, 1fr))",
          }}
        >
          <Input
            label="Risk-free rate"
            type="number"
            min="0"
            step="0.005"
            value={values.riskFreeRate}
            onChange={(event) =>
              onChange("riskFreeRate", Number(event.target.value))
            }
          />

          <Input
            label="Simulation count"
            type="number"
            min="500"
            step="100"
            value={values.simulationCount}
            onChange={(event) =>
              onChange("simulationCount", Number(event.target.value))
            }
          />

          <Input
            label="Seed (optional)"
            type="number"
            value={values.seed}
            onChange={(event) => onChange("seed", event.target.value)}
          />
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
            Analyze portfolio health
          </Button>
        </div>
      </div>
    </Card>
  );
}

export default HealthControlsCard;