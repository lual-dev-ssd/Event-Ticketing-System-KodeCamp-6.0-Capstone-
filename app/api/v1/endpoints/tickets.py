import uuid
from typing import Any, List
from sqlalchemy import select
from datetime import datetime, timezone
from fastapi import APIRouter, HTTPException, status, BackgroundTasks

from app.api.v1.deps import SessionDep, Current_User_Dep, CurrentAdminDep
from app.models.event import Event
from app.models.ticket import Ticket, TicketStatus
from app.schemas.ticket import TicketCreate, TicketResponse
from app.utils.ticket_delivery import send_ticket_email_task

router = APIRouter()

@router.post("/", response_model=TicketResponse, status_code=status.HTTP_201_CREATED)
def purchase_ticket(ticket_in:TicketCreate, db:SessionDep, current_user:Current_User_Dep, background_tasks:BackgroundTasks)->Any:
    event = db.get(Event, ticket_in.event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    if event.ticket_sold >= event.capacity:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Sorry, this event is sold out"
        )

    new_ticket = Ticket(
        user_id=current_user.id,
        event_id=event.id,
        purchase_price=event.ticket_price,
        status="valid"
    )

    event.ticket_sold +=1

    db.add(new_ticket)
    db.commit()
    db.refresh(new_ticket)

    background_tasks.add_task(
        send_ticket_email_task,
        recipient_email=current_user.email,
        ticket_id=str(new_ticket.id),
        event_title=event.title
    )

    return new_ticket

@router.patch("/{ticket_id}/cancel", response_model=TicketResponse)
def cancel_ticket(ticket_id: uuid.UUID, db:SessionDep, current_user:Current_User_Dep)->Any:
    ticket = db.get(Ticket, ticket_id)
    if not ticket:
        HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found"
        )

    if ticket.user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to cancel this ticket"
        )

    if ticket.status==TicketStatus.CANCELLED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ticket is already cancelled"
        )

    event = db.get(Event, ticket.event_id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Associated event not found"
        )

    ticket.status = TicketStatus.CANCELLED
    if event.ticket_sold>0:
        event.ticket_sold-=1

    db.add(ticket)
    db.add(event)
    db.commit()
    db.refresh(ticket)

    return ticket

@router.patch("/{ticket_id}/check-in", response_model=TicketResponse)
def check_in_ticket(ticket_id:uuid.UUID, db:SessionDep, current_dmin:CurrentAdminDep)->Any:
    ticket = db.get(Ticket, ticket_id)
    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid ticket ID"
        )

    if ticket.status in  [TicketStatus.CANCELLED, TicketStatus.FAILED, TicketStatus.PENDING]:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cannot check in. Ticket status is '{ticket.status}'."
        )

    
    if ticket.status == TicketStatus.USED:
        checked_in_time = (
            ticket.check_in_at.strftime("%Y-%m-%d %H:%M:%S")
            if ticket.check_in_at else "earlier"
        )

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ticket has already been used (Checked in at {checked_in_time})"
        )

    ticket.status = TicketStatus.USED
    ticket.check_in_at = datetime.now(timezone.utc)

    db.add(ticket)
    db.commit()
    db.refresh(ticket)

    return ticket


@router.get("/me", response_model=List[TicketResponse])
def get_my_tickets(db:SessionDep, current_user:Current_User_Dep, skip:int =0, limit:int=100)->Any:
    stmt = select(Ticket).where(Ticket.user_id==current_user.id).offset(skip).limit(limit)
    tickets = db.execute(stmt).scalars().all()
    return tickets

@router.get("/event/{event_id}", response_model=List[TicketResponse])
def get_event_tickets(event_id:uuid.UUID, db:SessionDep, current_admin:CurrentAdminDep)-> Any:
    event = db.get(Event, event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    stmt = select(Ticket).where(Ticket.event_id==event_id)
    tickets = db.execute(stmt).scalars().all()
    return tickets