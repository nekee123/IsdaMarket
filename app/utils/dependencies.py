from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from ..models import Buyer, Seller
from .security import decode_access_token
from neo4j import exceptions as neo4j_exceptions
import time

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
        
        buyer = _retry_get_or_none(Buyer, uid=uid)
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
        
        seller = _retry_get_or_none(Seller, uid=uid)
        if seller is None:
            raise credentials_exception
        
        return seller
    except ValueError:
        raise credentials_exception


def _retry_get_or_none(model_class, **kwargs):
    """Small retry wrapper around model_class.nodes.get_or_none for transient DB errors."""
    attempts = 3
    backoff = 0.5
    last_exc = None
    for attempt in range(attempts):
        try:
            node = model_class.nodes.get_or_none(**kwargs)
            last_exc = None
            return node
        except neo4j_exceptions.ServiceUnavailable as e:
            last_exc = e
            time.sleep(backoff * (attempt + 1))
    # If we got here, raise a HTTPException to be handled by caller context
    raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                        detail="Database unavailable, please try again later") from last_exc
