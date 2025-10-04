from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse  # 👈 add this line
from dotenv import load_dotenv
from .database import init_database, close_database
from .routes import (
    seller_router,
    buyer_router,
    fish_product_router,
    order_router
)
from .config import settings

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="IsdaMarket",
    version="1.0.0",
    description="A Fish Marketplace",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    """Initialize database connection on startup"""
    init_database()
    print(f"🚀 {settings.app_name} v{settings.app_version} started successfully!")

@app.on_event("shutdown")
async def shutdown_event():
    """Close database connection on shutdown"""
    close_database()
    print("👋 Application shutdown complete")

# 👇 ADD THIS NEW ROUTE
@app.get("/", include_in_schema=False)
async def redirect_to_docs():
    """Redirect root URL to Swagger docs"""
    return RedirectResponse(url="/docs")

# Include routers
app.include_router(seller_router)
app.include_router(buyer_router)
app.include_router(fish_product_router)
app.include_router(order_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
