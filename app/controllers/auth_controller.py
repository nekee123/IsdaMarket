from fastapi import HTTPException, status
from ..models import Buyer, Seller
from ..schemas import Token, BuyerLogin, SellerLogin
from ..utils.security import verify_password, create_access_token


class AuthController:
    """Controller for authentication operations"""
    
    @staticmethod
    def login_buyer(login_data: BuyerLogin) -> Token:
        """Authenticate buyer and return JWT token"""
        buyer = Buyer.nodes.get_or_none(email=login_data.email)
        
        if not buyer or not verify_password(login_data.password, buyer.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password"
            )
        
        # Create access token
        access_token = create_access_token(
            data={
                "uid": buyer.uid,
                "email": buyer.email,
                "user_type": "buyer"
            }
        )
        
        return Token(access_token=access_token)
    
    @staticmethod
    def login_seller(login_data: SellerLogin) -> Token:
        """Authenticate seller and return JWT token"""
        seller = Seller.nodes.get_or_none(email=login_data.email)
        
        if not seller or not verify_password(login_data.password, seller.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password"
            )
        
        # Create access token
        access_token = create_access_token(
            data={
                "uid": seller.uid,
                "email": seller.email,
                "user_type": "seller"
            }
        )
        
        return Token(access_token=access_token)
