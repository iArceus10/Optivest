from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


# Import ORM models so Alembic discovers them.
from app.models.user import User  # noqa: E402,F401