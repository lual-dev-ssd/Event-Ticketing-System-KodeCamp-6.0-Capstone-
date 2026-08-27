import uuid
from typing import Any
from fastapi import APIRouter, HTTPException, status, BackgroundTasks
import pybreaker

from app.api.v1.deps import SessionDep
from app.models.event import Event
from app.models.ticket import Ticket
from app.services.momo import MomoService
from app.services.ticket_delivery import send_ticket_email_task
from sqlalchemy.orm import joinedload
from app.schemas.payment import MoMoCallbackPayload
from app.api.v1.deps import currentVerfiedUserDep

router = APIRouter()

@router.post("/momo/initiate", status_code=status.HTTP_202_ACCEPTED)
def initiate_momo_ticket_purchase(
    event_id:uuid.UUID,
    phone_number:str,
    db:SessionDep,
    current_user:currentVerfiedUserDep
)-> Any:
    event = db.get(Event, event_id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Event not found"
        )

    if event.ticket_sold>=event.capacity:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Event is sold out"
        )
    ticket = Ticket(
        user_id=current_user.id,
        event_id=event.id,
        purchase_price=event.ticket_price,
        status="pending_payment"
    )

    db.add(ticket)
    db.commit()
    db.refresh(ticket)

    momo = MomoService()

    try:
        momo.request_to_pay(
            phone_number=phone_number,
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
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE if hasattr(status, "HTTP_503_SERVICE_UNAVAILABLE") else 503,
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
def momo_payment_callback(
    payload:MoMoCallbackPayload,
    db:SessionDep,
    background_tasks:BackgroundTasks
)-> Any:
    ticket_id_str = payload.externalId
    momo_status = payload.status

    if not ticket_id_str:
        raise HTTPException(status_code=400, detail="Missing external in callback")

    ticket = db.query(Ticket).options(joinedload(Ticket.user)).filter(Ticket.id==uuid.UUID(ticket_id_str)).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket record not found")

    if momo_status=="SUCCESSFUL":
        ticket.status = "valid"

        event = db.get(Event, ticket.event_id)
        if event:
            event.ticket_sold+=1
            db.add(event)

        user_email = ticket.user.email if ticket.user else None
        event_title = event.title if event else "Event Ticket"

        db.add(ticket)
        db.commit()

        if user_email:
            background_tasks.add_task(
                send_ticket_email_task,
                recipient_email=user_email,
                ticket_id=str(ticket.id),
                event_title=event_title
            )

        return {"status": "SUCCESSFULL", "message":"Payment confirmed and PDF ticket sent."}

    else:
        ticket.status="failed"
        db.add(ticket)
        db.commit()

        return {"status": "FAILED", "message":"Payment processing failed."}