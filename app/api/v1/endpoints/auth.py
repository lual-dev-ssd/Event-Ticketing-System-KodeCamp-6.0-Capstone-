from typing import Any
import uuid
<<<<<<< HEAD
from fastapi import APIRouter, status, HTTPException, BackgroundTasks
=======
from fastapi import APIRouter, status, HTTPException
>>>>>>> origin/main
from sqlalchemy import select
from jose import jwt, JWTError
from app.core.config import settings

from app.api.v1.deps import SessionDep, AuthFormDep
<<<<<<< HEAD
from app.core.security import create_access_token, verify_password, get_password_hashed, create_refresh_token, create_email_verification_token, verify_email_token

from app.models.user import User
from app.schemas.user import Token, UserResponse, UserCreate, TokenRefreshRequest
from app.utils.email import send_verification_email_task
=======
from app.core.security import create_access_token, verify_password, get_password_hashed, create_refresh_token

from app.models.user import User
from app.schemas.user import Token, UserResponse, UserCreate, TokenRefreshRequest
>>>>>>> origin/main


router = APIRouter()


<<<<<<< HEAD
@router.post("/register", status_code=status.HTTP_201_CREATED)
def register_user(user_in:UserCreate, db:SessionDep, background:BackgroundTasks)->Any:
=======
@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(user_in:UserCreate, db:SessionDep)->Any:
>>>>>>> origin/main
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
<<<<<<< HEAD
        is_admin=False,
        is_active=True
=======
        is_admin=False
>>>>>>> origin/main
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

<<<<<<< HEAD
    token = create_email_verification_token(new_user.email)
    verify_url = f"{settings.PUBLIC_URL}/api/v1/auth/verify-email?token={token}"


    background.add_task(
        send_verification_email_task,
        recipient_email=new_user.email,
        verify_url=verify_url
    )

    return {"message": "User registered successfully. Please check your email to verify your account."}


@router.get("/verify-email")
def verify_email(token: str, db: SessionDep) -> Any:
    email = verify_email_token(token)
    if not email:
        raise HTTPException(status_code=400, detail="Invalid or expired verification token")

    stmt = select(User).where(User.email==email)
    user = db.execute(stmt).scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user.is_verified:
        return {"message": "Email is already verified"}

    user.is_verified = True
    db.add(user)
    db.commit()

    return {"message": "Email verified successfully. You can now purchase tickets."}
=======
    return new_user
>>>>>>> origin/main

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

<<<<<<< HEAD
    if not user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email address not verified. Please check your inbox to verify your account"
        )

=======
>>>>>>> origin/main
    access_token = create_access_token(data={"sub":str(user.id), "type":"access"})
    refresh_token = create_refresh_token(data={"sub": str(user.id), "type":"refresh"})


    return {"access_token": access_token, "refresh_token": refresh_token, "token_type":"bearer"}

@router.post("/refresh_token", response_model=Token)
def refresh_access_token(body:TokenRefreshRequest, db:SessionDep)-> Any:
    credentials_exceptions = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
<<<<<<< HEAD
        detail="could not validate credentials",
=======
        detail="counld not validate credentials",
>>>>>>> origin/main
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

