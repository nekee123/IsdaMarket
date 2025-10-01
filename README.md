# 🐟 IsdaMarket - Fish E-Commerce API

A comprehensive, production-ready e-commerce backend API for a fish marketplace built with **FastAPI** and **Neo4j Aura** graph database.

## 🌟 Features

- **Complete CRUD Operations** for Sellers, Buyers, Fish Products, and Orders
- **JWT Authentication** for secure buyer and seller access
- **Graph Database** relationships using Neo4j Aura
- **Advanced Search & Filtering** for products (by name, type, price range, seller)
- **Order Management** with status tracking
- **Inventory Management** with automatic quantity updates
- **RESTful API** with comprehensive documentation
- **Production-Ready** modular architecture

## 📁 Project Structure

```
IsdaMarket/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application entry point
│   ├── config.py               # Configuration and settings
│   ├── database.py             # Neo4j database connection
│   │
│   ├── models/                 # Neo4j node models
│   │   ├── __init__.py
│   │   ├── seller.py
│   │   ├── buyer.py
│   │   ├── fish_product.py
│   │   └── order.py
│   │
│   ├── schemas/                # Pydantic validation schemas
│   │   ├── __init__.py
│   │   ├── seller.py
│   │   ├── buyer.py
│   │   ├── fish_product.py
│   │   ├── order.py
│   │   └── auth.py
│   │
│   ├── controllers/            # Business logic layer
│   │   ├── __init__.py
│   │   ├── seller_controller.py
│   │   ├── buyer_controller.py
│   │   ├── fish_product_controller.py
│   │   ├── order_controller.py
│   │   └── auth_controller.py
│   │
│   ├── routes/                 # API endpoints
│   │   ├── __init__.py
│   │   ├── seller_routes.py
│   │   ├── buyer_routes.py
│   │   ├── fish_product_routes.py
│   │   ├── order_routes.py
│   │   └── auth_routes.py
│   │
│   └── utils/                  # Utility functions
│       ├── __init__.py
│       ├── security.py         # JWT & password hashing
│       └── dependencies.py     # FastAPI dependencies
│
├── .env.example                # Environment variables template
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Neo4j Aura account (free tier available at [neo4j.com/aura](https://neo4j.com/aura))

### Installation

1. **Clone the repository**
   ```bash
   cd IsdaMarket
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   # Copy the example file
   copy .env.example .env
   
   # Edit .env with your Neo4j Aura credentials
   ```

5. **Run the application**
   ```bash
   uvicorn app.main:app --reload
   ```

   The API will be available at `http://localhost:8000`

## 📚 API Documentation

Once the server is running, access the interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔐 Authentication

### Register & Login Flow

1. **Register as Seller**
   ```http
   POST /sellers/
   Content-Type: application/json

   {
     "name": "John's Fish Market",
     "email": "john@fishmarket.com",
     "contact_number": "+1234567890",
     "password": "securepassword"
   }
   ```

2. **Register as Buyer**
   ```http
   POST /buyers/
   Content-Type: application/json

   {
     "name": "Jane Doe",
     "email": "jane@example.com",
     "contact_number": "+1234567890",
     "password": "securepassword"
   }
   ```

3. **Login**
   ```http
   POST /auth/seller/login
   Content-Type: application/json

   {
     "email": "john@fishmarket.com",
     "password": "securepassword"
   }
   ```

   Response:
   ```json
   {
     "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
     "token_type": "bearer"
   }
   ```

4. **Use Token in Requests**
   ```http
   GET /sellers/me
   Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
   ```

## 📖 API Endpoints

### Authentication
- `POST /auth/buyer/login` - Buyer login
- `POST /auth/seller/login` - Seller login

### Sellers
- `POST /sellers/` - Register new seller
- `GET /sellers/` - Get all sellers
- `GET /sellers/me` - Get current seller (authenticated)
- `GET /sellers/{uid}` - Get seller by UID
- `PATCH /sellers/{uid}` - Update seller (authenticated)
- `DELETE /sellers/{uid}` - Delete seller (authenticated)

