from .seller_routes import router as seller_router
from .buyer_routes import router as buyer_router
from .fish_product_routes import router as fish_product_router
from .order_routes import router as order_router
from .notification_routes import router as notification_router
from .message_routes import router as message_router
from .review_routes import router as review_router

__all__ = [
    "seller_router",
    "buyer_router",
    "fish_product_router",
    "order_router",
    "notification_router",
    "message_router",
    "review_router"
]
