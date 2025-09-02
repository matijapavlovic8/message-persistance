import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import Base, engine

# Make sure tables exist before running tests
Base.metadata.create_all(bind=engine)

@pytest.fixture(scope="session")
def client():
    with TestClient(app) as c:
        yield c
