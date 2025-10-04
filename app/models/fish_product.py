from neomodel import (
    StructuredNode,
    StringProperty,
    UniqueIdProperty,
    DateTimeProperty,
    FloatProperty,
    IntegerProperty,
    RelationshipTo,
    RelationshipFrom
)
from datetime import datetime


class FishProduct(StructuredNode):
    """Fish Product node in Neo4j graph database"""
    
    uid = UniqueIdProperty()
    name = StringProperty(required=True, index=True)
    type = StringProperty(required=True, index=True)  # e.g., "Freshwater", "Saltwater", "Shellfish"
    price = FloatProperty(required=True)
    quantity = IntegerProperty(default=0)
    description = StringProperty(default="")
    image = StringProperty(default="")  # Base64 encoded image
    
    created_at = DateTimeProperty(default_now=True)
    updated_at = DateTimeProperty(default_now=True)
    
    # Relationships
    seller = RelationshipTo('app.models.seller.Seller', 'SOLD_BY')
    orders = RelationshipFrom('app.models.order.Order', 'CONTAINS')
    
    def update_timestamp(self):
        """Update the updated_at timestamp"""
        self.updated_at = datetime.utcnow()
        self.save()
    
    def reduce_quantity(self, amount: int):
        """Reduce product quantity"""
        if self.quantity >= amount:
            self.quantity -= amount
            self.update_timestamp()
            return True
        return False
