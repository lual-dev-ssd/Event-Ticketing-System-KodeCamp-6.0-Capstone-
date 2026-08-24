from typing import Any
import uuid
from fastapi import APIRouter, status, HTTPException
from sqlalchemy import select
from jose import jwt, JWTError
from app.core.config import settings

from app.api.v1.deps import SessionDep, AuthFormDep
from app.core.security import create_access_token, verify_password, get_password_hashed, create_refresh_token

from app.models.user import User
from app.schemas.user import Token, UserResponse, UserCreate, TokenRefreshRequest


router = APIRouter()


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(user_in:UserCreate, db:SessionDep)->Any:
    stmt = select(User).where(User.email==user_in.email)
    existing_user = db.execute(stmt).scalar_one_or_none()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already Registered"
        )

    new_user = User(
        email = user_in.email,
        name = user_in.name,
        hashed_password = get_password_hashed(user_in.password),
        is_verified=False,
        is_admin=False
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.post("/token", response_model=Token)
def login_for_access_token(form_data:AuthFormDep, db:SessionDep)-> Any:
    stmt = select(User).where(User.email==form_data.username)
    user = db.execute(stmt).scalar_one_or_none()

    if not user or not verify_password(
        form_data.password, user.hashed_password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect Password or Email",
            headers={"WWW-Authenticate":"Bearer"}
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive User"
        )

    access_token = create_access_token(data={"sub":str(user.id), "type":"access"})
    refresh_token = create_refresh_token(data={"sub": str(user.id), "type":"refresh"})


    return {"access_token": access_token, "refresh_token": refresh_token, "token_type":"bearer"}

@router.post("/refresh_token", response_model=Token)
def refresh_access_token(body:TokenRefreshRequest, db:SessionDep)-> Any:
    credentials_exceptions = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="counld not validate credentials",
        headers={"WWW-Authenticate":"Bearer"}
    )

    try:
        payload = jwt.decode(body.refresh_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id:str | None = payload.get("sub")
        token_type:str | None = payload.get("type")

        if user_id is None or token_type != "refresh":
            raise credentials_exceptions

    except JWTError:
        raise credentials_exceptions

    stmt = select(User).where(User.id==uuid.UUID(user_id))
    user = db.execute(stmt).scalar_one_or_none()

    if not user or not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive User")

    access_token = create_access_token(data={"sub":str(user.id), "type":"access"})
    refresh_token = create_refresh_token(data={"sub": str(user.id), "type":"refresh"})

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

