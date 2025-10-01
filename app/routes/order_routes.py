from fastapi import APIRouter, Depends, status
from typing import List
from ..schemas import OrderCreate, OrderUpdate, OrderResponse
from ..controllers import OrderController
from ..models import Buyer, Seller
from ..utils import get_current_buyer, get_current_seller

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.post("/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def create_order(
    order_data: OrderCreate,
    current_buyer: Buyer = Depends(get_current_buyer)
):
    """
    Place a new order (buyers only)
    """
    return OrderController.create_order(order_data, current_buyer)


@router.get("/", response_model=List[OrderResponse])
def get_all_orders():
    """
    Get all orders (admin view)
    """
    return OrderController.get_all_orders()


@router.get("/buyer/me", response_model=List[OrderResponse])
def get_my_orders_as_buyer(current_buyer: Buyer = Depends(get_current_buyer)):
    """
    Get all orders for current buyer
    """
    return OrderController.get_buyer_orders(current_buyer)


@router.get("/seller/me", response_model=List[OrderResponse])
def get_my_orders_as_seller(current_seller: Seller = Depends(get_current_seller)):
    """
    Get all orders for current seller
    """
    return OrderController.get_seller_orders(current_seller)


@router.get("/{order_uid}", response_model=OrderResponse)
def get_order(order_uid: str):
    """
    Get order by UID
    """
    return OrderController.get_order(order_uid)


@router.patch("/{order_uid}", response_model=OrderResponse)
def update_order_status(order_uid: str, order_data: OrderUpdate):
    """
    Update order status
    
    Available statuses:
    - pending
    - confirmed
    - processing
    - shipped
    - delivered
    - cancelled
    """
    return OrderController.update_order_status(order_uid, order_data)


@router.delete("/{order_uid}", status_code=status.HTTP_200_OK)
def delete_order(order_uid: str):
    """
    Delete an order
    """
    return OrderController.delete_order(order_uid)
