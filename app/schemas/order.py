from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class OrderCreate(BaseModel):
    buyer_uid: str
    fish_product_uid: str
    quantity: int = Field(..., gt=0)
    # Optional fields from frontend (ignored by backend but accepted)
    buyer_name: Optional[str] = None
    seller_uid: Optional[str] = None
    seller_name: Optional[str] = None
    fish_product_name: Optional[str] = None
    total_price: Optional[float] = None


class OrderUpdate(BaseModel):
    status: str = Field(..., pattern="^(pending|confirmed|processing|shipped|delivered|cancelled)$")


class OrderResponse(BaseModel):
    uid: str
    buyer_uid: str
    buyer_name: str
    buyer_contact: str  # add this
    seller_uid: str
    seller_name: str
    seller_contact: str  # add this
    fish_product_uid: str
    fish_product_name: str
    quantity: int
    total_price: float
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
