from fastapi import FastAPI
from app.core.config import settings
from app.core.database import engine
from app.api.v1.api import api_router
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Response

from app.models import Base

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title = settings.PROJECT_NAME,
    description = settings.DESCRIPTION,
    version=settings.VERSION,
    docs_url=settings.DOCS_URL,
    redoc_url=settings.REDOCS_URL
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return Response(status_code=204)

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

app.include_router(api_router, prefix="/api/v1")