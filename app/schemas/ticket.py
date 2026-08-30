import uuid
from datetime import datetime
from pydantic import BaseModel, ConfigDict
from typing import Optional
from app.schemas.user import UserResponse

class TicketCreate(BaseModel):
    event_id: uuid.UUID

class TicketResponse(BaseModel):
    id:uuid.UUID
    event_id:uuid.UUID
    user_id:uuid.UUID
    purchase_price:float
    status:str
    created_at:datetime
    updated_at:datetime

    model_config = ConfigDict(from_attributes=True)

class AttendeeResponse(BaseModel):
    id:uuid.UUID
    ticket_status:str
    purchase_price:float
    checked_in_at: Optional[datetime] = None
    user: UserResponse

    model_config = ConfigDict(from_attributes=True)