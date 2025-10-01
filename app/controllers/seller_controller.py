from typing import List, Optional
from fastapi import HTTPException, status
from ..models import Seller
from ..schemas import SellerCreate, SellerUpdate, SellerResponse
from ..utils.security import get_password_hash


class SellerController:
    """Controller for Seller CRUD operations"""
    
    @staticmethod
    def create_seller(seller_data: SellerCreate) -> SellerResponse:
        """Create a new seller"""
        # Check if email already exists
        existing_seller = Seller.nodes.get_or_none(email=seller_data.email)
        if existing_seller:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Create new seller
        seller = Seller(
            name=seller_data.name,
            email=seller_data.email,
            contact_number=seller_data.contact_number,
            password_hash=get_password_hash(seller_data.password)
        ).save()
        
        return SellerController._to_response(seller)
    
    @staticmethod
    def get_seller(seller_uid: str) -> SellerResponse:
        """Get seller by UID"""
        seller = Seller.nodes.get_or_none(uid=seller_uid)
        if not seller:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Seller not found"
            )
        return SellerController._to_response(seller)
    
    @staticmethod
    def get_all_sellers() -> List[SellerResponse]:
        """Get all sellers"""
        sellers = Seller.nodes.all()
        return [SellerController._to_response(seller) for seller in sellers]
    
    @staticmethod
    def update_seller(seller_uid: str, seller_data: SellerUpdate) -> SellerResponse:
        """Update seller information"""
        seller = Seller.nodes.get_or_none(uid=seller_uid)
        if not seller:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Seller not found"
            )
        
        # Update fields if provided
        if seller_data.name is not None:
            seller.name = seller_data.name
        if seller_data.email is not None:
            # Check if new email already exists
            existing = Seller.nodes.get_or_none(email=seller_data.email)
            if existing and existing.uid != seller_uid:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already in use"
                )
            seller.email = seller_data.email
        if seller_data.contact_number is not None:
            seller.contact_number = seller_data.contact_number
        if seller_data.password is not None:
            seller.password_hash = get_password_hash(seller_data.password)
        
        seller.update_timestamp()
        return SellerController._to_response(seller)
    
    @staticmethod
    def delete_seller(seller_uid: str) -> dict:
        """Delete a seller"""
        seller = Seller.nodes.get_or_none(uid=seller_uid)
        if not seller:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Seller not found"
            )
        
        seller.delete()
        return {"message": "Seller deleted successfully"}
    
    @staticmethod
    def _to_response(seller: Seller) -> SellerResponse:
        """Convert Seller model to response schema"""
        return SellerResponse(
            uid=seller.uid,
            name=seller.name,
            email=seller.email,
            contact_number=seller.contact_number,
            created_at=seller.created_at,
            updated_at=seller.updated_at
        )
