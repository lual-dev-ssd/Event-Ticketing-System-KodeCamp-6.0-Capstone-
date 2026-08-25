from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str="FastAPI Event Ticketing"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "A modular FastAPI-based event ticketing system"
    DOCS_URL: str = "/docs"
    REDOCS_URL: str = "/redoc"

    DATABASE_URL: str = "postgresql+psycopg2://user:password@host/database_name"

    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: str = "daveben.ajak@gmail.com"
    SMTP_PASSWORD: str = ""
    SMTP_TLS: bool = True
    EMAILS_FROM_EMAIL: str = "daveben.ajak@gmail.com"
    EMAILS_FROM_NAME: str = "Event Ticketing System"

    SECRET_KEY:str = "Key here"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()