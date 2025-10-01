from fastapi import APIRouter, status
from typing import List
from ..schemas import BuyerCreate, BuyerUpdate, BuyerResponse
from ..controllers import BuyerController

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




@router.get("/{buyer_uid}", response_model=BuyerResponse)
def get_buyer(buyer_uid: str):
    """
    Get buyer by UID
    """
    return BuyerController.get_buyer(buyer_uid)


@router.patch("/{buyer_uid}", response_model=BuyerResponse)
def update_buyer(buyer_uid: str, buyer_data: BuyerUpdate):
    """
    Update buyer information
    """
    return BuyerController.update_buyer(buyer_uid, buyer_data)


@router.delete("/{buyer_uid}", status_code=status.HTTP_200_OK)
def delete_buyer(buyer_uid: str):
    """
    Delete buyer
    """
    return BuyerController.delete_buyer(buyer_uid)
