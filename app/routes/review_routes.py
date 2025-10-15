from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from ..database import get_db
import uuid

router = APIRouter(prefix="/reviews", tags=["Reviews"])

# Pydantic models
class ReviewCreate(BaseModel):
    buyer_uid: str
    buyer_name: str
    seller_uid: str
    order_uid: str
    rating: int
    comment: Optional[str] = ""

class ReviewResponse(BaseModel):
    uid: str
    buyer_uid: str
    buyer_name: str
    seller_uid: str
    order_uid: str
    rating: int
    comment: str
    created_at: str

# Submit review
@router.post("/", response_model=ReviewResponse)
def submit_review(review: ReviewCreate):
    """Submit a review for a seller"""
    driver = get_db()
    with driver.session() as session:
        # Check if review already exists for this order
        check_query = """
        MATCH (r:Review {order_uid: $order_uid})
        RETURN r.uid AS uid
        """
        existing = session.run(check_query, {"order_uid": review.order_uid})
        if existing.single():
            raise HTTPException(status_code=400, detail="Review already submitted for this order")
        
        review_uid = str(uuid.uuid4())
        created_at = datetime.utcnow().isoformat()
        
        # Create review
        create_query = """
        CREATE (r:Review {
            uid: $uid,
            buyer_uid: $buyer_uid,
            buyer_name: $buyer_name,
            seller_uid: $seller_uid,
            order_uid: $order_uid,
            rating: $rating,
            comment: $comment,
            created_at: $created_at
        })
        RETURN r.uid AS uid, r.buyer_uid AS buyer_uid, r.buyer_name AS buyer_name,
               r.seller_uid AS seller_uid, r.order_uid AS order_uid,
               r.rating AS rating, r.comment AS comment, r.created_at AS created_at
        """
        
        result = session.run(create_query, {
            "uid": review_uid,
            "buyer_uid": review.buyer_uid,
            "buyer_name": review.buyer_name,
            "seller_uid": review.seller_uid,
            "order_uid": review.order_uid,
            "rating": review.rating,
            "comment": review.comment,
            "created_at": created_at
        })
        
        record = result.single()
        
        # Create notification for seller
        notif_uid = str(uuid.uuid4())
        notif_message = f"{review.buyer_name} left a {review.rating}-star review!"
        
        notif_query = """
        CREATE (n:Notification {
            uid: $uid,
            recipient_uid: $seller_uid,
            recipient_type: 'seller',
            type: 'new_review',
            message: $message,
            read: false,
            created_at: $created_at
        })
        """
        
        session.run(notif_query, {
            "uid": notif_uid,
            "seller_uid": review.seller_uid,
            "message": notif_message,
            "created_at": created_at
        })
        
        # Update seller's average rating
        update_rating_query = """
        MATCH (s:Seller {uid: $seller_uid})
        OPTIONAL MATCH (r:Review {seller_uid: $seller_uid})
        WITH s, avg(r.rating) AS avg_rating, count(r) AS review_count
        SET s.average_rating = avg_rating,
            s.review_count = review_count
        """
        session.run(update_rating_query, {"seller_uid": review.seller_uid})
        
        return {
            "uid": record["uid"],
            "buyer_uid": record["buyer_uid"],
            "buyer_name": record["buyer_name"],
            "seller_uid": record["seller_uid"],
            "order_uid": record["order_uid"],
            "rating": record["rating"],
            "comment": record["comment"],
            "created_at": record["created_at"]
        }

# Get reviews for a seller
@router.get("/seller/{seller_uid}", response_model=List[ReviewResponse])
def get_seller_reviews(seller_uid: str):
    """Get all reviews for a seller"""
    driver = get_db()
    with driver.session() as session:
        query = """
        MATCH (r:Review {seller_uid: $seller_uid})
        RETURN r.uid AS uid, r.buyer_uid AS buyer_uid, r.buyer_name AS buyer_name,
               r.seller_uid AS seller_uid, r.order_uid AS order_uid,
               r.rating AS rating, r.comment AS comment, r.created_at AS created_at
        ORDER BY r.created_at DESC
        """
        result = session.run(query, {"seller_uid": seller_uid})
        reviews = []
        for record in result:
            reviews.append({
                "uid": record["uid"],
                "buyer_uid": record["buyer_uid"],
                "buyer_name": record["buyer_name"],
                "seller_uid": record["seller_uid"],
                "order_uid": record["order_uid"],
                "rating": record["rating"],
                "comment": record["comment"],
                "created_at": record["created_at"]
            })
        return reviews

# Get seller rating summary
@router.get("/seller/{seller_uid}/summary")
def get_seller_rating_summary(seller_uid: str):
    """Get rating summary for a seller"""
    driver = get_db()
    with driver.session() as session:
        query = """
        MATCH (s:Seller {uid: $seller_uid})
        OPTIONAL MATCH (r:Review {seller_uid: $seller_uid})
        RETURN s.average_rating AS average_rating, 
               s.review_count AS review_count,
               count(r) AS total_reviews
        """
        result = session.run(query, {"seller_uid": seller_uid})
        record = result.single()
        
        if not record:
            raise HTTPException(status_code=404, detail="Seller not found")
        
        return {
            "seller_uid": seller_uid,
            "average_rating": record["average_rating"] or 0,
            "review_count": record["review_count"] or 0
        }
