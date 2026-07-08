import { Target } from "lucide-react";
import { useEffect, useMemo, useRef, useState } from "react";
import { useParams } from "react-router-dom";

import Card from "../components/common/card";
import AnalysisControlsCard from "../components/portfolio/analysis-controls-card";
import AnalyticsAccordionItem from "../components/portfolio/analytics-accordion-item";
import AnalyticsModuleCard from "../components/portfolio/analytics-module-card";
import AnalyticsTabs from "../components/portfolio/analytics-tabs";
import DataPreviewTable from "../components/portfolio/data-preview-table";
import EfficientFrontierChart from "../components/portfolio/efficient-frontier-chart";
import HealthControlsCard from "../components/portfolio/health-controls-card";
import OptimizationControlsCard from "../components/portfolio/optimization-controls-card";
import OptimizedAllocationTable from "../components/portfolio/optimized-allocation-table";
import PortfolioHealthSummaryCard from "../components/portfolio/portfolio-health-summary-card";
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
import { analyzePortfolioHealth } from "../services/portfolio-health-service";
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

const DEFAULT_ANALYSIS_UNIVERSE = Object.freeze({
  tickers: ["AAPL", "MSFT", "NVDA"],
  start: "2024-01-01",
  end: "2025-01-01",
});

function getDefaultAnalysisUniverse() {
  return {
    tickers: [...DEFAULT_ANALYSIS_UNIVERSE.tickers],
    start: DEFAULT_ANALYSIS_UNIVERSE.start,
    end: DEFAULT_ANALYSIS_UNIVERSE.end,
  };
}

function createEqualWeights(count) {
  if (!count || count <= 0) {
    return [];
  }

  const rawWeight = 1 / count;

  return Array.from({ length: count }, (_, index) => {
    if (index === count - 1) {
      const used = rawWeight * (count - 1);
      return Number((1 - used).toFixed(6));
    }

    return Number(rawWeight.toFixed(6));
  });
}

function toNumber(value, fallback = 0) {
  const numeric = Number(value);
  return Number.isFinite(numeric) ? numeric : fallback;
}

function normalizeTickerList(rawTickers) {
  if (Array.isArray(rawTickers)) {
    return rawTickers
      .map((ticker) => String(ticker ?? "").trim().toUpperCase())
      .filter(Boolean);
  }

  if (typeof rawTickers === "string") {
    return rawTickers
      .split(",")
      .map((ticker) => ticker.trim().toUpperCase())
      .filter(Boolean);
  }

  return [];
}

