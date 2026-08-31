from fastapi import FastAPI
from app.core.config import settings
from app.core.database import engine
from app.api.v1.api import api_router
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Response
import socket


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
@app.get("/")
async def root():
    return {
        "status":"online",
        "message":f"welcome to {settings.PROJECT_NAME}",
        "docs":settings.DOCS_URL or "/docs"
    }

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return Response(status_code=204)

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/")
def read_root():
    return {
        "status": "online",
        "message": "Event Ticketing & MoMo Payment API",
        "docs": "/docs",
    }

orig_getaddrinfo = socket.getaddrinfo

def getaddrinfo_ipv4(*args, **kwargs):
    response = orig_getaddrinfo(*args, **kwargs)
    return [res for res in response if res[0]==socket.AF_INET]

socket.getaddrinfo = getaddrinfo_ipv4

app.include_router(api_router, prefix="/api/v1")