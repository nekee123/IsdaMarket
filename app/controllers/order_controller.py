from typing import List
from fastapi import HTTPException, status
from ..models import Order, FishProduct, Buyer, Seller
from ..utils.dependencies import _retry_get_or_none
from ..schemas import OrderCreate, OrderUpdate, OrderResponse
from ..database import get_db
from datetime import datetime
import uuid


class OrderController:
    """Controller for Order CRUD operations"""
    
    @staticmethod
    def create_order(order_data: OrderCreate) -> OrderResponse:
        # Lookup buyer
        buyer = _retry_get_or_none(Buyer, uid=order_data.buyer_uid)
        if not buyer:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Buyer not found")
        
        # Get product
        product = _retry_get_or_none(FishProduct, uid=order_data.fish_product_uid)
        if not product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
        
        if product.quantity < order_data.quantity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Insufficient quantity. Available: {product.quantity}"
            )
        
        # Get seller
        sellers = product.seller.all()
        if not sellers:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Product has no seller")
        seller = sellers[0]
        
        total_price = product.price * order_data.quantity
        
        # Create order
        order = Order(quantity=order_data.quantity, total_price=total_price, status="pending").save()
        order.buyer.connect(buyer)
        order.seller.connect(seller)
        order.fish_product.connect(product)
        product.reduce_quantity(order_data.quantity)
        
        # Create notification for seller
        OrderController._create_notification(
            recipient_uid=seller.uid,
            recipient_type="seller",
            notif_type="new_order",
            message=f"New order received from {buyer.name} for {product.name}!"
        )
        
        return OrderController._to_response(order)
    
    @staticmethod
    def get_order(order_uid: str) -> OrderResponse:
        order = Order.nodes.get_or_none(uid=order_uid)
        if not order:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
        return OrderController._to_response(order)
    
    @staticmethod
    def get_all_orders() -> List[OrderResponse]:
        orders = Order.nodes.all()
        return [OrderController._to_response(order) for order in orders]
    
    @staticmethod
    def get_buyer_orders(buyer_uid: str) -> List[OrderResponse]:
        buyer = _retry_get_or_none(Buyer, uid=buyer_uid)
        if not buyer:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Buyer not found")
        orders = buyer.orders.all()
        return [OrderController._to_response(order) for order in orders]
    
    @staticmethod
    def get_seller_orders(seller_uid: str) -> List[OrderResponse]:
        seller = _retry_get_or_none(Seller, uid=seller_uid)
        if not seller:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Seller not found")
        orders = seller.orders.all()
        return [OrderController._to_response(order) for order in orders]
    
    @staticmethod
    def update_order_status(order_uid: str, order_data: OrderUpdate) -> OrderResponse:
        order = _retry_get_or_none(Order, uid=order_uid)
        if not order:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
        
        old_status = order.status
        new_status = order_data.status
        order.update_status(new_status)
        
        # Get buyer for notification
        buyers = order.buyer.all()
        products = order.fish_product.all()
        buyer = buyers[0] if buyers else None
        product = products[0] if products else None
        
        # Create notification for buyer based on status change
        if buyer and new_status != old_status:
            if new_status in ["confirmed", "accepted", "processing"]:
                OrderController._create_notification(
                    recipient_uid=buyer.uid,
                    recipient_type="buyer",
                    notif_type="order_approved",
                    message=f"Your order for {product.name if product else 'product'} has been approved!"
                )
            elif new_status == "delivered":
                OrderController._create_notification(
                    recipient_uid=buyer.uid,
                    recipient_type="buyer",
                    notif_type="order_delivered",
                    message=f"Your order for {product.name if product else 'product'} has been delivered!"
                )
            elif new_status == "cancelled":
                OrderController._create_notification(
                    recipient_uid=buyer.uid,
                    recipient_type="buyer",
                    notif_type="order_cancelled",
                    message=f"Your order for {product.name if product else 'product'} has been cancelled."
                )
        
        return OrderController._to_response(order)
    
    @staticmethod
    def delete_order(order_uid: str) -> dict:
        order = _retry_get_or_none(Order, uid=order_uid)
        if not order:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
        
        if order.status == "pending":
            products = order.fish_product.all()
            if products:
                product = products[0]
                product.quantity += order.quantity
                product.update_timestamp()
        
        order.delete()
        return {"message": "Order deleted successfully"}
    
    @staticmethod
    def _create_notification(recipient_uid: str, recipient_type: str, notif_type: str, message: str):
        """Helper method to create a notification"""
        try:
            driver = get_db()
            with driver.session() as session:
                notif_uid = str(uuid.uuid4())
                created_at = datetime.utcnow().isoformat()
                
                query = """
                CREATE (n:Notification {
                    uid: $uid,
                    recipient_uid: $recipient_uid,
                    recipient_type: $recipient_type,
                    type: $type,
                    message: $message,
                    read: false,
                    created_at: $created_at
                })
                """
                
                session.run(query, {
                    "uid": notif_uid,
                    "recipient_uid": recipient_uid,
                    "recipient_type": recipient_type,
                    "type": notif_type,
                    "message": message,
                    "created_at": created_at
                })
        except Exception as e:
            print(f"Error creating notification: {e}")
    
    @staticmethod
    def _to_response(order: Order) -> dict:
        """Convert Order model to response dictionary including buyer and seller contacts"""
         # Get related buyer, seller, and product
        buyers = order.buyer.all()
        sellers = order.seller.all()
        products = order.fish_product.all()
    
        buyer = buyers[0] if buyers else None
        seller = sellers[0] if sellers else None
        product = products[0] if products else None
        
        # Check if order has been reviewed
        reviewed = False
        if order.uid:
            try:
                driver = get_db()
                with driver.session() as session:
                    review_check = session.run(
                        "MATCH (r:Review {order_uid: $order_uid}) RETURN count(r) as count",
                        {"order_uid": order.uid}
                    )
                    result = review_check.single()
                    reviewed = result["count"] > 0 if result else False
            except Exception:
                reviewed = False
    
        return {
        "uid": order.uid,
        "buyer_uid": buyer.uid if buyer else "",
        "buyer_name": buyer.name if buyer else "",
        "buyer_contact": buyer.contact_number if buyer and hasattr(buyer, "contact_number") else "N/A",
        "seller_uid": seller.uid if seller else "",
        "seller_name": seller.name if seller else "",
        "seller_contact": seller.contact_number if seller and hasattr(seller, "contact_number") else "N/A",
        "fish_product_uid": product.uid if product else "",
        "fish_product_name": product.name if product else "",
        "quantity": order.quantity,
        "total_price": order.total_price,
        "status": order.status,
        "reviewed": reviewed,
        "created_at": order.created_at,
        "updated_at": order.updated_at
    }