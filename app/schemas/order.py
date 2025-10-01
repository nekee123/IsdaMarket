from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class OrderCreate(BaseModel):
    fish_product_uid: str
    quantity: int = Field(..., gt=0)


class OrderUpdate(BaseModel):
    status: str = Field(..., pattern="^(pending|confirmed|processing|shipped|delivered|cancelled)$")


class OrderResponse(BaseModel):
    uid: str
    buyer_uid: str
    buyer_name: str
    seller_uid: str
    seller_name: str
    fish_product_uid: str
    fish_product_name: str
    quantity: int
    total_price: float
    status: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
