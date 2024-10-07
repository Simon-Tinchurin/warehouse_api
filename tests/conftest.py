import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.db import get_db, get_test_db, Base, test_engine

# Overriding get_db dependency for tests on test database
app.dependency_overrides[get_db] = get_test_db

# Fixture for creating a test database before tests and cleaning up after tests
@pytest.fixture(scope="session", autouse=True)
async def setup_test_db():
    # Creating tables
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Deleting tables after tests are completed
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

# Fixture for async client
@pytest.fixture(scope="function")
async def async_client():
    transport = ASGITransport(app=app, raise_app_exceptions=False)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client
