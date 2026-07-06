import Card from "../common/card";

function SimulationScatterChart({ portfolios = [] }) {
  const width = 920;
  const height = 360;
  const padding = 48;

  if (!portfolios.length) {
    return (
      <Card
        title="Monte Carlo portfolio cloud"
        subtitle="Scatter of simulated portfolios across return and volatility."
      >
        <div
          style={{
            minHeight: 240,
            display: "grid",
            placeItems: "center",
            color: "var(--text-muted)",
            textAlign: "center",
          }}
        >
          Run the simulation to render the portfolio cloud.
        </div>
      </Card>
    );
  }

  const volatilities = portfolios.map((portfolio) => portfolio.volatility);
  const returns = portfolios.map((portfolio) => portfolio.expected_return);
  const sharpes = portfolios.map((portfolio) => portfolio.sharpe_ratio);

  const minX = Math.min(...volatilities);
  const maxX = Math.max(...volatilities);
  const minY = Math.min(...returns);
  const maxY = Math.max(...returns);
  const minSharpe = Math.min(...sharpes);
  const maxSharpe = Math.max(...sharpes);

  function scaleX(value) {
    if (maxX === minX) {
      return padding + (width - padding * 2) / 2;
    }

    return (
      padding +
      ((value - minX) / (maxX - minX)) * (width - padding * 2)
    );
  }

  function scaleY(value) {
    if (maxY === minY) {
      return height / 2;
    }

    return (
      height -
      padding -
      ((value - minY) / (maxY - minY)) * (height - padding * 2)
    );
  }

  function scaleRadius(sharpe) {
    if (maxSharpe === minSharpe) {
      return 4.5;
    }

    return 3.5 + ((sharpe - minSharpe) / (maxSharpe - minSharpe)) * 3.5;
  }

  const points = portfolios.map((portfolio, index) => ({
    ...portfolio,
    id: index,
    x: scaleX(portfolio.volatility),
    y: scaleY(portfolio.expected_return),
    r: scaleRadius(portfolio.sharpe_ratio),
  }));

  return (
    <Card
      title="Monte Carlo portfolio cloud"
      subtitle="Each point is a simulated long-only portfolio. X-axis = volatility, Y-axis = expected return."
    >
      <div style={{ overflowX: "auto" }}>
        <svg
          viewBox={`0 0 ${width} ${height}`}
          width="100%"
          height="360"
          role="img"
          aria-label="Monte Carlo simulation scatter chart"
        >
          <line
            x1={padding}
            y1={height - padding}
            x2={width - padding}
            y2={height - padding}
            stroke="rgba(148, 163, 184, 0.35)"
            strokeWidth="1.5"
          />
          <line
            x1={padding}
            y1={padding}
            x2={padding}
            y2={height - padding}
            stroke="rgba(148, 163, 184, 0.35)"
            strokeWidth="1.5"
          />

          {points.map((point) => (
            <g key={point.id}>
              <circle
                cx={point.x}
                cy={point.y}
                r={point.r}
                fill="rgba(56, 189, 248, 0.55)"
                stroke="rgba(255,255,255,0.18)"
                strokeWidth="1"
              />
              <title>
                {`Return ${point.expected_return.toFixed(4)}, Volatility ${point.volatility.toFixed(4)}, Sharpe ${point.sharpe_ratio.toFixed(4)}`}
              </title>
            </g>
          ))}

          <text
            x={width / 2}
            y={height - 10}
            textAnchor="middle"
            fill="var(--text-faint)"
            fontSize="12"
          >
            Volatility (risk)
          </text>

          <text
            x="14"
            y={height / 2}
            transform={`rotate(-90 14 ${height / 2})`}
            textAnchor="middle"
            fill="var(--text-faint)"
            fontSize="12"
          >
            Expected return
          </text>
        </svg>
      </div>

      <div
        style={{
          marginTop: 12,
          display: "flex",
          flexWrap: "wrap",
          gap: 18,
          color: "var(--text-muted)",
          fontSize: "0.92rem",
        }}
      >
        <span>Portfolios: {portfolios.length}</span>
        <span>Volatility range: {minX.toFixed(4)} → {maxX.toFixed(4)}</span>
        <span>Return range: {minY.toFixed(4)} → {maxY.toFixed(4)}</span>
        <span>Sharpe range: {minSharpe.toFixed(4)} → {maxSharpe.toFixed(4)}</span>
      </div>
    </Card>
  );
}

export default SimulationScatterChart;