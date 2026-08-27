import uuid
from jose import jwt, JWTError
from typing import Annotated, Generator
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy import select

from app.core.config import settings
from app.core.database import get_db
from app.models.user import User

SessionDep = Annotated[Session, Depends(get_db)]


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")
TokenDep = Annotated[str, Depends(oauth2_scheme)]

AuthFormDep = Annotated[OAuth2PasswordRequestForm, Depends()]

def get_current_user(token:TokenDep, db:SessionDep)->User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="could not validate credentials",
        headers={"WWW-Authenticate":"Bearer"}
    )

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: str | None = payload.get("sub")
        token_type: str | None = payload.get("type")

        if user_id is None or token_type != "access":
            raise credentials_exception

        user_uuid = uuid.UUID(user_id)

    except (JWTError, ValueError):
        raise credentials_exception

    stmt = select(User).where(User.id==user_uuid)
    user = db.execute(stmt).scalar_one_or_none()

    if user is None:
        raise credentials_exception

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive User"
        )

    return user


Current_User_Dep = Annotated[User, Depends(get_current_user)]

def get_current_active_user(current_user:Current_User_Dep)->User:
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive User Account"
        )
    return current_user

def get_current_verified_user(current_user: User = Depends(get_current_active_user))->User:
    if not current_user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Email address not verified. Please verify your account first"
        )
    return current_user

currentVerfiedUserDep = Annotated[User, Depends(get_current_verified_user)]


def get_current_admin_user(current_user: Current_User_Dep)->User:
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Administrator previleges required",
            headers={"WWW-Authenticate":"Bearer"}
        )

    return current_user

CurrentAdminDep = Annotated[User, Depends(get_current_admin_user)]