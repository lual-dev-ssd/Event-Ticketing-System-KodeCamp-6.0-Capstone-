from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Session
from app.core.config import settings
from typing import Annotated
from fastapi import Depends

engine = create_engine(
    settings.DATABASE_URL
)

SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()

sessionDep = Annotated[Session, Depends(get_db)]