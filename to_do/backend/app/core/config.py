import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql+asyncpg://name:password@pg:5432/dbname")
    REDIS_URL: str =  os.getenv("REDIS_URL",'baseredisurl')

    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev-secret")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

settings = Settings()


def get_db_url():
    return settings.DATABASE_URL

def get_jwt_info():
    return {'SECRET_KEY':settings.SECRET_KEY,'ALGORITHM':settings.ALGORITHM,'ACCESS_TOKEN_EXPIRE_MINUTES':settings.ACCESS_TOKEN_EXPIRE_MINUTES}

def get_redis_url():
    return settings.REDIS_URL