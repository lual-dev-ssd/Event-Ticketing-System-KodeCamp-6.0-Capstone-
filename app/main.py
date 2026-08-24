from fastapi import FastAPI
from app.core.config import settings
from app.core.database import engine
from app.api.v1.api import api_router

from app.models import Base

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title = settings.PROJECT_NAME,
    description = settings.DESCRIPTION,
    version=settings.VERSION,
    docs_url=settings.DOCS_URL,
    redoc_url=settings.REDOCS_URL
)

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

app.include_router(api_router, prefix="/api/v1")