import os

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker

# ------------------------------------------------------------------
# Configure an isolated SQLite database for testing.
# ------------------------------------------------------------------

os.environ["DATABASE_URL"] = "sqlite://"

from app.database.base import Base
from app.database.session import get_db
from app.main import app

engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)

Base.metadata.create_all(bind=engine)


def override_get_db():
    """
    Provide a fresh database session for each test.
    """

    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture
def client():
    """
    FastAPI TestClient using the isolated SQLite database.
    """

    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    with TestClient(app) as test_client:
        yield test_client