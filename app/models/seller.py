from neomodel import (
    StructuredNode,
    StringProperty,
    UniqueIdProperty,
    DateTimeProperty,
    RelationshipFrom,
    EmailProperty
)
from datetime import datetime


class Seller(StructuredNode):
    """Seller node in Neo4j graph database"""
    
    uid = UniqueIdProperty()
    name = StringProperty(required=True, index=True)
    email = EmailProperty(required=True, unique_index=True)
    contact_number = StringProperty(required=True)
    password_hash = StringProperty(required=True)
    
    created_at = DateTimeProperty(default_now=True)
    updated_at = DateTimeProperty(default_now=True)
    
    # Relationships
    fish_products = RelationshipFrom('FishProduct', 'SOLD_BY')
    orders = RelationshipFrom('Order', 'FULFILLED_BY')
    
    def update_timestamp(self):
        """Update the updated_at timestamp"""
        self.updated_at = datetime.utcnow()
        self.save()
