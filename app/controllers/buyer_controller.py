from typing import List, Optional
from fastapi import HTTPException, status
from neomodel import db
from neo4j import exceptions as neo4j_exceptions
import time
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
        # Return only buyers with valid email formats to avoid neomodel inflate errors
        query = """
        MATCH (b:Buyer)
        WHERE b.email =~ '[^@]+@[^@]+\\.[^@]+'
        RETURN b.uid AS uid, b.name AS name, b.email AS email,
               b.contact_number AS contact_number, b.created_at AS created_at,
               b.updated_at AS updated_at
        ORDER BY b.created_at DESC
        """

        # Retry a few times for transient DB connection issues
        attempts = 3
        backoff = 0.5
        last_exc = None
        for attempt in range(attempts):
            try:
                results, meta = db.cypher_query(query)
                last_exc = None
                break
            except neo4j_exceptions.ServiceUnavailable as e:
                last_exc = e
                time.sleep(backoff * (attempt + 1))
        if last_exc:
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                                detail="Database unavailable, please try again later") from last_exc
        buyers = []
        for row in results:
            buyers.append({
                "uid": row[0],
                "name": row[1],
                "email": row[2],
                "contact_number": row[3],
                "created_at": row[4],
                "updated_at": row[5],
            })

        return buyers
    
    @staticmethod
    def update_buyer(buyer_uid: str, buyer_data: BuyerUpdate) -> BuyerResponse:
        """Update buyer information"""
        # Wrap get_or_none in a small retry loop for transient DB errors
        attempts = 3
        backoff = 0.5
        buyer = None
        last_exc = None
        for attempt in range(attempts):
            try:
                buyer = Buyer.nodes.get_or_none(uid=buyer_uid)
                last_exc = None
                break
            except neo4j_exceptions.ServiceUnavailable as e:
                last_exc = e
                time.sleep(backoff * (attempt + 1))
        if last_exc:
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                                detail="Database unavailable, please try again later") from last_exc
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
        if buyer_data.profile_picture is not None:
            buyer.profile_picture = buyer_data.profile_picture
        
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
            profile_picture=buyer.profile_picture if hasattr(buyer, 'profile_picture') else "",
            created_at=buyer.created_at,
            updated_at=buyer.updated_at
        )
