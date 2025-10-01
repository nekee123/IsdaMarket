from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from ..models import Buyer, Seller
from .security import decode_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_buyer(token: str = Depends(oauth2_scheme)) -> Buyer:
    """Get current authenticated buyer"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = decode_access_token(token)
        uid: str = payload.get("uid")
        user_type: str = payload.get("user_type")
        
        if uid is None or user_type != "buyer":
            raise credentials_exception
        
        buyer = Buyer.nodes.get_or_none(uid=uid)
        if buyer is None:
            raise credentials_exception
        
        return buyer
    except ValueError:
        raise credentials_exception


def get_current_seller(token: str = Depends(oauth2_scheme)) -> Seller:
    """Get current authenticated seller"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = decode_access_token(token)
        uid: str = payload.get("uid")
        user_type: str = payload.get("user_type")
        
        if uid is None or user_type != "seller":
            raise credentials_exception
        
        seller = Seller.nodes.get_or_none(uid=uid)
        if seller is None:
            raise credentials_exception
        
        return seller
    except ValueError:
        raise credentials_exception
