import DataPreviewTable from "./data-preview-table";

function buildRows(portfolios = []) {
  return portfolios.map((portfolio, index) => ({
    id: `simulation-${index}`,
    portfolio: `Portfolio ${index + 1}`,
    expected_return: portfolio.expected_return,
    volatility: portfolio.volatility,
    sharpe_ratio: portfolio.sharpe_ratio,
    allocations: portfolio.allocations
      .map(
        (allocation) =>
          `${allocation.ticker}: ${(allocation.weight * 100).toFixed(1)}%`
      )
      .join(" | "),
  }));
}

function SimulationPortfoliosTable({ portfolios = [] }) {
  return (
    <DataPreviewTable
      title="Top simulated portfolios"
      subtitle="Preview of the highest-Sharpe simulated portfolios from the Monte Carlo engine."
      columns={[
        { key: "portfolio", label: "Portfolio" },
        { key: "expected_return", label: "Expected return" },
        { key: "volatility", label: "Volatility" },
        { key: "sharpe_ratio", label: "Sharpe ratio" },
        { key: "allocations", label: "Allocations" },
      ]}
      rows={buildRows(portfolios)}
      emptyMessage="Run the Monte Carlo simulation to populate this table."
    />
  );
}

export default SimulationPortfoliosTable;