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

    MOMO_SUBSCRIPTION_KEY:str ="sub_key"
    MOMO_API_USER:str ="your_momo_api_user_uuid"
    MOMO_API_KEY:str = "your_momo_api_key"
    MOMO_ENVIRONMENT:str ="sandbox"
    MOMO_BASE_URL:str = "https://sandbox.momodevelopment.mtn.com"

    PUBLIC_URL:str = "https://abc123.ngrok-free.dev"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()