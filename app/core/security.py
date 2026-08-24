from datetime import datetime, timedelta, timezone
from pwdlib import PasswordHash
from jose import jwt, JWTError
from typing import Any
from app.core.config import settings

pwd_context = PasswordHash.recommended()

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hashed(password):
    return pwd_context.hash(password)

def create_access_token(data:dict):
    to_encode =data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})

    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    return encoded_jwt

def create_refresh_token(data: dict[str, Any])->str:
    to_encode = data.copy()
    to_encode.update({"type":"refresh"})

    expire = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp":expire})

    return jwt.encode(to_encode, settings.SECRET_KEY, settings.ALGORITHM)

