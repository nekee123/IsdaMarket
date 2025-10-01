# 📚 IsdaMarket API Examples

Complete examples for all API endpoints with request/response samples.

## Table of Contents
- [Authentication](#authentication)
- [Sellers](#sellers)
- [Buyers](#buyers)
- [Fish Products](#fish-products)
- [Orders](#orders)

---

## Authentication

### Seller Login

**Request:**
```http
POST /auth/seller/login
Content-Type: application/json

{
  "email": "john@fishmarket.com",
  "password": "securepass123"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1aWQiOiJhYmMxMjMiLCJlbWFpbCI6ImpvaG5AZmlzaG1hcmtldC5jb20iLCJ1c2VyX3R5cGUiOiJzZWxsZXIiLCJleHAiOjE3MDk4NTYwMDB9.xyz",
  "token_type": "bearer"
}
```

### Buyer Login

**Request:**
```http
POST /auth/buyer/login
Content-Type: application/json

{
  "email": "jane@example.com",
  "password": "buyerpass123"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

---

## Sellers

### Register New Seller

**Request:**
```http
POST /sellers/
Content-Type: application/json

{
  "name": "Ocean Fresh Fish Market",
  "email": "contact@oceanfresh.com",
  "contact_number": "+1-555-0123",
  "password": "SecurePassword123!"
}
```

**Response:**
```json
{
  "uid": "550e8400-e29b-41d4-a716-446655440000",
  "name": "Ocean Fresh Fish Market",
  "email": "contact@oceanfresh.com",
  "contact_number": "+1-555-0123",
  "created_at": "2025-10-01T08:00:00Z",
  "updated_at": "2025-10-01T08:00:00Z"
}
```

### Get All Sellers

**Request:**
```http
GET /sellers/
```

**Response:**
```json
[
  {
    "uid": "550e8400-e29b-41d4-a716-446655440000",
    "name": "Ocean Fresh Fish Market",
    "email": "contact@oceanfresh.com",
    "contact_number": "+1-555-0123",
    "created_at": "2025-10-01T08:00:00Z",
    "updated_at": "2025-10-01T08:00:00Z"
  },
  {
    "uid": "660e8400-e29b-41d4-a716-446655440001",
    "name": "Coastal Seafood",
    "email": "info@coastal.com",
    "contact_number": "+1-555-0124",
    "created_at": "2025-10-01T09:00:00Z",
    "updated_at": "2025-10-01T09:00:00Z"
  }
]
```

### Get Current Seller Info

**Request:**
```http
GET /sellers/me
Authorization: Bearer YOUR_SELLER_TOKEN
```

**Response:**
```json
{
  "uid": "550e8400-e29b-41d4-a716-446655440000",
  "name": "Ocean Fresh Fish Market",
  "email": "contact@oceanfresh.com",
  "contact_number": "+1-555-0123",
  "created_at": "2025-10-01T08:00:00Z",
  "updated_at": "2025-10-01T08:00:00Z"
}
```

### Update Seller

**Request:**
```http
PATCH /sellers/550e8400-e29b-41d4-a716-446655440000
Authorization: Bearer YOUR_SELLER_TOKEN
Content-Type: application/json

{
  "name": "Ocean Fresh Premium Fish Market",
  "contact_number": "+1-555-9999"
}
```

**Response:**
```json
{
  "uid": "550e8400-e29b-41d4-a716-446655440000",
  "name": "Ocean Fresh Premium Fish Market",
  "email": "contact@oceanfresh.com",
  "contact_number": "+1-555-9999",
  "created_at": "2025-10-01T08:00:00Z",
  "updated_at": "2025-10-01T10:30:00Z"
}
```

---

## Buyers

### Register New Buyer

**Request:**
```http
POST /buyers/
Content-Type: application/json

{
  "name": "Jane Smith",
  "email": "jane.smith@email.com",
  "contact_number": "+1-555-7890",
  "password": "BuyerPass456!"
}
```

**Response:**
```json
{
  "uid": "770e8400-e29b-41d4-a716-446655440002",
  "name": "Jane Smith",
  "email": "jane.smith@email.com",
  "contact_number": "+1-555-7890",
  "created_at": "2025-10-01T11:00:00Z",
  "updated_at": "2025-10-01T11:00:00Z"
}
```

### Get Current Buyer Info

**Request:**
```http
GET /buyers/me
Authorization: Bearer YOUR_BUYER_TOKEN
```

**Response:**
```json
{
  "uid": "770e8400-e29b-41d4-a716-446655440002",
  "name": "Jane Smith",
  "email": "jane.smith@email.com",
  "contact_number": "+1-555-7890",
  "created_at": "2025-10-01T11:00:00Z",
  "updated_at": "2025-10-01T11:00:00Z"
}
```

---

## Fish Products

### Create Fish Product (Seller Only)

**Request:**
```http
POST /products/
Authorization: Bearer YOUR_SELLER_TOKEN
Content-Type: application/json

{
  "name": "Atlantic Salmon",
  "type": "Saltwater",
  "price": 24.99,
  "quantity": 150,
  "description": "Fresh Atlantic salmon, wild-caught, premium quality"
}
```

**Response:**
```json
{
  "uid": "880e8400-e29b-41d4-a716-446655440003",
  "name": "Atlantic Salmon",
  "type": "Saltwater",
  "price": 24.99,
  "quantity": 150,
  "description": "Fresh Atlantic salmon, wild-caught, premium quality",
  "seller_uid": "550e8400-e29b-41d4-a716-446655440000",
  "seller_name": "Ocean Fresh Fish Market",
  "created_at": "2025-10-01T12:00:00Z",
  "updated_at": "2025-10-01T12:00:00Z"
}
```

### Get All Products (with filters)

**Request:**
```http
GET /products/?type=Saltwater&min_price=10&max_price=50
```

**Response:**
```json
[
  {
    "uid": "880e8400-e29b-41d4-a716-446655440003",
    "name": "Atlantic Salmon",
    "type": "Saltwater",
    "price": 24.99,
    "quantity": 150,
    "description": "Fresh Atlantic salmon, wild-caught, premium quality",
    "seller_uid": "550e8400-e29b-41d4-a716-446655440000",
    "seller_name": "Ocean Fresh Fish Market",
    "created_at": "2025-10-01T12:00:00Z",
    "updated_at": "2025-10-01T12:00:00Z"
  },
  {
    "uid": "990e8400-e29b-41d4-a716-446655440004",
    "name": "Pacific Tuna",
    "type": "Saltwater",
    "price": 32.50,
    "quantity": 75,
    "description": "Yellowfin tuna, sushi-grade",
    "seller_uid": "660e8400-e29b-41d4-a716-446655440001",
    "seller_name": "Coastal Seafood",
    "created_at": "2025-10-01T13:00:00Z",
    "updated_at": "2025-10-01T13:00:00Z"
  }
]
```

### Search Products by Name

**Request:**
```http
GET /products/?name=salmon
```

**Response:**
```json
[
  {
    "uid": "880e8400-e29b-41d4-a716-446655440003",
    "name": "Atlantic Salmon",
    "type": "Saltwater",
    "price": 24.99,
    "quantity": 150,
    "description": "Fresh Atlantic salmon, wild-caught, premium quality",
    "seller_uid": "550e8400-e29b-41d4-a716-446655440000",
    "seller_name": "Ocean Fresh Fish Market",
    "created_at": "2025-10-01T12:00:00Z",
    "updated_at": "2025-10-01T12:00:00Z"
  }
]
```

### Update Product (Owner Only)

**Request:**
```http
PATCH /products/880e8400-e29b-41d4-a716-446655440003
Authorization: Bearer YOUR_SELLER_TOKEN
Content-Type: application/json

{
  "price": 22.99,
  "quantity": 200
}
```

**Response:**
```json
{
  "uid": "880e8400-e29b-41d4-a716-446655440003",
  "name": "Atlantic Salmon",
  "type": "Saltwater",
  "price": 22.99,
  "quantity": 200,
  "description": "Fresh Atlantic salmon, wild-caught, premium quality",
  "seller_uid": "550e8400-e29b-41d4-a716-446655440000",
  "seller_name": "Ocean Fresh Fish Market",
  "created_at": "2025-10-01T12:00:00Z",
  "updated_at": "2025-10-01T14:30:00Z"
}
```

---

## Orders

### Place an Order (Buyer Only)

**Request:**
```http
POST /orders/
Authorization: Bearer YOUR_BUYER_TOKEN
Content-Type: application/json

{
  "fish_product_uid": "880e8400-e29b-41d4-a716-446655440003",
  "quantity": 10
}
```

**Response:**
```json
{
  "uid": "aa0e8400-e29b-41d4-a716-446655440005",
  "buyer_uid": "770e8400-e29b-41d4-a716-446655440002",
  "buyer_name": "Jane Smith",
  "seller_uid": "550e8400-e29b-41d4-a716-446655440000",
  "seller_name": "Ocean Fresh Fish Market",
  "fish_product_uid": "880e8400-e29b-41d4-a716-446655440003",
  "fish_product_name": "Atlantic Salmon",
  "quantity": 10,
  "total_price": 229.90,
  "status": "pending",
  "created_at": "2025-10-01T15:00:00Z",
  "updated_at": "2025-10-01T15:00:00Z"
}
```

### Get Buyer's Orders

**Request:**
```http
GET /orders/buyer/me
Authorization: Bearer YOUR_BUYER_TOKEN
```

**Response:**
```json
[
  {
    "uid": "aa0e8400-e29b-41d4-a716-446655440005",
    "buyer_uid": "770e8400-e29b-41d4-a716-446655440002",
    "buyer_name": "Jane Smith",
    "seller_uid": "550e8400-e29b-41d4-a716-446655440000",
    "seller_name": "Ocean Fresh Fish Market",
    "fish_product_uid": "880e8400-e29b-41d4-a716-446655440003",
    "fish_product_name": "Atlantic Salmon",
    "quantity": 10,
    "total_price": 229.90,
    "status": "pending",
    "created_at": "2025-10-01T15:00:00Z",
    "updated_at": "2025-10-01T15:00:00Z"
  }
]
```

### Get Seller's Orders

**Request:**
```http
GET /orders/seller/me
Authorization: Bearer YOUR_SELLER_TOKEN
```

**Response:**
```json
[
  {
    "uid": "aa0e8400-e29b-41d4-a716-446655440005",
    "buyer_uid": "770e8400-e29b-41d4-a716-446655440002",
    "buyer_name": "Jane Smith",
    "seller_uid": "550e8400-e29b-41d4-a716-446655440000",
    "seller_name": "Ocean Fresh Fish Market",
    "fish_product_uid": "880e8400-e29b-41d4-a716-446655440003",
    "fish_product_name": "Atlantic Salmon",
    "quantity": 10,
    "total_price": 229.90,
    "status": "pending",
    "created_at": "2025-10-01T15:00:00Z",
    "updated_at": "2025-10-01T15:00:00Z"
  }
]
```

### Update Order Status

**Request:**
```http
PATCH /orders/aa0e8400-e29b-41d4-a716-446655440005
Content-Type: application/json

{
  "status": "confirmed"
}
```

**Response:**
```json
{
  "uid": "aa0e8400-e29b-41d4-a716-446655440005",
  "buyer_uid": "770e8400-e29b-41d4-a716-446655440002",
  "buyer_name": "Jane Smith",
  "seller_uid": "550e8400-e29b-41d4-a716-446655440000",
  "seller_name": "Ocean Fresh Fish Market",
  "fish_product_uid": "880e8400-e29b-41d4-a716-446655440003",
  "fish_product_name": "Atlantic Salmon",
  "quantity": 10,
  "total_price": 229.90,
  "status": "confirmed",
  "created_at": "2025-10-01T15:00:00Z",
  "updated_at": "2025-10-01T15:30:00Z"
}
```

### Order Status Flow

Available statuses:
- `pending` → Initial state when order is placed
- `confirmed` → Seller confirms the order
- `processing` → Order is being prepared
- `shipped` → Order has been shipped
- `delivered` → Order delivered to buyer
- `cancelled` → Order cancelled

---

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Email already registered"
}
```

### 401 Unauthorized
```json
{
  "detail": "Could not validate credentials"
}
```

### 403 Forbidden
```json
{
  "detail": "Not authorized to update this product"
}
```

### 404 Not Found
```json
{
  "detail": "Product not found"
}
```

### 422 Validation Error
```json
{
  "detail": [
    {
      "loc": ["body", "price"],
      "msg": "ensure this value is greater than 0",
      "type": "value_error.number.not_gt"
    }
  ]
}
```

---

**Pro Tip:** Use the interactive API documentation at `http://localhost:8000/docs` to test all endpoints directly in your browser!
