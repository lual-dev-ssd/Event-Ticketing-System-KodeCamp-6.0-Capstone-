import uuid
import enum
from typing import List, TYPE_CHECKING, Optional
from sqlalchemy import String, Uuid, Float, ForeignKey, DateTime, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.event import Event

class TicketStatus(str, enum.Enum):
    PENDING = "pending"
    VALID = "valid"
    FAILED = "failed"
    USED = "used"
    CANCELLED = "cancelled"

class Ticket(Base):
    __tablename__ = "tickets"

    id:Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)

    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    event_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("events.id"), nullable=False, index=True)

    purchase_price:Mapped[float] = mapped_column(Float, nullable=False)
    status:Mapped[str] = mapped_column(String, default="pending_payemnt", nullable=False)

    status:Mapped[TicketStatus] = mapped_column(Enum(TicketStatus, native_enum=False), default=TicketStatus.PENDING, nullable=False, index=True)
    payment_ref:Mapped[Optional[str]] = mapped_column(String(100), nullable=True, index=True)
    check_in_at:Mapped[Optional[datetime]]= mapped_column(DateTime(timezone=True), nullable=True, default=None)

    user:Mapped["User"] = relationship("User", back_populates="tickets")
    event:Mapped["Event"] = relationship("Event", back_populates="tickets")