# 📂 IsdaMarket Project Structure

## Complete File Tree

```
IsdaMarket/
│
├── 📄 README.md                    # Main project documentation
├── 📄 SETUP.md                     # Step-by-step setup guide
├── 📄 API_EXAMPLES.md              # Complete API usage examples
├── 📄 PROJECT_STRUCTURE.md         # This file
├── 📄 requirements.txt             # Python dependencies
├── 📄 .env.example                 # Environment variables template
├── 📄 .gitignore                   # Git ignore rules
├── 📄 run.py                       # Quick start script
│
└── 📁 app/                         # Main application package
    │
    ├── 📄 __init__.py
    ├── 📄 main.py                  # FastAPI application entry point
    ├── 📄 config.py                # Application configuration
    ├── 📄 database.py              # Neo4j database connection
    │
    ├── 📁 models/                  # Neo4j node models (neomodel)
    │   ├── 📄 __init__.py
    │   ├── 📄 seller.py            # Seller node model
    │   ├── 📄 buyer.py             # Buyer node model
    │   ├── 📄 fish_product.py      # FishProduct node model
    │   └── 📄 order.py             # Order node model
    │
    ├── 📁 schemas/                 # Pydantic validation schemas
    │   ├── 📄 __init__.py
    │   ├── 📄 seller.py            # Seller request/response schemas
    │   ├── 📄 buyer.py             # Buyer request/response schemas
    │   ├── 📄 fish_product.py      # FishProduct schemas
    │   ├── 📄 order.py             # Order schemas
    │   └── 📄 auth.py              # Authentication schemas (Token, TokenData)
    │
    ├── 📁 controllers/             # Business logic layer
    │   ├── 📄 __init__.py
    │   ├── 📄 seller_controller.py         # Seller CRUD operations
    │   ├── 📄 buyer_controller.py          # Buyer CRUD operations
    │   ├── 📄 fish_product_controller.py   # Product CRUD + filtering
    │   ├── 📄 order_controller.py          # Order management
    │   └── 📄 auth_controller.py           # Authentication logic
    │
    ├── 📁 routes/                  # API endpoint definitions
    │   ├── 📄 __init__.py
    │   ├── 📄 seller_routes.py     # Seller endpoints
    │   ├── 📄 buyer_routes.py      # Buyer endpoints
    │   ├── 📄 fish_product_routes.py   # Product endpoints
    │   ├── 📄 order_routes.py      # Order endpoints
    │   └── 📄 auth_routes.py       # Authentication endpoints
    │
    └── 📁 utils/                   # Utility functions
        ├── 📄 __init__.py
        ├── 📄 security.py          # JWT & password hashing
        └── 📄 dependencies.py      # FastAPI dependencies (auth)
```

## Architecture Overview

### 🏗️ Layer Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    API Routes Layer                      │
│  (HTTP endpoints, request/response handling)             │
│  • seller_routes.py                                      │
│  • buyer_routes.py                                       │
│  • fish_product_routes.py                               │
│  • order_routes.py                                       │
│  • auth_routes.py                                        │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│                 Controllers Layer                        │
│  (Business logic, validation, orchestration)             │
│  • SellerController                                      │
│  • BuyerController                                       │
│  • FishProductController                                 │
│  • OrderController                                       │
│  • AuthController                                        │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│                   Models Layer                           │
│  (Neo4j nodes and relationships via neomodel)            │
│  • Seller                                                │
│  • Buyer                                                 │
│  • FishProduct                                           │
│  • Order                                                 │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│                Neo4j Aura Database                       │
│  (Graph database storing nodes and relationships)        │
└─────────────────────────────────────────────────────────┘
```

### 🔄 Request Flow

```
1. Client Request
   │
   ▼
2. FastAPI Route (routes/)
   │ - Validates JWT token (if protected)
   │ - Validates request schema (Pydantic)
   ▼
3. Controller (controllers/)
   │ - Business logic
   │ - Data transformation
   │ - Error handling
   ▼
4. Model (models/)
   │ - Neo4j operations
   │ - Relationship management
   ▼
5. Neo4j Database
   │ - Store/retrieve data
   ▼
6. Response back through layers
   │
   ▼
