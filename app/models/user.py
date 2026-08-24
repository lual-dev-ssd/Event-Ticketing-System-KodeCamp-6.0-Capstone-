import uuid
from typing import List, TYPE_CHECKING
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import String, Uuid, Boolean
from app.models.base import Base

if TYPE_CHECKING:
    from app.models.event import Event
    from app.models.ticket import Ticket


class User(Base):
    __tablename__ = "users"

    id:Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    email:Mapped[str] = mapped_column(String, index=True, nullable=False, unique=True)
    name:Mapped[str] = mapped_column(String, nullable=False)
    hashed_password:Mapped[str] = mapped_column(String, nullable=False)

    is_verified:Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_admin:Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_active:Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    events:Mapped[list["Event"]] = relationship("Event", back_populates="organizer")
    tickets:Mapped[List["Ticket"]]=relationship("Ticket", back_populates="user")