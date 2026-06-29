from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.api.dependencies.auth import get_current_user
from app.database.session import get_db
from app.models.user import User
from app.schemas.portfolio import (
    PortfolioCreate,
    PortfolioResponse,
    PortfolioUpdate,
)
from app.services.portfolio_service import PortfolioService

router = APIRouter(
    prefix="/portfolios",
    tags=["Portfolio"],
)


@router.post(
    "",
    response_model=PortfolioResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_portfolio(
    portfolio_data: PortfolioCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> PortfolioResponse:
    """
    Create a new portfolio for the authenticated user.
    """

    portfolio = PortfolioService.create_portfolio(
        db=db,
        user_id=current_user.id,
        portfolio_data=portfolio_data,
    )

    return PortfolioResponse.model_validate(portfolio)


@router.get(
    "",
    response_model=list[PortfolioResponse],
)
def get_user_portfolios(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[PortfolioResponse]:
    """
    Retrieve all portfolios belonging to the authenticated user.
    """

    portfolios = PortfolioService.get_user_portfolios(
        db=db,
        user_id=current_user.id,
    )

    return [
        PortfolioResponse.model_validate(portfolio)
        for portfolio in portfolios
    ]


@router.get(
    "/{portfolio_id}",
    response_model=PortfolioResponse,
)
def get_portfolio(
    portfolio_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> PortfolioResponse:
    """
    Retrieve a portfolio owned by the authenticated user.
    """

    portfolio = PortfolioService.get_portfolio(
        db=db,
        portfolio_id=portfolio_id,
        user_id=current_user.id,
    )

    if portfolio is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Portfolio not found.",
        )

    return PortfolioResponse.model_validate(portfolio)


@router.patch(
    "/{portfolio_id}",
    response_model=PortfolioResponse,
)
def update_portfolio(
    portfolio_id: UUID,
    portfolio_data: PortfolioUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> PortfolioResponse:
    """
    Update a portfolio owned by the authenticated user.
    """

    portfolio = PortfolioService.get_portfolio(
        db=db,
        portfolio_id=portfolio_id,
        user_id=current_user.id,
    )

    if portfolio is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Portfolio not found.",
        )

    updated_portfolio = PortfolioService.update_portfolio(
        db=db,
        portfolio=portfolio,
        portfolio_data=portfolio_data,
    )

    return PortfolioResponse.model_validate(updated_portfolio)


@router.delete(
    "/{portfolio_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_portfolio(
    portfolio_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Response:
    """
    Delete a portfolio owned by the authenticated user.
    """

    portfolio = PortfolioService.get_portfolio(
        db=db,
        portfolio_id=portfolio_id,
        user_id=current_user.id,
    )

    if portfolio is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Portfolio not found.",
        )

    PortfolioService.delete_portfolio(
        db=db,
        portfolio=portfolio,
    )

    return Response(status_code=status.HTTP_204_NO_CONTENT)