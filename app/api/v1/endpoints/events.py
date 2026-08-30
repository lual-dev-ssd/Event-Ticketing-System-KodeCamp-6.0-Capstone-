import uuid
from typing import Any, List, Optional
from sqlalchemy import select
from datetime import datetime
from fastapi import APIRouter, HTTPException, status, Query
from sqlalchemy.orm import selectinload

from app.api.v1.deps import SessionDep, CurrentAdminDep
from app.models.event import Event
from app.models.ticket import Ticket
from app.schemas.event import EventCreate, EventResponse, EventUpdate
from app.schemas.ticket import AttendeeResponse

router = APIRouter()

@router.post("/", response_model=EventResponse, status_code=status.HTTP_201_CREATED)
def create_event(event_in:EventCreate, db:SessionDep, current_admin:CurrentAdminDep)->Any:
    event_data = event_in.model_dump()

    event_data["organizer_id"]=current_admin.id

    new_event = Event(**event_data)
    db.add(new_event)
    db.commit()
    db.refresh(new_event)

    return new_event

@router.patch("/{event_id}", response_model=EventResponse)
def update_event(event_id: uuid.UUID, event_in: EventUpdate, db:SessionDep, current_admin:CurrentAdminDep)->Any:
    event = db.get(Event, event_id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Evnt not found"
        )
    if event_in.capacity is not None and event_in.capacity < event.ticket_sold:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot reduce capacity below already sold tickets ({event.ticket_sold})"
        )

    update_data = event_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(event, field, value)

    db.add(event)
    db.commit()
    db.refresh(event)

    return event

@router.delete("/{event_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_event(event_id:uuid.UUID, db:SessionDep, current_admin:CurrentAdminDep)->None:
    event = db.get(Event, event_id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )

    if event.ticket_sold >0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete an event that has active ticket sales. Cancel tickets first"
        )
    db.delete(event)
    db.commit()

@router.get("/{event_id}/attendees", response_model=List[AttendeeResponse])
def list_event_attendees(event_id: uuid.UUID, db:SessionDep, current_admin:CurrentAdminDep, skip:int=0, limit: int=100)->Any:
    event = db.get(Event, event_id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )

    stmt = (
        select(Ticket)
        .options(selectinload(Ticket.user))
        .where(Ticket.event_id==event_id)
        .offset(skip)
        .limit(limit)
    )

    tickets = db.execute(stmt).scalars().all()

    return [
        {
            "id":t.id,
            "ticket_status":t.status,
            "purchase_price":t.purchase_price,
            "checked_in_at":t.check_in_at,
            "user":t.user
        }
        for t in tickets
    ]


@router.get("/", response_model=List[EventResponse])
def list_events(
    db:SessionDep,
    category: Optional[str]=Query(None, description="Filter by event category"),
    start_date: Optional[datetime]=Query(None, description="Filter events starting on or after this date"),
    end_date: Optional[datetime]=Query(None, description="Filter events starting on or before this date"),
    skip: int=0,
    limit:int=100
)-> Any:
    
    stmt = select(Event)

    if category:
        stmt = stmt.where(Event.category.ilike(f"%{category}%"))

    if start_date:
        stmt = stmt.where(Event.start_time >= start_date)

    if end_date:
        stmt = stmt.where(Event.start_time <= end_date)

    stmt = stmt.offset(skip).limit(limit)

    return db.execute(stmt).scalars()
  

@router.get("/{event_id}", response_model=EventResponse)
def get_event(event_id: uuid.UUID, db:SessionDep)->Any:
    event = db.get(Event, event_id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="event not found"
        )
    return event