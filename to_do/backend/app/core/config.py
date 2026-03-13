import os
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    REDIS_URL: str =  os.getenv("REDIS_URL")


    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ALGORITHM: str = os.getenv("ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

    CORS_ORIGINS: list = eval(os.getenv("CORS_ORIGINS"))


settings = Settings()


def get_db_url():
    return settings.DATABASE_URL

def get_jwt_info():
    return {'SECRET_KEY':settings.SECRET_KEY,'ALGORITHM':settings.ALGORITHM,'ACCESS_TOKEN_EXPIRE_MINUTES':settings.ACCESS_TOKEN_EXPIRE_MINUTES}

def get_redis_url():
    return settings.REDIS_URL