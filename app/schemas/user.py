from datetime import datetime
from pydantic import BaseModel, EmailStr, ConfigDict
import uuid


class UserBase(BaseModel):
    email:EmailStr
    name:str

class UserCreate(UserBase):
    password:str

class UserResponse(UserBase):
    id:uuid.UUID
    is_verified:bool
    is_admin:bool
    is_active:bool
    created_at:datetime
    updated_at:datetime

    model_config=ConfigDict(from_attributes=True)

class Token(BaseModel):
    access_token:str
    refresh_token:str
    token_type:str

class TokenRefreshRequest(BaseModel):
    refresh_token:str
