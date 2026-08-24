from typing import Any
from fastapi import APIRouter, status, HTTPException
from sqlalchemy import select

from app.api.v1.deps import SessionDep, Current_User_Dep

from app.models.user import User
from app.schemas.user import UserResponse, UserUpdate

router = APIRouter()

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user:Current_User_Dep)->Any:
    return current_user


@router.patch("/me", response_model=UserResponse)
def update_my_profile(user_in: UserUpdate, db:SessionDep, current_user:Current_User_Dep)->Any:
    if user_in.email and user_in.email != current_user.email:
        existing = db.execute(
            select(User).where(User.email==user_in.email)
        ).scalar_one_or_none()

        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email address is already in use"
            )
        current_user.email = user_in.email

    if user_in.full_name is not None:
        current_user.full_name=user_in.full_name

    db.add(current_user),
    db.commit()
    db.refresh(current_user)
    
    return current_user