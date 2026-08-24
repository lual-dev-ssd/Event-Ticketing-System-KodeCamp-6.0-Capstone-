import uuid
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field

class EventBase(BaseModel):
    title:str
    description: Optional[str]=None
    date:datetime
    location:str
    ticket_price:float
    capacity: int

class EventCreate(EventBase):
    pass

class EventResponse(EventBase):
    id: uuid.UUID
    organizer_id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class EventUpdate(BaseModel):
    title:Optional[str] = None
    description: Optional[str] = None
    location:Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    capacity: Optional[int] = Field(default=None, ge=1)
    ticket_price: Optional[int] = Field(default=None, ge=0.0)

