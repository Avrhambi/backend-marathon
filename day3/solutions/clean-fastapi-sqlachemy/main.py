from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.infrastructure.db import engine, Base
from app.api.routers import router as user_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Create database tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Teardown
    await engine.dispose()

app = FastAPI(title="Day 3 Clean Architecture Service", lifespan=lifespan)
app.include_router(user_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)