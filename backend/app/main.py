from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from app.models import Base
from app.api import router as auth_router
from app.settings import get_settings
from sqlalchemy import create_engine

settings = get_settings()
app = FastAPI(title=settings.app_name)
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

engine = create_engine(settings.database_url)
Base.metadata.create_all(bind=engine)
