from typing import List, Optional
from fastapi import HTTPException, status
from ..models import Buyer
from ..schemas import BuyerCreate, BuyerUpdate, BuyerResponse
from ..utils.security import get_password_hash


class BuyerController:
    """Controller for Buyer CRUD operations"""
    
    @staticmethod
    def create_buyer(buyer_data: BuyerCreate) -> BuyerResponse:
        """Create a new buyer"""
        # Check if email already exists
        existing_buyer = Buyer.nodes.get_or_none(email=buyer_data.email)
        if existing_buyer:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Create new buyer
        buyer = Buyer(
            name=buyer_data.name,
            email=buyer_data.email,
            contact_number=buyer_data.contact_number,
            password_hash=get_password_hash(buyer_data.password)
        ).save()
        
        return BuyerController._to_response(buyer)
    
    @staticmethod
    def get_buyer(buyer_uid: str) -> BuyerResponse:
        """Get buyer by UID"""
        buyer = Buyer.nodes.get_or_none(uid=buyer_uid)
        if not buyer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Buyer not found"
            )
        return BuyerController._to_response(buyer)
    
    @staticmethod
    def get_all_buyers() -> List[BuyerResponse]:
        """Get all buyers"""
        buyers = Buyer.nodes.all()
        return [BuyerController._to_response(buyer) for buyer in buyers]
    
    @staticmethod
    def update_buyer(buyer_uid: str, buyer_data: BuyerUpdate) -> BuyerResponse:
        """Update buyer information"""
        buyer = Buyer.nodes.get_or_none(uid=buyer_uid)
        if not buyer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Buyer not found"
            )
        
        # Update fields if provided
        if buyer_data.name is not None:
            buyer.name = buyer_data.name
        if buyer_data.email is not None:
            # Check if new email already exists
            existing = Buyer.nodes.get_or_none(email=buyer_data.email)
            if existing and existing.uid != buyer_uid:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already in use"
                )
            buyer.email = buyer_data.email
        if buyer_data.contact_number is not None:
            buyer.contact_number = buyer_data.contact_number
        if buyer_data.password is not None:
            buyer.password_hash = get_password_hash(buyer_data.password)
        
        buyer.update_timestamp()
        return BuyerController._to_response(buyer)
    
    @staticmethod
    def delete_buyer(buyer_uid: str) -> dict:
        """Delete a buyer"""
        buyer = Buyer.nodes.get_or_none(uid=buyer_uid)
        if not buyer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Buyer not found"
            )
        
        buyer.delete()
        return {"message": "Buyer deleted successfully"}
    
    @staticmethod
    def _to_response(buyer: Buyer) -> BuyerResponse:
        """Convert Buyer model to response schema"""
        return BuyerResponse(
            uid=buyer.uid,
            name=buyer.name,
            email=buyer.email,
            contact_number=buyer.contact_number,
            created_at=buyer.created_at,
            updated_at=buyer.updated_at
        )
