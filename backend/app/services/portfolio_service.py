from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.portfolio import Portfolio
from app.schemas.portfolio import PortfolioCreate, PortfolioUpdate


class PortfolioService:
    """
    Business logic for portfolio management.
    """

    @staticmethod
    def create_portfolio(
        db: Session,
        *,
        user_id: UUID,
        portfolio_data: PortfolioCreate,
    ) -> Portfolio:
        """
        Create a new portfolio.
        """

        portfolio = Portfolio(
            user_id=user_id,
            name=portfolio_data.name,
            description=portfolio_data.description,
        )

        try:
            db.add(portfolio)
            db.commit()
            db.refresh(portfolio)
            return portfolio
        except Exception:
            db.rollback()
            raise

    @staticmethod
    def get_user_portfolios(
        db: Session,
        *,
        user_id: UUID,
    ) -> list[Portfolio]:
        """
        Return all portfolios owned by a user.
        """

        statement = (
            select(Portfolio)
            .where(Portfolio.user_id == user_id)
            .order_by(Portfolio.created_at.desc())
        )

        return list(db.scalars(statement).all())

    @staticmethod
    def get_portfolio(
        db: Session,
        *,
        portfolio_id: UUID,
        user_id: UUID,
    ) -> Portfolio | None:
        """
        Return a portfolio only if it belongs to the user.
        """

        statement = (
            select(Portfolio)
            .where(
                Portfolio.id == portfolio_id,
                Portfolio.user_id == user_id,
            )
        )

        return db.scalar(statement)

    @staticmethod
    def update_portfolio(
        db: Session,
        *,
        portfolio: Portfolio,
        portfolio_data: PortfolioUpdate,
    ) -> Portfolio:
        """
        Update an existing portfolio.
        """

        update_data = portfolio_data.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(portfolio, field, value)

        try:
            db.commit()
            db.refresh(portfolio)
            return portfolio
        except Exception:
            db.rollback()
            raise

    @staticmethod
    def delete_portfolio(
        db: Session,
        *,
        portfolio: Portfolio,
    ) -> None:
        """
        Delete a portfolio.
        """

        try:
            db.delete(portfolio)
            db.commit()
        except Exception:
            db.rollback()
            raise