import { Target } from "lucide-react";
import { useEffect, useMemo, useState } from "react";
import { useParams } from "react-router-dom";

import Card from "../components/common/card";
import AnalysisControlsCard from "../components/portfolio/analysis-controls-card";
import AnalyticsAccordionItem from "../components/portfolio/analytics-accordion-item";
import AnalyticsModuleCard from "../components/portfolio/analytics-module-card";
import AnalyticsTabs from "../components/portfolio/analytics-tabs";
import DataPreviewTable from "../components/portfolio/data-preview-table";
import EfficientFrontierChart from "../components/portfolio/efficient-frontier-chart";
import OptimizationControlsCard from "../components/portfolio/optimization-controls-card";
import OptimizedAllocationTable from "../components/portfolio/optimized-allocation-table";
import PortfolioOverviewCard from "../components/portfolio/portfolio-overview-card";
import RiskControlsCard from "../components/portfolio/risk-controls-card";
import RiskMetricCard from "../components/portfolio/risk-metric-card";
import SimulationControlsCard from "../components/portfolio/simulation-controls-card";
import SimulationHighlightCard from "../components/portfolio/simulation-highlight-card";
import SimulationPortfoliosTable from "../components/portfolio/simulation-portfolios-table";
import SimulationScatterChart from "../components/portfolio/simulation-scatter-chart";

import {
  getDailyReturns,
  getHistoricalPrices,
} from "../services/market-data-service";
import {
  runEfficientFrontier,
  runMaximumSharpeOptimization,
  runMeanVarianceOptimization,
  runMinimumVarianceOptimization,
} from "../services/optimization-service";
import { getPortfolioById } from "../services/portfolio-service";
import { analyzePortfolioRisk } from "../services/risk-service";
import { runMonteCarloSimulation } from "../services/simulation-service";
import {
  getCorrelationMatrix,
  getCovarianceMatrix,
  getExpectedReturns,
} from "../services/statistics-service";

const ANALYTICS_TABS = [
  { id: "market-data", label: "Market Data" },
  { id: "statistics", label: "Statistics" },
  { id: "optimization", label: "Optimization" },
  { id: "risk", label: "Risk" },
  { id: "simulation", label: "Simulation" },
  { id: "health", label: "Health" },
];

function getDefaultAnalysisUniverse() {
  return {
    tickers: ["AAPL", "MSFT", "NVDA"],
    start: "2024-01-01",
    end: "2025-01-01",
  };
}

function createEqualWeights(count) {
  if (!count || count <= 0) {
    return [];
  }

  const weight = Number((1 / count).toFixed(4));
  return Array.from({ length: count }, () => weight);
}

function createMatrixRows(matrix) {
  const tickers = Object.keys(matrix ?? {});
  return tickers.map((ticker) => ({
    id: ticker,
    asset: ticker,
    ...matrix[ticker],
  }));
}

function createMatrixColumns(matrix) {
  const tickers = Object.keys(matrix ?? {});
  return [
    { key: "asset", label: "Asset" },
    ...tickers.map((ticker) => ({
      key: ticker,
      label: ticker,
    })),
  ];
}

function createExpectedReturnsRows(expectedReturns) {
  return Object.entries(expectedReturns ?? {}).map(([ticker, value]) => ({
    id: ticker,
    ticker,
    expected_return: value,
  }));
}

function createPriceRows(response) {
  return (response?.records ?? []).map((record, index) => ({
    id: `${record.date}-${index}`,
    date: record.date,
    ...record.values,
  }));
}

function createPriceColumns(response) {
  const tickers = response?.tickers ?? [];
  return [
    { key: "date", label: "Date" },
    ...tickers.map((ticker) => ({
      key: ticker,
      label: ticker,
    })),
  ];
}

function createFrontierRows(frontier = []) {
  return frontier.map((point, index) => ({
    id: `frontier-${index}`,
    portfolio: `Point ${index + 1}`,
    expected_return: point.expected_return,
    volatility: point.volatility,
    allocations: point.allocations
      .map(
        (allocation) =>
          `${allocation.ticker}: ${(allocation.weight * 100).toFixed(1)}%`
      )
      .join(" | "),
  }));
}

function getSectionStatus({ data, error }) {
  if (error) {
    return "error";
  }

  if (data) {
    return "loaded";
  }

  return "idle";
}

