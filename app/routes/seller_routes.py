from fastapi import APIRouter, Depends, status
from typing import List
from ..schemas import SellerCreate, SellerUpdate, SellerResponse
from ..controllers import SellerController
from ..models import Seller
from ..utils import get_current_seller

router = APIRouter(prefix="/sellers", tags=["Sellers"])


@router.post("/", response_model=SellerResponse, status_code=status.HTTP_201_CREATED)
def create_seller(seller_data: SellerCreate):
    """
    Register a new seller
    """
    return SellerController.create_seller(seller_data)


@router.get("/", response_model=List[SellerResponse])
def get_all_sellers():
    """
    Get all sellers
    """
    return SellerController.get_all_sellers()


@router.get("/me", response_model=SellerResponse)
def get_current_seller_info(current_seller: Seller = Depends(get_current_seller)):
    """
    Get current authenticated seller information
    """
    return SellerController._to_response(current_seller)


@router.get("/{seller_uid}", response_model=SellerResponse)
def get_seller(seller_uid: str):
    """
    Get seller by UID
    """
    return SellerController.get_seller(seller_uid)


@router.patch("/{seller_uid}", response_model=SellerResponse)
def update_seller(
    seller_uid: str,
    seller_data: SellerUpdate,
    current_seller: Seller = Depends(get_current_seller)
):
    """
    Update seller information (only own profile)
    """
    if current_seller.uid != seller_uid:
        from fastapi import HTTPException
        raise HTTPException(status_code=403, detail="Not authorized to update this seller")
    return SellerController.update_seller(seller_uid, seller_data)


@router.delete("/{seller_uid}", status_code=status.HTTP_200_OK)
def delete_seller(
    seller_uid: str,
    current_seller: Seller = Depends(get_current_seller)
):
    """
    Delete seller (only own profile)
    """
    if current_seller.uid != seller_uid:
        from fastapi import HTTPException
        raise HTTPException(status_code=403, detail="Not authorized to delete this seller")
    return SellerController.delete_seller(seller_uid)
