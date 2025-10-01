from fastapi import APIRouter, Depends, status
from typing import List
from ..schemas import BuyerCreate, BuyerUpdate, BuyerResponse
from ..controllers import BuyerController
from ..models import Buyer
from ..utils import get_current_buyer

router = APIRouter(prefix="/buyers", tags=["Buyers"])


@router.post("/", response_model=BuyerResponse, status_code=status.HTTP_201_CREATED)
def create_buyer(buyer_data: BuyerCreate):
    """
    Register a new buyer
    """
    return BuyerController.create_buyer(buyer_data)


@router.get("/", response_model=List[BuyerResponse])
def get_all_buyers():
    """
    Get all buyers
    """
    return BuyerController.get_all_buyers()


@router.get("/me", response_model=BuyerResponse)
def get_current_buyer_info(current_buyer: Buyer = Depends(get_current_buyer)):
    """
    Get current authenticated buyer information
    """
    return BuyerController._to_response(current_buyer)


@router.get("/{buyer_uid}", response_model=BuyerResponse)
def get_buyer(buyer_uid: str):
    """
    Get buyer by UID
    """
    return BuyerController.get_buyer(buyer_uid)


@router.patch("/{buyer_uid}", response_model=BuyerResponse)
def update_buyer(
    buyer_uid: str,
    buyer_data: BuyerUpdate,
    current_buyer: Buyer = Depends(get_current_buyer)
):
    """
    Update buyer information (only own profile)
    """
    if current_buyer.uid != buyer_uid:
        from fastapi import HTTPException
        raise HTTPException(status_code=403, detail="Not authorized to update this buyer")
    return BuyerController.update_buyer(buyer_uid, buyer_data)


@router.delete("/{buyer_uid}", status_code=status.HTTP_200_OK)
def delete_buyer(
    buyer_uid: str,
    current_buyer: Buyer = Depends(get_current_buyer)
):
    """
    Delete buyer (only own profile)
    """
    if current_buyer.uid != buyer_uid:
        from fastapi import HTTPException
        raise HTTPException(status_code=403, detail="Not authorized to delete this buyer")
    return BuyerController.delete_buyer(buyer_uid)
