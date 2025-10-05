from typing import List
from fastapi import HTTPException, status
from ..models import Order, FishProduct, Buyer, Seller
from ..utils.dependencies import _retry_get_or_none
from ..schemas import OrderCreate, OrderUpdate, OrderResponse


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
        
        order.update_status(order_data.status)
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
    def _to_response(order: Order) -> dict:
        """Convert Order model to response dictionary including buyer and seller contacts"""
         # Get related buyer, seller, and product
        buyers = order.buyer.all()
        sellers = order.seller.all()
        products = order.fish_product.all()
    
        buyer = buyers[0] if buyers else None
        seller = sellers[0] if sellers else None
        product = products[0] if products else None
    
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
        "created_at": order.created_at,
        "updated_at": order.updated_at
    }