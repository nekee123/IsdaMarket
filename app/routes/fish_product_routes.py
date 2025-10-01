from fastapi import APIRouter, Depends, Query, status
from typing import List, Optional
from ..schemas import FishProductCreate, FishProductUpdate, FishProductResponse
from ..controllers import FishProductController
from ..models import Seller
from ..utils import get_current_seller

router = APIRouter(prefix="/products", tags=["Fish Products"])


@router.post("/", response_model=FishProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(
    product_data: FishProductCreate,
    current_seller: Seller = Depends(get_current_seller)
):
    """
    Create a new fish product (sellers only)
    """
    return FishProductController.create_product(product_data, current_seller)


@router.get("/", response_model=List[FishProductResponse])
def get_all_products(
    name: Optional[str] = Query(None, description="Search by product name"),
    type: Optional[str] = Query(None, description="Filter by fish type"),
    min_price: Optional[float] = Query(None, ge=0, description="Minimum price"),
    max_price: Optional[float] = Query(None, ge=0, description="Maximum price"),
    seller_uid: Optional[str] = Query(None, description="Filter by seller UID")
):
    """
    Get all fish products with optional filters:
    - Search by name
    - Filter by type
    - Filter by price range
    - Filter by seller
    """
    return FishProductController.get_all_products(
        name=name,
        type=type,
        min_price=min_price,
        max_price=max_price,
        seller_uid=seller_uid
    )


@router.get("/{product_uid}", response_model=FishProductResponse)
def get_product(product_uid: str):
    """
    Get fish product by UID
    """
    return FishProductController.get_product(product_uid)


@router.patch("/{product_uid}", response_model=FishProductResponse)
def update_product(
    product_uid: str,
    product_data: FishProductUpdate,
    current_seller: Seller = Depends(get_current_seller)
):
    """
    Update fish product (only by product owner)
    """
    return FishProductController.update_product(product_uid, product_data, current_seller)


@router.delete("/{product_uid}", status_code=status.HTTP_200_OK)
def delete_product(
    product_uid: str,
    current_seller: Seller = Depends(get_current_seller)
):
    """
    Delete fish product (only by product owner)
    """
    return FishProductController.delete_product(product_uid, current_seller)
