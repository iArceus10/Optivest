"""
Portfolio Health Financial Engine.

This package provides deterministic, framework-independent portfolio
health diagnostics by synthesizing outputs from the Statistics,
Simulation, Optimization, and Risk Analytics engines.

The Portfolio Health Engine performs no statistical estimation,
optimization, simulation, or market data retrieval. It evaluates
precomputed portfolio metrics and produces normalized health scores,
summaries, and deterministic investment recommendations.

Public API:

- PortfolioHealthResult
- analyze_portfolio_health
"""

from .health import (
    analyze_portfolio_health,
)
from .models import (
    PortfolioHealthResult,
)

__all__ = [
    "PortfolioHealthResult",
    "analyze_portfolio_health",
]