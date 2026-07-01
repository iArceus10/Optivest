from __future__ import annotations

from fastapi import APIRouter, HTTPException, status

from app.financial_engines.simulation.models import (
    MonteCarloPortfolio,
)
from app.schemas.simulation import (
    MonteCarloPortfolioResponse,
    MonteCarloSimulationRequest,
    MonteCarloSimulationResponse,
    PortfolioWeight,
)
from app.services.simulation_service import (
    SimulationService,
)

router = APIRouter(
    prefix="/simulation",
    tags=["Monte Carlo Simulation"],
)


def _serialize_portfolio(
    portfolio: MonteCarloPortfolio,
) -> MonteCarloPortfolioResponse:
    """
    Serialize a Monte Carlo portfolio into an API response model.
    """

    return MonteCarloPortfolioResponse(
        expected_return=portfolio.expected_return,
        volatility=portfolio.volatility,
        sharpe_ratio=portfolio.sharpe_ratio,
        allocations=[
            PortfolioWeight(
                ticker=ticker,
                weight=float(weight),
            )
            for ticker, weight in portfolio.weights.items()
        ],
    )


@router.post(
    "",
    response_model=MonteCarloSimulationResponse,
    summary="Run Monte Carlo portfolio simulation",
)
def run_simulation(
    request: MonteCarloSimulationRequest,
) -> MonteCarloSimulationResponse:
    """
    Execute Monte Carlo portfolio simulation.
    """

    try:
        result = SimulationService.run_simulation(
            tickers=request.tickers,
            start=request.start,
            end=request.end,
            simulation_count=request.simulation_count,
            risk_free_rate=request.risk_free_rate,
            seed=request.seed,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    return MonteCarloSimulationResponse(
        portfolios=[
            _serialize_portfolio(portfolio)
            for portfolio in result.portfolios
        ],
        best_sharpe=_serialize_portfolio(
            result.best_sharpe,
        ),
        minimum_volatility=_serialize_portfolio(
            result.minimum_volatility,
        ),
    )