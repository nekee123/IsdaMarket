from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class FishProductBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    type: str = Field(..., min_length=1, max_length=50)
    price: float = Field(..., gt=0)
    quantity: int = Field(..., ge=0)
    description: Optional[str] = Field(default="", max_length=500)
    image: Optional[str] = None


class FishProductCreate(FishProductBase):
    # The UID of the seller creating this product
    seller_uid: str
    # Optional seller_name from frontend (ignored by backend but accepted)
    seller_name: Optional[str] = None


class FishProductUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    type: Optional[str] = Field(None, min_length=1, max_length=50)
    price: Optional[float] = Field(None, gt=0)
    quantity: Optional[int] = Field(None, ge=0)
    description: Optional[str] = Field(None, max_length=500)
    image: Optional[str] = None


class FishProductResponse(FishProductBase):
    uid: str
    seller_uid: Optional[str] = None
    seller_name: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
