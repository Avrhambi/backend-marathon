import os
import time
import uuid
from typing import AsyncGenerator
from contextlib import asynccontextmanager

import structlog
from fastapi import FastAPI, Depends, HTTPException, status, Request, Response
from pydantic import BaseModel, ConfigDict
from sqlalchemy import String, select
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_sessionmaker,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

# ---------------------------------------------------------
# 1. Observability: Structured Logging Setup
# ---------------------------------------------------------
structlog.configure(
    processors=[
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer(),
    ]
)
logger = structlog.get_logger()

# ---------------------------------------------------------
# 2. Database Models & Schema
# ---------------------------------------------------------
class Base(DeclarativeBase):
    pass

class UserItem(Base):
    __tablename__ = "user_items"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    metadata_payload: Mapped[dict] = mapped_column(
        JSONB, nullable=False, default=dict
    )

# ---------------------------------------------------------
# 3. Pydantic Request / Response Schemas
# ---------------------------------------------------------
class ItemCreate(BaseModel):
    name: str
    metadata_payload: dict = {}

class ItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str
    metadata_payload: dict

# ---------------------------------------------------------
# 4. Dynamic Database Engine & Lifespan Management
# ---------------------------------------------------------
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://postgres:postgres@localhost:5432/app_db",
)

engine = create_async_engine(DATABASE_URL, echo=False, pool_pre_ping=True)
async_session_factory = async_sessionmaker(engine, expire_on_commit=False)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_factory() as session:
        yield session

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Ready to accept requests
    yield
    # Graceful Shutdown on SIGTERM: Dispose connection pool cleanly
    await engine.dispose()

# ---------------------------------------------------------
# 5. FastAPI Application & Middleware
# ---------------------------------------------------------
app = FastAPI(title="Day 5 Backend Service", lifespan=lifespan)

@app.middleware("http")
async def logging_middleware(request: Request, call_next):
    # Clear context from any previous request on this task worker
    structlog.contextvars.clear_contextvars()
    
    req_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
    structlog.contextvars.bind_contextvars(
        request_id=req_id,
        path=request.url.path,
        method=request.method,
    )

    start_time = time.perf_counter()
    try:
        response: Response = await call_next(request)
        duration_ms = (time.perf_counter() - start_time) * 1000
        logger.info(
            "http_request_processed",
            status_code=response.status_code,
            duration_ms=round(duration_ms, 2),
        )
        response.headers["X-Request-ID"] = req_id
        return response
    except Exception as exc:
        duration_ms = (time.perf_counter() - start_time) * 1000
        logger.error(
            "http_request_failed",
            error=str(exc),
            duration_ms=round(duration_ms, 2),
        )
        raise 

# ---------------------------------------------------------
# 6. Endpoints & Probes
# ---------------------------------------------------------
@app.get("/health", status_code=status.HTTP_200_OK)
async def health_check():
    """Liveness probe used by Docker HEALTHCHECK and orchestrators."""
    return {"status": "healthy", "service": "backend-api"}

@app.post("/items", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
async def create_item(payload: ItemCreate, db: AsyncSession = Depends(get_db)):
    item = UserItem(name=payload.name, metadata_payload=payload.metadata_payload)
    db.add(item)
    await db.commit()
    await db.refresh(item)
    return item

@app.get("/items/{item_id}", response_model=ItemResponse)
async def get_item(item_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    query = select(UserItem).where(UserItem.id == item_id)
    result = await db.execute(query)
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Item not found"
        )
    return item