function PortfolioPage() {
  const { portfolioId } = useParams();

  const [portfolio, setPortfolio] = useState(null);
  const [isLoadingPortfolio, setIsLoadingPortfolio] = useState(true);
  const [portfolioError, setPortfolioError] = useState("");

  const [analysisUniverse, setAnalysisUniverse] = useState(
    getDefaultAnalysisUniverse()
  );
  const [activeTab, setActiveTab] = useState("market-data");
  const [isApplyingUniverse, setIsApplyingUniverse] = useState(false);

  const [openSections, setOpenSections] = useState({
    historicalPrices: true,
    dailyReturns: false,
    expectedReturns: true,
    covariance: false,
    correlation: false,
    meanVariance: true,
    minimumVariance: false,
    maximumSharpe: false,
    efficientFrontier: false,
  });

  const [historicalPricesResult, setHistoricalPricesResult] = useState(null);
  const [historicalPricesError, setHistoricalPricesError] = useState("");
  const [isLoadingHistoricalPrices, setIsLoadingHistoricalPrices] =
    useState(false);

  const [dailyReturnsResult, setDailyReturnsResult] = useState(null);
  const [dailyReturnsError, setDailyReturnsError] = useState("");
  const [isLoadingDailyReturns, setIsLoadingDailyReturns] = useState(false);

  const [expectedReturnsResult, setExpectedReturnsResult] = useState(null);
  const [expectedReturnsError, setExpectedReturnsError] = useState("");
  const [isLoadingExpectedReturns, setIsLoadingExpectedReturns] =
    useState(false);

  const [covarianceResult, setCovarianceResult] = useState(null);
  const [covarianceError, setCovarianceError] = useState("");
  const [isLoadingCovariance, setIsLoadingCovariance] = useState(false);

  const [correlationResult, setCorrelationResult] = useState(null);
  const [correlationError, setCorrelationError] = useState("");
  const [isLoadingCorrelation, setIsLoadingCorrelation] = useState(false);

  const [optimizationInputs, setOptimizationInputs] = useState({
    riskAversion: 3,
    riskFreeRate: 0.02,
    numPoints: 20,
  });

  const [meanVarianceResult, setMeanVarianceResult] = useState(null);
  const [meanVarianceError, setMeanVarianceError] = useState("");
  const [isLoadingMeanVariance, setIsLoadingMeanVariance] = useState(false);

  const [minimumVarianceResult, setMinimumVarianceResult] = useState(null);
  const [minimumVarianceError, setMinimumVarianceError] = useState("");
  const [isLoadingMinimumVariance, setIsLoadingMinimumVariance] =
    useState(false);

  const [maximumSharpeResult, setMaximumSharpeResult] = useState(null);
  const [maximumSharpeError, setMaximumSharpeError] = useState("");
  const [isLoadingMaximumSharpe, setIsLoadingMaximumSharpe] = useState(false);

  const [efficientFrontierResult, setEfficientFrontierResult] =
    useState(null);
  const [efficientFrontierError, setEfficientFrontierError] = useState("");
  const [isLoadingEfficientFrontier, setIsLoadingEfficientFrontier] =
    useState(false);

  const [riskInputs, setRiskInputs] = useState({
    weights: createEqualWeights(getDefaultAnalysisUniverse().tickers.length),
    riskFreeRate: 0.02,
    confidenceLevel: 0.95,
  });
  const [riskAnalyticsResult, setRiskAnalyticsResult] = useState(null);
  const [riskAnalyticsError, setRiskAnalyticsError] = useState("");
  const [isLoadingRiskAnalytics, setIsLoadingRiskAnalytics] = useState(false);

  const [simulationInputs, setSimulationInputs] = useState({
    simulationCount: 2500,
    riskFreeRate: 0.02,
    seed: "",
  });
  const [simulationResult, setSimulationResult] = useState(null);
  const [simulationError, setSimulationError] = useState("");
  const [isLoadingSimulation, setIsLoadingSimulation] = useState(false);

  useEffect(() => {
    async function loadPortfolio() {
      try {
        setIsLoadingPortfolio(true);
        setPortfolioError("");
        const response = await getPortfolioById(portfolioId);
        setPortfolio(response);
      } catch (error) {
        setPortfolioError(
          error.message || "Unable to load the selected portfolio."
        );
      } finally {
        setIsLoadingPortfolio(false);
      }
    }

    loadPortfolio();
  }, [portfolioId]);

  useEffect(() => {
    setRiskInputs((previous) => {
      const targetLength = analysisUniverse.tickers.length;
      const previousWeights = Array.isArray(previous.weights)
        ? previous.weights
        : [];

      if (previousWeights.length === targetLength) {
        return previous;
      }

      return {
        ...previous,
        weights: createEqualWeights(targetLength),
      };
    });
  }, [analysisUniverse]);

  function toggleSection(sectionKey) {
    setOpenSections((previous) => ({
      ...previous,
      [sectionKey]: !previous[sectionKey],
    }));
  }

  function handleApplyAnalysisUniverse(nextUniverse) {
    setIsApplyingUniverse(true);

    const parsedTickers = nextUniverse.tickers
      .split(",")
      .map((ticker) => ticker.trim().toUpperCase())
      .filter(Boolean);

    setAnalysisUniverse({
      tickers: parsedTickers.length ? parsedTickers : ["AAPL", "MSFT", "NVDA"],
      start: nextUniverse.start,
      end: nextUniverse.end,
    });

    setTimeout(() => {
      setIsApplyingUniverse(false);
    }, 300);
  }

  function handleOptimizationInputChange(key, value) {
    setOptimizationInputs((previous) => ({
      ...previous,
      [key]: value,
    }));
  }

  function handleRiskInputChange(key, payload) {
    if (key === "weight") {
      setRiskInputs((previous) => {
        const nextWeights = [...(previous.weights || [])];
        nextWeights[payload.index] = payload.value;

        return {
          ...previous,
          weights: nextWeights,
        };
      });
      return;
    }

    setRiskInputs((previous) => ({
      ...previous,
      [key]: payload,
    }));
  }

  function handleSimulationInputChange(key, value) {
    setSimulationInputs((previous) => ({
      ...previous,
      [key]: value,
    }));
  }

  async function handleLoadHistoricalPrices() {
    try {
      setIsLoadingHistoricalPrices(true);
      setHistoricalPricesError("");

      const response = await getHistoricalPrices({
        tickers: analysisUniverse.tickers,
        start: analysisUniverse.start,
        end: analysisUniverse.end,
      });

      setHistoricalPricesResult(response);
    } catch (error) {
      setHistoricalPricesError(
        error.message || "Unable to load historical prices."
      );
    } finally {
      setIsLoadingHistoricalPrices(false);
    }
  }

  async function handleLoadDailyReturns() {
    try {
      setIsLoadingDailyReturns(true);
      setDailyReturnsError("");

      const response = await getDailyReturns({
        tickers: analysisUniverse.tickers,
        start: analysisUniverse.start,
        end: analysisUniverse.end,
      });

      setDailyReturnsResult(response);
    } catch (error) {
      setDailyReturnsError(error.message || "Unable to load daily returns.");
    } finally {
      setIsLoadingDailyReturns(false);
    }
  }

  async function handleLoadExpectedReturns() {
    try {
      setIsLoadingExpectedReturns(true);
      setExpectedReturnsError("");

      const response = await getExpectedReturns({
        tickers: analysisUniverse.tickers,
        start: analysisUniverse.start,
        end: analysisUniverse.end,
      });

      setExpectedReturnsResult(response);
    } catch (error) {
      setExpectedReturnsError(
        error.message || "Unable to compute expected returns."
      );
    } finally {
      setIsLoadingExpectedReturns(false);
    }
  }

  async function handleLoadCovarianceMatrix() {
    try {
      setIsLoadingCovariance(true);
      setCovarianceError("");

      const response = await getCovarianceMatrix({
        tickers: analysisUniverse.tickers,
        start: analysisUniverse.start,
        end: analysisUniverse.end,
      });

      setCovarianceResult(response);
    } catch (error) {
      setCovarianceError(
        error.message || "Unable to compute covariance matrix."
      );
    } finally {
      setIsLoadingCovariance(false);
    }
  }

  async function handleLoadCorrelationMatrix() {
    try {
      setIsLoadingCorrelation(true);
      setCorrelationError("");

      const response = await getCorrelationMatrix({
        tickers: analysisUniverse.tickers,
        start: analysisUniverse.start,
        end: analysisUniverse.end,
      });

      setCorrelationResult(response);
    } catch (error) {
      setCorrelationError(
        error.message || "Unable to compute correlation matrix."
      );
    } finally {
      setIsLoadingCorrelation(false);
    }
  }

  async function handleRunMeanVariance() {
    try {
      setIsLoadingMeanVariance(true);
      setMeanVarianceError("");

      const response = await runMeanVarianceOptimization({
        tickers: analysisUniverse.tickers,
        start: analysisUniverse.start,
        end: analysisUniverse.end,
        riskAversion: optimizationInputs.riskAversion,
      });

      setMeanVarianceResult(response);
    } catch (error) {
      setMeanVarianceError(
        error.message || "Unable to run mean-variance optimization."
      );
    } finally {
      setIsLoadingMeanVariance(false);
    }
  }

  async function handleRunMinimumVariance() {
    try {
      setIsLoadingMinimumVariance(true);
      setMinimumVarianceError("");

      const response = await runMinimumVarianceOptimization({
        tickers: analysisUniverse.tickers,
        start: analysisUniverse.start,
        end: analysisUniverse.end,
      });

      setMinimumVarianceResult(response);
    } catch (error) {
      setMinimumVarianceError(
        error.message || "Unable to run minimum variance optimization."
      );
    } finally {
      setIsLoadingMinimumVariance(false);
    }
  }

  async function handleRunMaximumSharpe() {
    try {
      setIsLoadingMaximumSharpe(true);
      setMaximumSharpeError("");

      const response = await runMaximumSharpeOptimization({
        tickers: analysisUniverse.tickers,
        start: analysisUniverse.start,
        end: analysisUniverse.end,
        riskFreeRate: optimizationInputs.riskFreeRate,
      });

      setMaximumSharpeResult(response);
    } catch (error) {
      setMaximumSharpeError(
        error.message || "Unable to run maximum Sharpe optimization."
      );
    } finally {
      setIsLoadingMaximumSharpe(false);
    }
  }

  async function handleRunEfficientFrontier() {
    try {
      setIsLoadingEfficientFrontier(true);
      setEfficientFrontierError("");

      const response = await runEfficientFrontier({
        tickers: analysisUniverse.tickers,
        start: analysisUniverse.start,
        end: analysisUniverse.end,
        numPoints: optimizationInputs.numPoints,
      });

      setEfficientFrontierResult(response);
    } catch (error) {
      setEfficientFrontierError(
        error.message || "Unable to generate efficient frontier."
      );
    } finally {
      setIsLoadingEfficientFrontier(false);
    }
  }

  async function handleAnalyzeRisk() {
    try {
      setIsLoadingRiskAnalytics(true);
      setRiskAnalyticsError("");

      const normalizedWeights = (riskInputs.weights || []).map((weight) =>
        Number(weight)
      );

      const response = await analyzePortfolioRisk({
        tickers: analysisUniverse.tickers,
        weights: normalizedWeights,
        start: analysisUniverse.start,
        end: analysisUniverse.end,
        riskFreeRate: riskInputs.riskFreeRate,
        confidenceLevel: riskInputs.confidenceLevel,
      });

      setRiskAnalyticsResult(response);
    } catch (error) {
      setRiskAnalyticsError(
        error.message || "Unable to analyze portfolio risk."
      );
    } finally {
      setIsLoadingRiskAnalytics(false);
    }
  }

  async function handleRunSimulation() {
    try {
      setIsLoadingSimulation(true);
      setSimulationError("");

      const response = await runMonteCarloSimulation({
        tickers: analysisUniverse.tickers,
        start: analysisUniverse.start,
        end: analysisUniverse.end,
        simulationCount: simulationInputs.simulationCount,
        riskFreeRate: simulationInputs.riskFreeRate,
        seed: simulationInputs.seed,
      });

      setSimulationResult(response);
    } catch (error) {
      setSimulationError(
        error.message || "Unable to run Monte Carlo simulation."
      );
    } finally {
      setIsLoadingSimulation(false);
    }
  }

  const analysisSummary = useMemo(() => {
    return `${analysisUniverse.tickers.join(", ")} | ${analysisUniverse.start} → ${analysisUniverse.end}`;
  }, [analysisUniverse]);

  const historicalPriceRows = useMemo(
    () => createPriceRows(historicalPricesResult),
    [historicalPricesResult]
  );

  const historicalPriceColumns = useMemo(
    () => createPriceColumns(historicalPricesResult),
    [historicalPricesResult]
  );

  const dailyReturnsRows = useMemo(
    () => createPriceRows(dailyReturnsResult),
    [dailyReturnsResult]
  );

  const dailyReturnsColumns = useMemo(
    () => createPriceColumns(dailyReturnsResult),
    [dailyReturnsResult]
  );

  const expectedReturnsRows = useMemo(
    () => createExpectedReturnsRows(expectedReturnsResult?.expected_returns),
    [expectedReturnsResult]
  );

  const covarianceRows = useMemo(
    () => createMatrixRows(covarianceResult?.covariance_matrix),
    [covarianceResult]
  );

  const covarianceColumns = useMemo(
    () => createMatrixColumns(covarianceResult?.covariance_matrix),
    [covarianceResult]
  );

  const correlationRows = useMemo(
    () => createMatrixRows(correlationResult?.correlation_matrix),
    [correlationResult]
  );

  const correlationColumns = useMemo(
    () => createMatrixColumns(correlationResult?.correlation_matrix),
    [correlationResult]
  );

  const frontierRows = useMemo(
    () => createFrontierRows(efficientFrontierResult?.frontier),
    [efficientFrontierResult]
  );

  const topSimulationPortfolios = useMemo(() => {
    const portfolios = simulationResult?.portfolios || [];
    return [...portfolios]
      .sort(
        (left, right) =>
          Number(right.sharpe_ratio) - Number(left.sharpe_ratio)
      )
      .slice(0, 12);
  }, [simulationResult]);

  if (isLoadingPortfolio) {
    return (
      <div
        style={{
          minHeight: "70vh",
          display: "grid",
          placeItems: "center",
          color: "var(--text-muted)",
        }}
      >
        Loading portfolio workspace…
      </div>
    );
  }

  if (portfolioError || !portfolio) {
    return (
      <Card
        title="Portfolio workspace unavailable"
        subtitle="The selected portfolio could not be loaded."
      >
        <div
          style={{
            padding: "20px",
            borderRadius: "var(--radius-sm)",
            border: "1px solid rgba(239, 68, 68, 0.24)",
            background: "rgba(127, 29, 29, 0.12)",
            color: "#fecaca",
            lineHeight: 1.7,
          }}
        >
          {portfolioError || "Portfolio not found."}
        </div>
      </Card>
    );
  }

  return (
    <div>
      <section className="page-hero">
        <div className="page-hero__content">
          <div className="page-hero__eyebrow">
            <Target size={16} />
            Portfolio analytics workspace
          </div>

          <h1 className="page-hero__title">{portfolio.name}</h1>

          <p className="page-hero__copy">
            This workspace is anchored to the selected portfolio and acts as the
            analytics control surface for market data, statistics,
            optimization, simulation, risk, and portfolio health workflows.
          </p>

          <p
            style={{
              margin: "18px 0 0",
              color: "var(--text-faint)",
              fontSize: "0.94rem",
            }}
          >
            Active analysis universe:{" "}
            <strong style={{ color: "var(--text-secondary)" }}>
              {analysisSummary}
            </strong>
          </p>
        </div>
      </section>

      <section className="dashboard-grid" style={{ marginBottom: 24 }}>
        <div className="dashboard-grid__span-8">
          <PortfolioOverviewCard portfolio={portfolio} />
        </div>

        <div className="dashboard-grid__span-4">
          <AnalysisControlsCard
            initialTickers={analysisUniverse.tickers.join(", ")}
            onApplyAnalysisUniverse={handleApplyAnalysisUniverse}
            isApplying={isApplyingUniverse}
          />
        </div>
      </section>

      <section style={{ marginBottom: 24 }}>
        <AnalyticsTabs
          tabs={ANALYTICS_TABS}
          activeTab={activeTab}
          onChange={setActiveTab}
        />
      </section>

      {activeTab === "market-data" ? (
        <section style={{ display: "grid", gap: 18 }}>
          <AnalyticsAccordionItem
            title="Historical price series"
            description="Retrieve adjusted close price history for the configured analysis universe from the market data backend."
            status={getSectionStatus({
              data: historicalPricesResult,
              error: historicalPricesError,
            })}
            isOpen={openSections.historicalPrices}
            onToggle={() => toggleSection("historicalPrices")}
          >
            {historicalPricesError ? (
              <div
                style={{
                  marginBottom: 16,
                  padding: "14px 16px",
                  borderRadius: "var(--radius-sm)",
                  border: "1px solid rgba(239, 68, 68, 0.24)",
                  background: "rgba(127, 29, 29, 0.12)",
                  color: "#fecaca",
                  lineHeight: 1.7,
                }}
              >
                {historicalPricesError}
              </div>
            ) : null}

            <div style={{ display: "grid", gap: 18 }}>
              <AnalyticsModuleCard
                title="Historical price workflow"
                description="Fetch adjusted close price history for the current analysis universe."
                actionLabel="Load historical prices"
                onAction={handleLoadHistoricalPrices}
                isLoading={isLoadingHistoricalPrices}
              />

              <DataPreviewTable
                title="Historical prices"
                subtitle="Adjusted close price series returned by the market data backend."
                columns={historicalPriceColumns}
                rows={historicalPriceRows}
                emptyMessage="Run the historical price workflow to populate this table."
              />
            </div>
          </AnalyticsAccordionItem>

          <AnalyticsAccordionItem
            title="Daily return series"
            description="Compute daily percentage returns for the configured analysis universe."
            status={getSectionStatus({
              data: dailyReturnsResult,
              error: dailyReturnsError,
            })}
            isOpen={openSections.dailyReturns}
            onToggle={() => toggleSection("dailyReturns")}
          >
            {dailyReturnsError ? (
              <div
                style={{
                  marginBottom: 16,
                  padding: "14px 16px",
                  borderRadius: "var(--radius-sm)",
                  border: "1px solid rgba(239, 68, 68, 0.24)",
                  background: "rgba(127, 29, 29, 0.12)",
                  color: "#fecaca",
                  lineHeight: 1.7,
                }}
              >
                {dailyReturnsError}
              </div>
            ) : null}

            <div style={{ display: "grid", gap: 18 }}>
              <AnalyticsModuleCard
                title="Daily return workflow"
                description="Calculate daily returns for the current analysis universe."
                actionLabel="Load daily returns"
                onAction={handleLoadDailyReturns}
                isLoading={isLoadingDailyReturns}
              />

              <DataPreviewTable
                title="Daily returns"
                subtitle="Daily return series returned by the market data backend."
                columns={dailyReturnsColumns}
                rows={dailyReturnsRows}
                emptyMessage="Run the daily returns workflow to populate this table."
              />
            </div>
          </AnalyticsAccordionItem>
        </section>
      ) : null}

      {activeTab === "statistics" ? (
        <section style={{ display: "grid", gap: 18 }}>
          <AnalyticsAccordionItem
            title="Expected annual returns"
            description="Estimate annualized expected returns for the configured analysis universe."
            status={getSectionStatus({
              data: expectedReturnsResult,
              error: expectedReturnsError,
            })}
            isOpen={openSections.expectedReturns}
            onToggle={() => toggleSection("expectedReturns")}
          >
            {expectedReturnsError ? (
              <div
                style={{
                  marginBottom: 16,
                  padding: "14px 16px",
                  borderRadius: "var(--radius-sm)",
                  border: "1px solid rgba(239, 68, 68, 0.24)",
                  background: "rgba(127, 29, 29, 0.12)",
                  color: "#fecaca",
                  lineHeight: 1.7,
                }}
              >
                {expectedReturnsError}
              </div>
            ) : null}

            <div style={{ display: "grid", gap: 18 }}>
              <AnalyticsModuleCard
                title="Expected return workflow"
                description="Compute annualized expected returns for the current analysis universe."
                actionLabel="Run expected returns"
                onAction={handleLoadExpectedReturns}
                isLoading={isLoadingExpectedReturns}
              />

              <DataPreviewTable
                title="Expected returns"
                subtitle="Annualized expected returns returned by the statistics backend."
                columns={[
                  { key: "ticker", label: "Ticker" },
                  { key: "expected_return", label: "Expected return" },
                ]}
                rows={expectedReturnsRows}
                emptyMessage="Run the expected returns workflow to populate this table."
              />
            </div>
          </AnalyticsAccordionItem>

          <AnalyticsAccordionItem
            title="Covariance matrix"
            description="Compute the annualized covariance matrix for the configured analysis universe."
            status={getSectionStatus({
              data: covarianceResult,
              error: covarianceError,
            })}
            isOpen={openSections.covariance}
            onToggle={() => toggleSection("covariance")}
          >
            {covarianceError ? (
              <div
                style={{
                  marginBottom: 16,
                  padding: "14px 16px",
                  borderRadius: "var(--radius-sm)",
                  border: "1px solid rgba(239, 68, 68, 0.24)",
                  background: "rgba(127, 29, 29, 0.12)",
                  color: "#fecaca",
                  lineHeight: 1.7,
                }}
              >
                {covarianceError}
              </div>
            ) : null}

            <div style={{ display: "grid", gap: 18 }}>
              <AnalyticsModuleCard
                title="Covariance workflow"
                description="Compute the covariance matrix for the current analysis universe."
                actionLabel="Run covariance"
                onAction={handleLoadCovarianceMatrix}
                isLoading={isLoadingCovariance}
              />

              <DataPreviewTable
                title="Covariance matrix"
                subtitle="Annualized covariance matrix returned by the statistics backend."
                columns={covarianceColumns}
                rows={covarianceRows}
                emptyMessage="Run the covariance workflow to populate this table."
              />
            </div>
          </AnalyticsAccordionItem>

          <AnalyticsAccordionItem
            title="Correlation matrix"
            description="Compute the correlation matrix for the configured analysis universe."
            status={getSectionStatus({
              data: correlationResult,
              error: correlationError,
            })}
            isOpen={openSections.correlation}
            onToggle={() => toggleSection("correlation")}
          >
            {correlationError ? (
              <div
                style={{
                  marginBottom: 16,
                  padding: "14px 16px",
                  borderRadius: "var(--radius-sm)",
                  border: "1px solid rgba(239, 68, 68, 0.24)",
                  background: "rgba(127, 29, 29, 0.12)",
                  color: "#fecaca",
                  lineHeight: 1.7,
                }}
              >
                {correlationError}
              </div>
            ) : null}

            <div style={{ display: "grid", gap: 18 }}>
              <AnalyticsModuleCard
                title="Correlation workflow"
                description="Compute the correlation matrix for the current analysis universe."
                actionLabel="Run correlation"
                onAction={handleLoadCorrelationMatrix}
                isLoading={isLoadingCorrelation}
              />

              <DataPreviewTable
                title="Correlation matrix"
                subtitle="Correlation matrix returned by the statistics backend."
                columns={correlationColumns}
                rows={correlationRows}
                emptyMessage="Run the correlation workflow to populate this table."
              />
            </div>
          </AnalyticsAccordionItem>
        </section>
      ) : null}

      {activeTab === "optimization" ? (
        <section style={{ display: "grid", gap: 18 }}>
          <AnalyticsAccordionItem
            title="Mean-variance optimization"
            description="Optimize allocations using the mean-variance objective with a configurable risk-aversion coefficient."
            status={getSectionStatus({
              data: meanVarianceResult,
              error: meanVarianceError,
            })}
            isOpen={openSections.meanVariance}
            onToggle={() => toggleSection("meanVariance")}
          >
            {meanVarianceError ? (
              <div
                style={{
                  marginBottom: 16,
                  padding: "14px 16px",
                  borderRadius: "var(--radius-sm)",
                  border: "1px solid rgba(239, 68, 68, 0.24)",
                  background: "rgba(127, 29, 29, 0.12)",
                  color: "#fecaca",
                  lineHeight: 1.7,
                }}
              >
                {meanVarianceError}
              </div>
            ) : null}

            <div style={{ display: "grid", gap: 18 }}>
              <OptimizationControlsCard
                title="Mean-variance controls"
                description="Run the optimizer using the current analysis universe and the selected risk-aversion coefficient."
                fields={[
                  {
                    key: "riskAversion",
                    label: "Risk aversion",
                    min: 0.01,
                    step: 0.1,
                  },
                ]}
                values={optimizationInputs}
                onChange={handleOptimizationInputChange}
                actionLabel="Run mean-variance optimization"
                onAction={handleRunMeanVariance}
                isLoading={isLoadingMeanVariance}
              />

              <OptimizedAllocationTable
                title="Mean-variance allocations"
                subtitle="Optimized portfolio weights returned by the optimization backend."
                allocations={meanVarianceResult?.allocations}
                emptyMessage="Run mean-variance optimization to populate this table."
              />
            </div>
          </AnalyticsAccordionItem>

          <AnalyticsAccordionItem
            title="Minimum variance portfolio"
            description="Compute the lowest-volatility portfolio available for the current analysis universe."
            status={getSectionStatus({
              data: minimumVarianceResult,
              error: minimumVarianceError,
            })}
            isOpen={openSections.minimumVariance}
            onToggle={() => toggleSection("minimumVariance")}
          >
            {minimumVarianceError ? (
              <div
                style={{
                  marginBottom: 16,
                  padding: "14px 16px",
                  borderRadius: "var(--radius-sm)",
                  border: "1px solid rgba(239, 68, 68, 0.24)",
                  background: "rgba(127, 29, 29, 0.12)",
                  color: "#fecaca",
                  lineHeight: 1.7,
                }}
              >
                {minimumVarianceError}
              </div>
            ) : null}

            <div style={{ display: "grid", gap: 18 }}>
              <OptimizationControlsCard
                title="Minimum variance controls"
                description="Run the minimum variance optimizer using the current analysis universe."
                fields={[]}
                values={optimizationInputs}
                onChange={handleOptimizationInputChange}
                actionLabel="Run minimum variance optimization"
                onAction={handleRunMinimumVariance}
                isLoading={isLoadingMinimumVariance}
              />

              <OptimizedAllocationTable
                title="Minimum variance allocations"
                subtitle="Portfolio weights returned by the minimum variance optimization endpoint."
                allocations={minimumVarianceResult?.allocations}
                emptyMessage="Run minimum variance optimization to populate this table."
              />
            </div>
          </AnalyticsAccordionItem>

          <AnalyticsAccordionItem
            title="Maximum Sharpe portfolio"
            description="Optimize allocations to maximize Sharpe ratio using the configured annual risk-free rate."
            status={getSectionStatus({
              data: maximumSharpeResult,
              error: maximumSharpeError,
            })}
            isOpen={openSections.maximumSharpe}
            onToggle={() => toggleSection("maximumSharpe")}
          >
            {maximumSharpeError ? (
              <div
                style={{
                  marginBottom: 16,
                  padding: "14px 16px",
                  borderRadius: "var(--radius-sm)",
                  border: "1px solid rgba(239, 68, 68, 0.24)",
                  background: "rgba(127, 29, 29, 0.12)",
                  color: "#fecaca",
                  lineHeight: 1.7,
                }}
              >
                {maximumSharpeError}
              </div>
            ) : null}

            <div style={{ display: "grid", gap: 18 }}>
              <OptimizationControlsCard
                title="Maximum Sharpe controls"
                description="Run the maximum Sharpe optimizer using the current analysis universe and annual risk-free rate."
                fields={[
                  {
                    key: "riskFreeRate",
                    label: "Risk-free rate",
                    step: 0.005,
                  },
                ]}
                values={optimizationInputs}
                onChange={handleOptimizationInputChange}
                actionLabel="Run maximum Sharpe optimization"
                onAction={handleRunMaximumSharpe}
                isLoading={isLoadingMaximumSharpe}
              />

              <OptimizedAllocationTable
                title="Maximum Sharpe allocations"
                subtitle="Portfolio weights returned by the maximum Sharpe optimization endpoint."
                allocations={maximumSharpeResult?.allocations}
                emptyMessage="Run maximum Sharpe optimization to populate this table."
              />
            </div>
          </AnalyticsAccordionItem>

          <AnalyticsAccordionItem
            title="Efficient frontier"
            description="Generate multiple optimized portfolios across the feasible risk-return frontier for the current analysis universe."
            status={getSectionStatus({
              data: efficientFrontierResult,
              error: efficientFrontierError,
            })}
            isOpen={openSections.efficientFrontier}
            onToggle={() => toggleSection("efficientFrontier")}
          >
            {efficientFrontierError ? (
              <div
                style={{
                  marginBottom: 16,
                  padding: "14px 16px",
                  borderRadius: "var(--radius-sm)",
                  border: "1px solid rgba(239, 68, 68, 0.24)",
                  background: "rgba(127, 29, 29, 0.12)",
                  color: "#fecaca",
                  lineHeight: 1.7,
                }}
              >
                {efficientFrontierError}
              </div>
            ) : null}

            <div style={{ display: "grid", gap: 18 }}>
              <OptimizationControlsCard
                title="Efficient frontier controls"
                description="Generate a configurable number of frontier portfolios using the current analysis universe."
                fields={[
                  {
                    key: "numPoints",
                    label: "Frontier points",
                    min: 2,
                    step: 1,
                  },
                ]}
                values={optimizationInputs}
                onChange={handleOptimizationInputChange}
                actionLabel="Generate efficient frontier"
                onAction={handleRunEfficientFrontier}
                isLoading={isLoadingEfficientFrontier}
              />

              <EfficientFrontierChart
                points={efficientFrontierResult?.frontier || []}
              />

              <DataPreviewTable
                title="Efficient frontier portfolios"
                subtitle="Frontier portfolios returned by the optimization backend."
                columns={[
                  { key: "portfolio", label: "Portfolio" },
                  { key: "expected_return", label: "Expected return" },
                  { key: "volatility", label: "Volatility" },
                  { key: "allocations", label: "Allocations" },
                ]}
                rows={frontierRows}
                emptyMessage="Generate the efficient frontier to populate this table."
              />
            </div>
          </AnalyticsAccordionItem>
        </section>
      ) : null}

      {activeTab === "risk" ? (
        <section style={{ display: "grid", gap: 18 }}>
          {riskAnalyticsError ? (
            <div
              style={{
                padding: "14px 16px",
                borderRadius: "var(--radius-sm)",
                border: "1px solid rgba(239, 68, 68, 0.24)",
                background: "rgba(127, 29, 29, 0.12)",
                color: "#fecaca",
                lineHeight: 1.7,
              }}
            >
              {riskAnalyticsError}
            </div>
          ) : null}

          <RiskControlsCard
            tickers={analysisUniverse.tickers}
            values={riskInputs}
            onChange={handleRiskInputChange}
            onAnalyze={handleAnalyzeRisk}
            isLoading={isLoadingRiskAnalytics}
          />

          <div
            style={{
              display: "grid",
              gap: 18,
              gridTemplateColumns: "repeat(auto-fit, minmax(220px, 1fr))",
            }}
          >
            <RiskMetricCard
              title="Sharpe ratio"
              description="Annualized excess return per unit of total portfolio volatility."
              value={riskAnalyticsResult?.sharpe_ratio}
              accent="cyan"
            />

            <RiskMetricCard
              title="Sortino ratio"
              description="Annualized excess return per unit of downside volatility only."
              value={riskAnalyticsResult?.sortino_ratio}
              accent="green"
            />

            <RiskMetricCard
              title="Maximum drawdown"
              description="Largest historical peak-to-trough portfolio decline across the selected time window."
              value={riskAnalyticsResult?.maximum_drawdown}
              format="percent"
              accent="rose"
            />

            <RiskMetricCard
              title="Value at Risk"
              description="Historical VaR at the configured confidence level, expressed as a positive loss."
              value={riskAnalyticsResult?.value_at_risk}
              format="percent"
              accent="amber"
            />

            <RiskMetricCard
              title="Conditional VaR"
              description="Expected shortfall beyond the VaR threshold, expressed as a positive loss."
              value={riskAnalyticsResult?.conditional_value_at_risk}
              format="percent"
              accent="rose"
            />
          </div>

          <Card
            title="Risk metric interpretation"
            subtitle="How to read the portfolio risk diagnostics returned by the backend."
          >
            <div
              style={{
                display: "grid",
                gap: 14,
                color: "var(--text-muted)",
                lineHeight: 1.8,
              }}
            >
              <div>
                <strong style={{ color: "var(--text-secondary)" }}>
                  Sharpe Ratio:
                </strong>{" "}
                Measures excess annualized return per unit of total volatility.
              </div>

              <div>
                <strong style={{ color: "var(--text-secondary)" }}>
                  Sortino Ratio:
                </strong>{" "}
                Similar to Sharpe, but penalizes only downside volatility rather
                than total volatility.
              </div>

              <div>
                <strong style={{ color: "var(--text-secondary)" }}>
                  Maximum Drawdown:
                </strong>{" "}
                Captures the largest historical portfolio decline from a prior
                peak during the selected period.
              </div>

              <div>
                <strong style={{ color: "var(--text-secondary)" }}>
                  VaR / CVaR:
                </strong>{" "}
                Quantify downside tail risk. VaR estimates a loss threshold at
                the selected confidence level, while CVaR estimates the average
                loss in the worst tail beyond that threshold.
              </div>
            </div>
          </Card>
        </section>
      ) : null}

      {activeTab === "simulation" ? (
        <section style={{ display: "grid", gap: 18 }}>
          {simulationError ? (
            <div
              style={{
                padding: "14px 16px",
                borderRadius: "var(--radius-sm)",
                border: "1px solid rgba(239, 68, 68, 0.24)",
                background: "rgba(127, 29, 29, 0.12)",
                color: "#fecaca",
                lineHeight: 1.7,
              }}
            >
              {simulationError}
            </div>
          ) : null}

          <SimulationControlsCard
            values={simulationInputs}
            onChange={handleSimulationInputChange}
            onRun={handleRunSimulation}
            isLoading={isLoadingSimulation}
          />

          <div
            style={{
              display: "grid",
              gap: 18,
              gridTemplateColumns: "repeat(auto-fit, minmax(220px, 1fr))",
            }}
          >
            <RiskMetricCard
              title="Simulated portfolios"
              description="Number of random long-only portfolios generated by the Monte Carlo engine."
              value={simulationResult?.portfolios?.length ?? null}
              format="integer"
              accent="cyan"
            />

            <RiskMetricCard
              title="Best Sharpe ratio"
              description="Highest simulated Sharpe ratio across the generated portfolio cloud."
              value={simulationResult?.best_sharpe?.sharpe_ratio}
              accent="green"
            />

            <RiskMetricCard
              title="Minimum volatility"
              description="Lowest annualized volatility found across the simulated portfolio set."
              value={simulationResult?.minimum_volatility?.volatility}
              format="percent"
              accent="amber"
            />

            <RiskMetricCard
              title="Highest expected return"
              description="Largest simulated expected return observed across the generated portfolios."
              value={
                simulationResult?.portfolios?.length
                  ? Math.max(
                      ...simulationResult.portfolios.map((portfolio) =>
                        Number(portfolio.expected_return)
                      )
                    )
                  : null
              }
              format="percent"
              accent="rose"
            />
          </div>

          <div
            style={{
              display: "grid",
              gap: 18,
              gridTemplateColumns: "repeat(auto-fit, minmax(320px, 1fr))",
            }}
          >
            <SimulationHighlightCard
              title="Best Sharpe portfolio"
              subtitle="Portfolio with the highest simulated Sharpe ratio."
              portfolio={simulationResult?.best_sharpe}
              accent="green"
            />

            <SimulationHighlightCard
              title="Minimum volatility portfolio"
              subtitle="Portfolio with the lowest simulated annualized volatility."
              portfolio={simulationResult?.minimum_volatility}
              accent="cyan"
            />
          </div>

          <SimulationScatterChart
            portfolios={simulationResult?.portfolios || []}
          />

          <SimulationPortfoliosTable portfolios={topSimulationPortfolios} />

          <Card
            title="Monte Carlo interpretation"
            subtitle="How to read the simulation output."
          >
            <div
              style={{
                display: "grid",
                gap: 14,
                color: "var(--text-muted)",
                lineHeight: 1.8,
              }}
            >
              <div>
                <strong style={{ color: "var(--text-secondary)" }}>
                  Simulation cloud:
                </strong>{" "}
                Each point represents one randomly generated long-only portfolio
                over the current analysis universe.
              </div>

              <div>
                <strong style={{ color: "var(--text-secondary)" }}>
                  Best Sharpe portfolio:
                </strong>{" "}
                The simulated portfolio with the highest risk-adjusted return
                based on the configured risk-free rate.
              </div>

              <div>
                <strong style={{ color: "var(--text-secondary)" }}>
                  Minimum volatility portfolio:
                </strong>{" "}
                The simulated portfolio with the lowest annualized volatility in
                the generated sample.
              </div>

              <div>
                <strong style={{ color: "var(--text-secondary)" }}>
                  Practical interpretation:
                </strong>{" "}
                Monte Carlo simulation is useful for exploring the feasible
                region of portfolio allocations and understanding the trade-off
                between return, risk, and Sharpe efficiency before choosing a
                candidate allocation.
              </div>
            </div>
          </Card>
        </section>
      ) : null}

      {activeTab === "health" ? (
        <section style={{ display: "grid", gap: 18 }}>
          <Card
            title="Portfolio health workspace"
            subtitle="Portfolio health analytics UI will be wired next on top of the completed backend health engine."
          >
            <div
              style={{
                color: "var(--text-muted)",
                lineHeight: 1.8,
              }}
            >
              The backend health analytics module already exists, but this
              frontend surface has not been integrated yet in the current batch.
              We’ll wire the health score cards, recommendations, and summary
              presentation next without disturbing the market data, statistics,
              optimization, risk, and simulation flows.
            </div>
          </Card>
        </section>
      ) : null}
    </div>
  );
}

export default PortfolioPage;