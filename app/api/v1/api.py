from fastapi import APIRouter
from app.api.v1.endpoints import auth, events, tickets

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(events.router, prefix="/events", tags=["Events"])
api_router.include_router(tickets.router, prefix="/tickets", tags=["Tickets"])