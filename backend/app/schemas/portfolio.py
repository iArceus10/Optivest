from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class PortfolioCreate(BaseModel):
    """
    Schema for creating a new portfolio.
    """

    name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Portfolio name",
    )

    description: str | None = Field(
        default=None,
        max_length=1000,
        description="Optional portfolio description",
    )


class PortfolioUpdate(BaseModel):
    """
    Schema for updating an existing portfolio.

    All fields are optional to support partial updates.
    """

    name: str | None = Field(
        default=None,
        min_length=1,
        max_length=100,
    )

    description: str | None = Field(
        default=None,
        max_length=1000,
    )


class PortfolioResponse(BaseModel):
    """
    Portfolio response returned by the API.
    """

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    user_id: UUID
    name: str
    description: str | None
    created_at: datetime
    updated_at: datetime