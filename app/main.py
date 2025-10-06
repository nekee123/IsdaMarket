from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from dotenv import load_dotenv
from neo4j import GraphDatabase
import os
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

# ✅ Neo4j Aura Connection
NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USER = os.getenv("NEO4J_USER")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")
driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

@app.on_event("startup")
async def startup_event():
    """Initialize database connection on startup"""
    init_database()
    print(f"🚀 {settings.app_name} v{settings.app_version} started successfully!")

@app.on_event("shutdown")
async def shutdown_event():
    """Close database connection on shutdown"""
    close_database()
    driver.close()
    print("👋 Application shutdown complete")

# Redirect root to Swagger docs
@app.get("/", include_in_schema=False)
async def redirect_to_docs():
    """Redirect root URL to Swagger docs"""
    return RedirectResponse(url="/docs")

# ✅ SEARCH ROUTE
@app.get("/search")
def search_items(query: str = Query(...), search_type: str = Query("products")):
    """
    Search for products, sellers, or buyers by name.
    """
    with driver.session() as session:
        if search_type == "products":
            cypher = """
            MATCH (p:Product)
            WHERE toLower(p.name) CONTAINS toLower($query)
            RETURN p { .name, .price, .location } AS item
            """
        elif search_type == "sellers":
            cypher = """
            MATCH (s:Seller)
            WHERE toLower(s.name) CONTAINS toLower($query)
            RETURN s { .name, .location } AS item
            """
        else:
            cypher = """
            MATCH (b:Buyer)
            WHERE toLower(b.name) CONTAINS toLower($query)
            RETURN b { .name, .location } AS item
            """

        results = session.run(cypher, {"query": query})
        items = [record["item"] for record in results]
        return items

# Include routers
app.include_router(seller_router)
app.include_router(buyer_router)
app.include_router(fish_product_router)
app.include_router(order_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
