from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str="FastAPI Event Ticketing"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "A modular FastAPI-based event ticketing system"
    DOCS_URL: str = "/docs"
    REDOCS_URL: str = "/redoc"

    DATABASE_URL: str = "postgresql+psycopg2://user:password@host/database_name"


    SECRET_KEY:str = "689794011b3717ea6923a3c2ab376f4711817c71fc5fa45228d43c009994aade"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()