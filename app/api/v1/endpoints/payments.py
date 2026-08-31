import uuid
from typing import Any
from fastapi import APIRouter, HTTPException, status, BackgroundTasks, Request
import pybreaker
from json import JSONDecodeError

from app.api.v1.deps import SessionDep
from app.models.event import Event
from app.models.ticket import Ticket, TicketStatus
from app.models.user import User
from app.services.momo import MomoService
from app.utils.ticket_delivery import send_ticket_email_task
from sqlalchemy.orm import joinedload
from app.schemas.payment import MoMoInitiateRequest, MoMoCallbackPayload
from app.api.v1.deps import currentVerfiedUserDep

router = APIRouter()

@router.post("/momo/initiate", status_code=status.HTTP_202_ACCEPTED)
async def initiate_momo_ticket_purchase(
    request:MoMoInitiateRequest,
    db:SessionDep,
    current_user: currentVerfiedUserDep
)-> Any:
    event = db.get(Event, request.event_id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )

    if event.ticket_sold>=event.capacity:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Event is sold out"
        )

    ticket_id = uuid.uuid4()
    ticket = Ticket(
        id=ticket_id,
        user_id=current_user.id,
        event_id=event.id,
        purchase_price=event.ticket_price,
        status=TicketStatus.PENDING,
        payment_ref=str(ticket_id)
    )

    db.add(ticket)
    db.commit()
    db.refresh(ticket)

    ticket.payment_ref = str(ticket.id)
    db.add(ticket)
    db.commit()

    momo = MomoService()

    try:
        await momo.request_to_pay(
            phone_number=request.phone_number,
            amount=float(event.ticket_price),
            reference_id=str(ticket.id)
        )
        return {
            "Message":"Payment prompt sent to mobile device",
            "ticket_id":ticket.id,
            "status":ticket.status
        }

    except pybreaker.CircuitBreakerError:
        db.delete(ticket)
        db.commit()
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE ,
            detail="Payment gateway service temporarily unavailable. Please try again later. "
        )

    except Exception as exc:
        db.delete(ticket)
        db.commit()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Payment request failed: {str(exc)}"
        )


@router.post("/momo/callback", status_code=status.HTTP_200_OK)
async def momo_payment_callback(
    payload:MoMoCallbackPayload,
    db:SessionDep,
    background_tasks:BackgroundTasks
)-> Any:
    
    reference_id = payload.externalId or payload.financialTransactionId
    momo_status = payload.status

    if not reference_id:
        raise HTTPException(status_code=400, detail="Missing reference_id in callback")

    try:
        target_uuid = uuid.UUID(str(reference_id))
    except ValueError:
        target_uuid = None

    ticket = (
        db.query(Ticket)
        .options(joinedload(Ticket.event), joinedload(Ticket.user))
        .filter((Ticket.payment_ref==str(reference_id))|(Ticket.id==target_uuid))
        .first()
    )

    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket record not found")

    if ticket.status == TicketStatus.VALID and momo_status=="SUCCESSFUL":
        return {
            "status":"SUCCESSFUL",
            "message":"Payment already confirmed previously."
        }

    if momo_status == "SUCCESSFUL":
        ticket.status = TicketStatus.VALID

        if ticket.event:
            ticket.event.ticket_sold+=1

        db.commit()
        db.refresh(ticket)

        user = ticket.user or db.get(User, ticket.user_id)
        event_title = ticket.event.title if ticket.event else "Event"

        if user:
            background_tasks.add_task(
                send_ticket_email_task,
                recipient_email=user.email,
                ticket_id=str(ticket.id),
                event_title=event_title
            )

        return {"status": "SUCCESSFUL", "message":"Payment confirmed and PDF ticket sent."}

    else:
        ticket.status=TicketStatus.FAILED
        db.commit()
        return {"status": "FAILED", "message":f"Payment processing failed: {momo_status}"}