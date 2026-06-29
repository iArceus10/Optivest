from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class ExpectedReturnsResponse(BaseModel):
    """
    Annualized expected returns for each asset.
    """

    expected_returns: dict[str, float]

    model_config = ConfigDict(
        from_attributes=True,
    )


class CovarianceMatrixResponse(BaseModel):
    """
    Annualized covariance matrix.
    """

    covariance_matrix: dict[str, dict[str, float]]

    model_config = ConfigDict(
        from_attributes=True,
    )


class CorrelationMatrixResponse(BaseModel):
    """
    Correlation matrix.
    """

    correlation_matrix: dict[str, dict[str, float]]

    model_config = ConfigDict(
        from_attributes=True,
    )


class PortfolioVolatilityResponse(BaseModel):
    """
    Annualized portfolio volatility.
    """

    portfolio_volatility: float

    model_config = ConfigDict(
        from_attributes=True,
    )