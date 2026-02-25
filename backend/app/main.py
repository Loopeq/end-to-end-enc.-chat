from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from app.models import Base
from app.api import router as auth_router
from app.settings import get_settings
from app.crud import engine
from app.redis import init_redis, close_redis
from sqlalchemy import create_engine

settings = get_settings()

async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await init_redis()
    yield
    await close_redis()

app = FastAPI(title=settings.app_name, lifespan=lifespan)
app.include_router(auth_router)
origins = [
    "http://localhost:5137",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