function extractPortfolioTickers(portfolio) {
  const holdings = Array.isArray(portfolio?.holdings) ? portfolio.holdings : [];

  const tickers = holdings
    .map((holding) => {
      if (typeof holding?.ticker === "string") {
        return holding.ticker;
      }

      if (typeof holding?.symbol === "string") {
        return holding.symbol;
      }

      if (typeof holding?.asset_ticker === "string") {
        return holding.asset_ticker;
      }

      return "";
    })
    .map((ticker) => ticker.trim().toUpperCase())
    .filter(Boolean);

  return [...new Set(tickers)];
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
    allocations: (point.allocations ?? [])
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

function renderErrorBanner(message) {
  if (!message) {
    return null;
  }

  return (
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
      {message}
    </div>
  );
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

  const didHydrateUniverseFromPortfolio = useRef(false);

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

  const [efficientFrontierResult, setEfficientFrontierResult] = useState(null);
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

  const [healthInputs, setHealthInputs] = useState({
    weights: createEqualWeights(getDefaultAnalysisUniverse().tickers.length),
    riskFreeRate: 0.02,
    simulationCount: 2500,
    seed: "",
  });
  const [portfolioHealthResult, setPortfolioHealthResult] = useState(null);
  const [portfolioHealthError, setPortfolioHealthError] = useState("");
  const [isLoadingPortfolioHealth, setIsLoadingPortfolioHealth] =
    useState(false);

  function resetAnalyticsState() {
    setHistoricalPricesResult(null);
    setHistoricalPricesError("");
    setDailyReturnsResult(null);
    setDailyReturnsError("");
    setExpectedReturnsResult(null);
    setExpectedReturnsError("");
    setCovarianceResult(null);
    setCovarianceError("");
    setCorrelationResult(null);
    setCorrelationError("");

    setMeanVarianceResult(null);
    setMeanVarianceError("");
    setMinimumVarianceResult(null);
    setMinimumVarianceError("");
    setMaximumSharpeResult(null);
    setMaximumSharpeError("");
    setEfficientFrontierResult(null);
    setEfficientFrontierError("");

    setRiskAnalyticsResult(null);
    setRiskAnalyticsError("");

    setSimulationResult(null);
    setSimulationError("");

    setPortfolioHealthResult(null);
    setPortfolioHealthError("");
  }

  useEffect(() => {
    async function loadPortfolio() {
      try {
        setIsLoadingPortfolio(true);
        setPortfolioError("");
        didHydrateUniverseFromPortfolio.current = false;

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
    if (!portfolio || didHydrateUniverseFromPortfolio.current) {
      return;
    }

    const portfolioTickers = extractPortfolioTickers(portfolio);

    setAnalysisUniverse((previous) => ({
      tickers:
        portfolioTickers.length > 0
          ? portfolioTickers
          : [...DEFAULT_ANALYSIS_UNIVERSE.tickers],
      start: previous?.start || DEFAULT_ANALYSIS_UNIVERSE.start,
      end: previous?.end || DEFAULT_ANALYSIS_UNIVERSE.end,
    }));

    resetAnalyticsState();
    didHydrateUniverseFromPortfolio.current = true;
  }, [portfolio]);

  useEffect(() => {
    const targetLength = analysisUniverse.tickers.length;

    setRiskInputs((previous) => ({
      ...previous,
      weights: createEqualWeights(targetLength),
    }));

    setHealthInputs((previous) => ({
      ...previous,
      weights: createEqualWeights(targetLength),
    }));
  }, [analysisUniverse.tickers]);

  function toggleSection(sectionKey) {
    setOpenSections((previous) => ({
      ...previous,
      [sectionKey]: !previous[sectionKey],
    }));
  }

  async function handleApplyAnalysisUniverse(nextUniverse) {
    setIsApplyingUniverse(true);

    try {
      const parsedTickers = normalizeTickerList(nextUniverse?.tickers);
      const nextTickers = parsedTickers.length
        ? parsedTickers
        : [...DEFAULT_ANALYSIS_UNIVERSE.tickers];

      const nextStart =
        typeof nextUniverse?.start === "string" && nextUniverse.start.trim()
          ? nextUniverse.start
          : analysisUniverse.start;

      const nextEnd =
        typeof nextUniverse?.end === "string" && nextUniverse.end.trim()
          ? nextUniverse.end
          : analysisUniverse.end;

      setAnalysisUniverse({
        tickers: nextTickers,
        start: nextStart,
        end: nextEnd,
      });

      resetAnalyticsState();
      setActiveTab("market-data");
    } finally {
      setIsApplyingUniverse(false);
    }
  }

  function handleOptimizationInputChange(key, value) {
    setOptimizationInputs((previous) => ({
      ...previous,
      [key]: toNumber(value, previous[key]),
    }));
  }

  function handleRiskInputChange(key, payload) {
    if (key === "weight") {
      setRiskInputs((previous) => {
        const nextWeights = [...(previous.weights || [])];
        nextWeights[payload.index] = toNumber(payload.value, 0);

        return {
          ...previous,
          weights: nextWeights,
        };
      });
      return;
    }

    setRiskInputs((previous) => ({
      ...previous,
      [key]: toNumber(payload, previous[key]),
    }));
  }

  function handleSimulationInputChange(key, value) {
    setSimulationInputs((previous) => ({
      ...previous,
      [key]: key === "seed" ? value : toNumber(value, previous[key]),
    }));
  }

  function handleHealthInputChange(key, payload) {
    if (key === "weight") {
      setHealthInputs((previous) => {
        const nextWeights = [...(previous.weights || [])];
        nextWeights[payload.index] = toNumber(payload.value, 0);

        return {
          ...previous,
          weights: nextWeights,
        };
      });
      return;
    }

    setHealthInputs((previous) => ({
      ...previous,
      [key]: key === "seed" ? payload : toNumber(payload, previous[key]),
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
        toNumber(weight, 0)
      );

      const response = await analyzePortfolioRisk({
        tickers: analysisUniverse.tickers,
        weights: normalizedWeights,
        start: analysisUniverse.start,
        end: analysisUniverse.end,
        riskFreeRate: toNumber(riskInputs.riskFreeRate, 0.02),
        confidenceLevel: toNumber(riskInputs.confidenceLevel, 0.95),
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
        simulationCount: toNumber(simulationInputs.simulationCount, 2500),
        riskFreeRate: toNumber(simulationInputs.riskFreeRate, 0.02),
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

  async function handleAnalyzePortfolioHealth() {
    try {
      setIsLoadingPortfolioHealth(true);
      setPortfolioHealthError("");

      const normalizedWeights = (healthInputs.weights || []).map((weight) =>
        toNumber(weight, 0)
      );

      const response = await analyzePortfolioHealth({
        tickers: analysisUniverse.tickers,
        weights: normalizedWeights,
        start: analysisUniverse.start,
        end: analysisUniverse.end,
        riskFreeRate: toNumber(healthInputs.riskFreeRate, 0.02),
        simulationCount: toNumber(healthInputs.simulationCount, 2500),
        seed: healthInputs.seed,
      });

      setPortfolioHealthResult(response);
    } catch (error) {
      setPortfolioHealthError(
        error.message || "Unable to analyze portfolio health."
      );
    } finally {
      setIsLoadingPortfolioHealth(false);
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
            {renderErrorBanner(historicalPricesError)}

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
            {renderErrorBanner(dailyReturnsError)}

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
            {renderErrorBanner(expectedReturnsError)}

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
            {renderErrorBanner(covarianceError)}

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
            {renderErrorBanner(correlationError)}

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
            {renderErrorBanner(meanVarianceError)}

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
            {renderErrorBanner(minimumVarianceError)}

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
            {renderErrorBanner(maximumSharpeError)}

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
            {renderErrorBanner(efficientFrontierError)}

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
          {renderErrorBanner(riskAnalyticsError)}

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
          {renderErrorBanner(simulationError)}

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
          {renderErrorBanner(portfolioHealthError)}

          <HealthControlsCard
            tickers={analysisUniverse.tickers}
            values={healthInputs}
            onChange={handleHealthInputChange}
            onAnalyze={handleAnalyzePortfolioHealth}
            isLoading={isLoadingPortfolioHealth}
          />

          <PortfolioHealthSummaryCard result={portfolioHealthResult} />

          <div
            style={{
              display: "grid",
              gap: 18,
              gridTemplateColumns: "repeat(auto-fit, minmax(220px, 1fr))",
            }}
          >
            <RiskMetricCard
              title="Return score"
              description="Score derived from expected annual return quality."
              value={portfolioHealthResult?.return_score}
              accent="green"
            />

            <RiskMetricCard
              title="Risk score"
              description="Composite risk score using Sharpe ratio, drawdown, and Value at Risk."
              value={portfolioHealthResult?.risk_score}
              accent="cyan"
            />

            <RiskMetricCard
              title="Diversification score"
              description="Score based on portfolio weight dispersion and diversification quality."
              value={portfolioHealthResult?.diversification_score}
              accent="amber"
            />

            <RiskMetricCard
              title="Concentration score"
              description="Score based on largest-position concentration risk."
              value={portfolioHealthResult?.concentration_score}
              accent="rose"
            />

            <RiskMetricCard
              title="Optimization efficiency"
              description="Portfolio efficiency relative to the best Monte Carlo Sharpe portfolio."
              value={portfolioHealthResult?.optimization_efficiency_score}
              accent="green"
            />
          </div>

          <Card
            title="Health recommendations"
            subtitle="Actionable recommendations generated by the portfolio health engine."
          >
            {portfolioHealthResult?.recommendations?.length ? (
              <div
                style={{
                  display: "grid",
                  gap: 12,
                }}
              >
                {portfolioHealthResult.recommendations.map(
                  (recommendation, index) => (
                    <div
                      key={`${recommendation}-${index}`}
                      style={{
                        padding: "14px 16px",
                        borderRadius: "var(--radius-sm)",
                        border: "1px solid var(--border-primary)",
                        background: "rgba(15, 23, 42, 0.48)",
                        color: "var(--text-secondary)",
                        lineHeight: 1.7,
                      }}
                    >
                      {recommendation}
                    </div>
                  )
                )}
              </div>
            ) : (
              <div
                style={{
                  color: "var(--text-muted)",
                  lineHeight: 1.8,
                }}
              >
                Run portfolio health analysis to receive portfolio construction
                recommendations from the backend health engine.
              </div>
            )}
          </Card>

          <Card
            title="How to read portfolio health"
            subtitle="Interpretation of the backend health score dimensions."
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
                  Overall health score:
                </strong>{" "}
                A composite 0–100 portfolio quality score combining return
                quality, risk quality, diversification, concentration control,
                and optimization efficiency.
              </div>

              <div>
                <strong style={{ color: "var(--text-secondary)" }}>
                  Return score:
                </strong>{" "}
                Evaluates how attractive the expected annual return is relative
                to the engine’s scoring thresholds.
              </div>

              <div>
                <strong style={{ color: "var(--text-secondary)" }}>
                  Risk score:
                </strong>{" "}
                Rewards stronger Sharpe ratios and penalizes large drawdowns and
                large Value-at-Risk.
              </div>

              <div>
                <strong style={{ color: "var(--text-secondary)" }}>
                  Diversification and concentration:
                </strong>{" "}
                These scores inspect whether capital is spread sensibly across
                holdings or over-concentrated in a few positions.
              </div>

              <div>
                <strong style={{ color: "var(--text-secondary)" }}>
                  Optimization efficiency:
                </strong>{" "}
                Compares the portfolio’s Sharpe quality to the best Sharpe ratio
                discovered during Monte Carlo simulation.
              </div>
            </div>
          </Card>
        </section>
      ) : null}
    </div>
  );
}

export default PortfolioPage;