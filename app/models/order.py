from neomodel import (
    StructuredNode,
    StringProperty,
    UniqueIdProperty,
    DateTimeProperty,
    FloatProperty,
    IntegerProperty,
    RelationshipTo
)
from datetime import datetime


class Order(StructuredNode):
    """Order node in Neo4j graph database"""
    
    uid = UniqueIdProperty()
    quantity = IntegerProperty(default=1)
    total_price = FloatProperty(required=True)
    status = StringProperty(
        default="pending",
        choices={
            "pending": "Pending",
            "confirmed": "Confirmed",
            "processing": "Processing",
            "shipped": "Shipped",
            "delivered": "Delivered",
            "cancelled": "Cancelled"
        }
    )
    
    created_at = DateTimeProperty(default_now=True)
    updated_at = DateTimeProperty(default_now=True)
    
    # Relationships
    buyer = RelationshipTo('Buyer', 'PLACED_BY')
    seller = RelationshipTo('Seller', 'FULFILLED_BY')
    fish_product = RelationshipTo('FishProduct', 'CONTAINS')
    
    def update_timestamp(self):
        """Update the updated_at timestamp"""
        self.updated_at = datetime.utcnow()
        self.save()
    
    def update_status(self, new_status: str):
        """Update order status"""
        self.status = new_status
        self.update_timestamp()
