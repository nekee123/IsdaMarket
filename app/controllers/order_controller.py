from typing import List
from fastapi import HTTPException, status
from ..models import Order, FishProduct, Buyer, Seller
from ..schemas import OrderCreate, OrderUpdate, OrderResponse


class OrderController:
    """Controller for Order CRUD operations"""
    
    @staticmethod
    def create_order(order_data: OrderCreate, buyer: Buyer) -> OrderResponse:
        """Create a new order"""
        # Get the fish product
        product = FishProduct.nodes.get_or_none(uid=order_data.fish_product_uid)
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found"
            )
        
        # Check if product has enough quantity
        if product.quantity < order_data.quantity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Insufficient quantity. Available: {product.quantity}"
            )
        
        # Get the seller
        sellers = product.seller.all()
        if not sellers:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Product has no seller"
            )
        seller = sellers[0]
        
        # Calculate total price
        total_price = product.price * order_data.quantity
        
        # Create order
        order = Order(
            quantity=order_data.quantity,
            total_price=total_price,
            status="pending"
        ).save()
        
        # Create relationships
        order.buyer.connect(buyer)
        order.seller.connect(seller)
        order.fish_product.connect(product)
        
        # Reduce product quantity
        product.reduce_quantity(order_data.quantity)
        
        return OrderController._to_response(order)
    
    @staticmethod
    def get_order(order_uid: str) -> OrderResponse:
        """Get order by UID"""
        order = Order.nodes.get_or_none(uid=order_uid)
        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order not found"
            )
        return OrderController._to_response(order)
    
    @staticmethod
    def get_all_orders() -> List[OrderResponse]:
        """Get all orders"""
        orders = Order.nodes.all()
        return [OrderController._to_response(order) for order in orders]
    
    @staticmethod
    def get_buyer_orders(buyer: Buyer) -> List[OrderResponse]:
        """Get all orders for a specific buyer"""
        orders = buyer.orders.all()
        return [OrderController._to_response(order) for order in orders]
    
    @staticmethod
    def get_seller_orders(seller: Seller) -> List[OrderResponse]:
        """Get all orders for a specific seller"""
        orders = seller.orders.all()
        return [OrderController._to_response(order) for order in orders]
    
    @staticmethod
    def update_order_status(order_uid: str, order_data: OrderUpdate) -> OrderResponse:
        """Update order status"""
        order = Order.nodes.get_or_none(uid=order_uid)
        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order not found"
            )
        
        order.update_status(order_data.status)
        return OrderController._to_response(order)
    
    @staticmethod
    def delete_order(order_uid: str) -> dict:
        """Delete an order"""
        order = Order.nodes.get_or_none(uid=order_uid)
        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order not found"
            )
        
        # If order is pending, restore product quantity
        if order.status == "pending":
            products = order.fish_product.all()
            if products:
                product = products[0]
                product.quantity += order.quantity
                product.update_timestamp()
        
        order.delete()
        return {"message": "Order deleted successfully"}
    
    @staticmethod
    def _to_response(order: Order) -> OrderResponse:
        """Convert Order model to response schema"""
        buyers = order.buyer.all()
        sellers = order.seller.all()
        products = order.fish_product.all()
        
        buyer = buyers[0] if buyers else None
        seller = sellers[0] if sellers else None
        product = products[0] if products else None
        
        return OrderResponse(
            uid=order.uid,
            buyer_uid=buyer.uid if buyer else "",
            buyer_name=buyer.name if buyer else "",
            seller_uid=seller.uid if seller else "",
            seller_name=seller.name if seller else "",
            fish_product_uid=product.uid if product else "",
            fish_product_name=product.name if product else "",
            quantity=order.quantity,
            total_price=order.total_price,
            status=order.status,
            created_at=order.created_at,
            updated_at=order.updated_at
        )
