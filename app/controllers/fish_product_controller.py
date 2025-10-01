from typing import List, Optional
from fastapi import HTTPException, status
from ..models import FishProduct, Seller
from ..schemas import FishProductCreate, FishProductUpdate, FishProductResponse


class FishProductController:
    """Controller for Fish Product CRUD operations"""
    
    @staticmethod
    def create_product(product_data: FishProductCreate, seller: Seller) -> FishProductResponse:
        """Create a new fish product"""
        # Create new product
        product = FishProduct(
            name=product_data.name,
            type=product_data.type,
            price=product_data.price,
            quantity=product_data.quantity,
            description=product_data.description
        ).save()
        
        # Link to seller
        product.seller.connect(seller)
        
        return FishProductController._to_response(product)
    
    @staticmethod
    def get_product(product_uid: str) -> FishProductResponse:
        """Get product by UID"""
        product = FishProduct.nodes.get_or_none(uid=product_uid)
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found"
            )
        return FishProductController._to_response(product)
    
    @staticmethod
    def get_all_products(
        name: Optional[str] = None,
        type: Optional[str] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        seller_uid: Optional[str] = None
    ) -> List[FishProductResponse]:
        """Get all products with optional filters"""
        products = FishProduct.nodes.all()
        
        # Apply filters
        filtered_products = []
        for product in products:
            # Name filter (case-insensitive partial match)
            if name and name.lower() not in product.name.lower():
                continue
            
            # Type filter (case-insensitive partial match)
            if type and type.lower() not in product.type.lower():
                continue
            
            # Price range filter
            if min_price is not None and product.price < min_price:
                continue
            if max_price is not None and product.price > max_price:
                continue
            
            # Seller filter
            if seller_uid:
                sellers = product.seller.all()
                if not sellers or sellers[0].uid != seller_uid:
                    continue
            
            filtered_products.append(product)
        
        return [FishProductController._to_response(p) for p in filtered_products]
    
    @staticmethod
    def update_product(product_uid: str, product_data: FishProductUpdate, seller: Seller) -> FishProductResponse:
        """Update product information"""
        product = FishProduct.nodes.get_or_none(uid=product_uid)
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found"
            )
        
        # Verify seller owns this product
        sellers = product.seller.all()
        if not sellers or sellers[0].uid != seller.uid:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to update this product"
            )
        
        # Update fields if provided
        if product_data.name is not None:
            product.name = product_data.name
        if product_data.type is not None:
            product.type = product_data.type
        if product_data.price is not None:
            product.price = product_data.price
        if product_data.quantity is not None:
            product.quantity = product_data.quantity
        if product_data.description is not None:
            product.description = product_data.description
        
        product.update_timestamp()
        return FishProductController._to_response(product)
    
    @staticmethod
    def delete_product(product_uid: str, seller: Seller) -> dict:
        """Delete a product"""
        product = FishProduct.nodes.get_or_none(uid=product_uid)
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found"
            )
        
        # Verify seller owns this product
        sellers = product.seller.all()
        if not sellers or sellers[0].uid != seller.uid:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to delete this product"
            )
        
        product.delete()
        return {"message": "Product deleted successfully"}
    
    @staticmethod
    def _to_response(product: FishProduct) -> FishProductResponse:
        """Convert FishProduct model to response schema"""
        sellers = product.seller.all()
        seller_uid = sellers[0].uid if sellers else None
        seller_name = sellers[0].name if sellers else None
        
        return FishProductResponse(
            uid=product.uid,
            name=product.name,
            type=product.type,
            price=product.price,
            quantity=product.quantity,
            description=product.description,
            seller_uid=seller_uid,
            seller_name=seller_name,
            created_at=product.created_at,
            updated_at=product.updated_at
        )
