import DataPreviewTable from "./data-preview-table";

function formatAllocationRows(allocations = []) {
  return allocations.map((allocation, index) => ({
    id: `${allocation.ticker}-${index}`,
    ticker: allocation.ticker,
    weight: allocation.weight,
    weight_percent: `${(allocation.weight * 100).toFixed(2)}%`,
  }));
}

function OptimizedAllocationTable({
  title,
  subtitle,
  allocations,
  emptyMessage,
}) {
  return (
    <DataPreviewTable
      title={title}
      subtitle={subtitle}
      columns={[
        { key: "ticker", label: "Ticker" },
        { key: "weight", label: "Weight" },
        { key: "weight_percent", label: "Weight %" },
      ]}
      rows={formatAllocationRows(allocations)}
      emptyMessage={emptyMessage}
    />
  );
}

export default OptimizedAllocationTable;