from fastapi import APIRouter, status
from ..schemas import Token, BuyerLogin, SellerLogin
from ..controllers import AuthController

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/buyer/login", response_model=Token, status_code=status.HTTP_200_OK)
def login_buyer(login_data: BuyerLogin):
    """
    Login as a buyer and receive JWT access token
    """
    return AuthController.login_buyer(login_data)


@router.post("/seller/login", response_model=Token, status_code=status.HTTP_200_OK)
def login_seller(login_data: SellerLogin):
    """
    Login as a seller and receive JWT access token
    """
    return AuthController.login_seller(login_data)
