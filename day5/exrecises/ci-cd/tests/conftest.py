import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from testcontainers.postgres import PostgresContainer
from app.main import app, Base, get_db

@pytest.fixture(scope="session")
def postgres_container():
    """Starts an ephemeral Postgres container for the entire test session."""
    with PostgresContainer("postgres:16-alpine") as postgres:
        yield postgres

@pytest_asyncio.fixture(scope="session")
async def db_engine(postgres_container):
    """Initializes schema once on the containerized database."""
    # Convert connection URL to asyncpg driver
    sync_url = postgres_container.get_connection_url()
    async_url = sync_url.replace("postgresql+psycopg2://", "postgresql+asyncpg://")
    
    engine = create_async_engine(async_url, echo=False)
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        
    yield engine
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()

@pytest_asyncio.fixture(scope="function")
async def db_session(db_engine):
    """Provides an isolated session wrapped in an outer transaction that rolls back."""
    connection = await db_engine.connect()
    transaction = await connection.begin()
    
    session_factory = async_sessionmaker(
        bind=connection,
        expire_on_commit=False,
        class_=AsyncSession
    )
    session = session_factory()
    
    yield session
    
    await session.close()
    await transaction.rollback()
    await connection.close()

@pytest_asyncio.fixture(scope="function")
async def client(db_session):
    """FastAPI test client with the database dependency overridden."""
    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac
    app.dependency_overrides.clear()