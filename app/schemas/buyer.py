from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class BuyerBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    contact_number: str = Field(..., min_length=10, max_length=20)


class BuyerCreate(BuyerBase):
    password: str = Field(..., min_length=6)


class BuyerUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    email: Optional[EmailStr] = None
    contact_number: Optional[str] = Field(None, min_length=10, max_length=20)
    password: Optional[str] = Field(None, min_length=6)


class BuyerResponse(BuyerBase):
    uid: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class BuyerLogin(BaseModel):
    email: EmailStr
    password: str