### Buyers
- `POST /buyers/` - Register new buyer
- `GET /buyers/` - Get all buyers
- `GET /buyers/me` - Get current buyer (authenticated)
- `GET /buyers/{uid}` - Get buyer by UID
- `PATCH /buyers/{uid}` - Update buyer (authenticated)
- `DELETE /buyers/{uid}` - Delete buyer (authenticated)

### Fish Products
- `POST /products/` - Create product (seller only)
- `GET /products/` - Get all products with filters
  - Query params: `name`, `type`, `min_price`, `max_price`, `seller_uid`
- `GET /products/{uid}` - Get product by UID
- `PATCH /products/{uid}` - Update product (owner only)
- `DELETE /products/{uid}` - Delete product (owner only)

### Orders
- `POST /orders/` - Place order (buyer only)
- `GET /orders/` - Get all orders
- `GET /orders/buyer/me` - Get buyer's orders (authenticated)
- `GET /orders/seller/me` - Get seller's orders (authenticated)
- `GET /orders/{uid}` - Get order by UID
- `PATCH /orders/{uid}` - Update order status
- `DELETE /orders/{uid}` - Delete order

## 🎯 Usage Examples

### Create a Fish Product (as Seller)

```bash
curl -X POST "http://localhost:8000/products/" \
  -H "Authorization: Bearer YOUR_SELLER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Fresh Salmon",
    "type": "Saltwater",
    "price": 25.99,
    "quantity": 100,
    "description": "Premium Atlantic Salmon, fresh daily"
  }'
```

### Search Products

```bash
# Search by name
curl "http://localhost:8000/products/?name=salmon"

# Filter by type and price range
curl "http://localhost:8000/products/?type=saltwater&min_price=10&max_price=50"

# Filter by seller
curl "http://localhost:8000/products/?seller_uid=abc123"
```

### Place an Order (as Buyer)

```bash
curl -X POST "http://localhost:8000/orders/" \
  -H "Authorization: Bearer YOUR_BUYER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "fish_product_uid": "product-uid-here",
    "quantity": 5
  }'
```

### Update Order Status

```bash
curl -X PATCH "http://localhost:8000/orders/order-uid-here" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "shipped"
  }'
```

## 🗄️ Database Schema

### Nodes
- **Seller**: id, name, email, contact_number, password_hash
- **Buyer**: id, name, email, contact_number, password_hash
- **FishProduct**: id, name, type, price, quantity, description
- **Order**: id, quantity, total_price, status

### Relationships
- `(FishProduct)-[:SOLD_BY]->(Seller)`
- `(Order)-[:PLACED_BY]->(Buyer)`
- `(Order)-[:FULFILLED_BY]->(Seller)`
- `(Order)-[:CONTAINS]->(FishProduct)`

## 🔒 Security Features

- **Password Hashing**: Bcrypt algorithm
- **JWT Tokens**: Secure authentication with expiration
- **Role-Based Access**: Separate buyer and seller authentication
- **Input Validation**: Pydantic schemas for all requests
- **Authorization Checks**: Users can only modify their own resources

## 🛠️ Development

### Running in Development Mode

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Environment Variables

Create a `.env` file with:

```env
NEO4J_URI=bolt+s://your-instance.databases.neo4j.io:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=your-password
JWT_SECRET_KEY=your-secret-key
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440
```

## 📦 Dependencies

- **FastAPI**: Modern web framework
- **Uvicorn**: ASGI server
- **Neomodel**: Neo4j OGM (Object-Graph Mapping)
- **Pydantic**: Data validation
- **python-jose**: JWT implementation
- **passlib**: Password hashing
- **python-dotenv**: Environment management

## 🚢 Production Deployment

1. Set strong `JWT_SECRET_KEY` (use `openssl rand -hex 32`)
2. Configure CORS for specific origins
3. Use environment-specific `.env` files
4. Enable HTTPS
5. Set up proper logging
6. Configure Neo4j Aura production instance
7. Use a production ASGI server (e.g., Gunicorn with Uvicorn workers)

```bash
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker
```

## 📝 License

This project is open source and available for educational and commercial use.

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

## 📧 Support

For support, email your-email@example.com or open an issue in the repository.

---

**Built with ❤️ using FastAPI and Neo4j**