7. Client receives JSON response
```

## File Responsibilities

### 📄 `main.py`
- FastAPI application initialization
- Middleware configuration (CORS)
- Router registration
- Startup/shutdown events
- Health check endpoints

### 📄 `config.py`
- Environment variable loading
- Application settings
- Database configuration
- JWT settings

### 📄 `database.py`
- Neo4j connection initialization
- Connection URL composition
- Database lifecycle management

### 📁 `models/`
Each model file defines a Neo4j node with:
- Properties (fields)
- Relationships to other nodes
- Helper methods

**Example relationships:**
- `Seller` ← `SOLD_BY` ← `FishProduct`
- `Buyer` ← `PLACED_BY` ← `Order`
- `Seller` ← `FULFILLED_BY` ← `Order`
- `FishProduct` ← `CONTAINS` ← `Order`

### 📁 `schemas/`
Pydantic models for:
- Request validation (Create, Update)
- Response serialization (Response)
- Authentication (Login, Token)

### 📁 `controllers/`
Business logic including:
- CRUD operations
- Data validation
- Authorization checks
- Error handling
- Model ↔ Schema conversion

### 📁 `routes/`
API endpoints with:
- HTTP method definitions
- Path parameters
- Query parameters
- Request/response models
- Authentication dependencies

### 📁 `utils/`
Utility functions:
- **security.py**: JWT creation/validation, password hashing
- **dependencies.py**: FastAPI dependency injection (get current user)

## Key Design Patterns

### 1. **Separation of Concerns**
- Routes handle HTTP
- Controllers handle business logic
- Models handle data persistence

### 2. **Dependency Injection**
```python
def create_product(
    product_data: FishProductCreate,
    current_seller: Seller = Depends(get_current_seller)
):
    # current_seller automatically injected and validated
```

### 3. **Schema Validation**
```python
class FishProductCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    price: float = Field(..., gt=0)
    # Automatic validation before reaching controller
```

### 4. **Graph Relationships**
```python
# Creating relationships in Neo4j
product.seller.connect(seller)
order.buyer.connect(buyer)
order.fish_product.connect(product)
```

## Database Schema (Neo4j)

### Nodes
- **Seller**: User who sells fish products
- **Buyer**: User who purchases fish products
- **FishProduct**: Fish items for sale
- **Order**: Purchase transaction

### Relationships
```
(Seller)-[:SOLD_BY]-(FishProduct)
(Buyer)-[:PLACED_BY]-(Order)
(Seller)-[:FULFILLED_BY]-(Order)
(FishProduct)-[:CONTAINS]-(Order)
```

### Graph Visualization
```
    ┌─────────┐
    │ Seller  │
    └────┬────┘
         │ SOLD_BY
         │
    ┌────▼────────┐
    │ FishProduct │
    └────┬────────┘
         │ CONTAINS
         │
    ┌────▼────┐
    │  Order  │
    └────┬────┘
         │ PLACED_BY
         │
    ┌────▼────┐
    │  Buyer  │
    └─────────┘
```

## API Endpoint Summary

### Authentication
- `POST /auth/buyer/login`
- `POST /auth/seller/login`

### Sellers (6 endpoints)
- `POST /sellers/` - Register
- `GET /sellers/` - List all
- `GET /sellers/me` - Current seller
- `GET /sellers/{uid}` - Get by ID
- `PATCH /sellers/{uid}` - Update
- `DELETE /sellers/{uid}` - Delete

### Buyers (6 endpoints)
- `POST /buyers/` - Register
- `GET /buyers/` - List all
- `GET /buyers/me` - Current buyer
- `GET /buyers/{uid}` - Get by ID
- `PATCH /buyers/{uid}` - Update
- `DELETE /buyers/{uid}` - Delete

### Products (5 endpoints)
- `POST /products/` - Create (seller only)
- `GET /products/` - List with filters
- `GET /products/{uid}` - Get by ID
- `PATCH /products/{uid}` - Update (owner only)
- `DELETE /products/{uid}` - Delete (owner only)

### Orders (7 endpoints)
- `POST /orders/` - Place order (buyer only)
- `GET /orders/` - List all
- `GET /orders/buyer/me` - Buyer's orders
- `GET /orders/seller/me` - Seller's orders
- `GET /orders/{uid}` - Get by ID
- `PATCH /orders/{uid}` - Update status
- `DELETE /orders/{uid}` - Delete

**Total: 26 API endpoints**

## Technology Stack

| Component | Technology |
|-----------|-----------|
| **Framework** | FastAPI 0.114.2 |
| **Database** | Neo4j Aura (Graph DB) |
| **OGM** | neomodel 5.3.2 |
| **Validation** | Pydantic 2.9.2 |
| **Authentication** | JWT (python-jose) |
| **Password Hashing** | Bcrypt (passlib) |
| **Server** | Uvicorn 0.30.6 |
| **Language** | Python 3.8+ |

## Security Features

✅ **Password Hashing**: Bcrypt with salt  
✅ **JWT Authentication**: Secure token-based auth  
✅ **Role-Based Access**: Separate buyer/seller roles  
✅ **Input Validation**: Pydantic schemas  
✅ **Authorization**: Resource ownership checks  
✅ **CORS**: Configurable cross-origin requests  

## Next Steps for Development

1. **Add Tests**: Unit tests, integration tests
2. **Add Logging**: Structured logging with levels
3. **Add Pagination**: For list endpoints
4. **Add Rate Limiting**: Prevent abuse
5. **Add Caching**: Redis for frequently accessed data
6. **Add Webhooks**: Order status notifications
7. **Add Admin Panel**: Management interface
8. **Add Analytics**: Sales reports, metrics

---

**This structure provides a solid foundation for a production-ready e-commerce API! 🚀**
