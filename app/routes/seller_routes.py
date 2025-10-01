from fastapi import APIRouter, status
from typing import List
from ..schemas import SellerCreate, SellerUpdate, SellerResponse
from ..controllers import SellerController

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




@router.get("/{seller_uid}", response_model=SellerResponse)
def get_seller(seller_uid: str):
    """
    Get seller by UID
    """
    return SellerController.get_seller(seller_uid)


@router.patch("/{seller_uid}", response_model=SellerResponse)
def update_seller(seller_uid: str, seller_data: SellerUpdate):
    """
    Update seller information
    """
    return SellerController.update_seller(seller_uid, seller_data)


@router.delete("/{seller_uid}", status_code=status.HTTP_200_OK)
def delete_seller(seller_uid: str):
    """
    Delete seller
    """
    return SellerController.delete_seller(seller_uid)
