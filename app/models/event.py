import uuid
from typing import List, TYPE_CHECKING
from datetime import datetime
from sqlalchemy import String, Uuid, DateTime, Float, Integer, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.ticket import Ticket


class Event(Base):
    __tablename__ = "events"

    id:Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    title:Mapped[str] = mapped_column(String, index=True, nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    date:Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    location:Mapped[str] = mapped_column(String, nullable=False)
    ticket_price:Mapped[float] = mapped_column(Float, nullable=False)
    capacity: Mapped[int] = mapped_column(Integer, nullable=False)

    ticket_sold:Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    organizer_id:Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    organizer:Mapped["User"]=relationship("User", back_populates="events")
    tickets:Mapped[List["Ticket"]] = relationship("Ticket", back_populates="event")

    