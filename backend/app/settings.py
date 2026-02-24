from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    app_name: str
    database_url: str
    postgres_user: str
    postgres_password: str
    postgres_db: str

    access_token_expire_minutes: int
    secret_key: str
    
    class Config:
        env_file = '.env'

@lru_cache
def get_settings():
    return Settings()
