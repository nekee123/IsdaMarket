# ⚡ IsdaMarket Quick Start Guide

Get up and running in **5 minutes**!

## 🎯 Prerequisites Checklist

- [ ] Python 3.8 or higher installed
- [ ] Neo4j Aura account created (free at [neo4j.com/aura](https://neo4j.com/aura))
- [ ] Neo4j credentials saved

## 🚀 Installation (3 Steps)

### Step 1: Install Dependencies
```bash
# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Install packages
pip install -r requirements.txt
```

### Step 2: Configure Environment
```bash
# Copy example file
copy .env.example .env

# Edit .env with your Neo4j credentials
# NEO4J_URI=bolt+s://xxxxx.databases.neo4j.io:7687
# NEO4J_USER=neo4j
# NEO4J_PASSWORD=your-password
# JWT_SECRET_KEY=generate-random-key
```

**Generate JWT Secret:**
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### Step 3: Run the Server
```bash
python run.py
```

✅ **Server running at:** http://localhost:8000  
✅ **API Docs:** http://localhost:8000/docs

---

## 🧪 Test the API (2 Minutes)

### 1️⃣ Register a Seller
```bash
curl -X POST "http://localhost:8000/sellers/" ^
  -H "Content-Type: application/json" ^
  -d "{\"name\":\"Test Market\",\"email\":\"seller@test.com\",\"contact_number\":\"1234567890\",\"password\":\"pass123\"}"
```

### 2️⃣ Login as Seller
```bash
curl -X POST "http://localhost:8000/auth/seller/login" ^
  -H "Content-Type: application/json" ^
  -d "{\"email\":\"seller@test.com\",\"password\":\"pass123\"}"
```

**Copy the `access_token` from response!**

### 3️⃣ Create a Product
```bash
curl -X POST "http://localhost:8000/products/" ^
  -H "Authorization: Bearer YOUR_TOKEN_HERE" ^
  -H "Content-Type: application/json" ^
  -d "{\"name\":\"Fresh Tuna\",\"type\":\"Saltwater\",\"price\":29.99,\"quantity\":50,\"description\":\"Premium tuna\"}"
```

### 4️⃣ View All Products
```bash
curl "http://localhost:8000/products/"
```

---

## 📱 Use Interactive Docs

**Easiest way:** Open http://localhost:8000/docs

1. Click on any endpoint
2. Click "Try it out"
3. Fill in the parameters
4. Click "Execute"
5. See the response!

For protected endpoints:
1. Click 🔒 "Authorize" button at top
2. Enter: `Bearer YOUR_TOKEN`
3. Click "Authorize"
4. Now you can access protected endpoints!

---

## 🎓 Complete Workflow Example

### Scenario: Seller lists fish, Buyer purchases

```bash
# 1. Register Seller
POST /sellers/
{
  "name": "Ocean Fresh Market",
  "email": "ocean@fresh.com",
  "contact_number": "555-0100",
  "password": "seller123"
}

# 2. Seller Login → Get Token
POST /auth/seller/login
{
  "email": "ocean@fresh.com",
  "password": "seller123"
}
# Save access_token as SELLER_TOKEN

# 3. Seller Creates Product
POST /products/
Authorization: Bearer SELLER_TOKEN
{
  "name": "Atlantic Salmon",
  "type": "Saltwater",
  "price": 24.99,
  "quantity": 100,
  "description": "Fresh wild-caught salmon"
}
# Save product uid as PRODUCT_UID

# 4. Register Buyer
POST /buyers/
{
  "name": "John Doe",
  "email": "john@example.com",
  "contact_number": "555-0200",
  "password": "buyer123"
}

# 5. Buyer Login → Get Token
POST /auth/buyer/login
{
  "email": "john@example.com",
  "password": "buyer123"
}
# Save access_token as BUYER_TOKEN

# 6. Buyer Browses Products
GET /products/?type=Saltwater&max_price=30

# 7. Buyer Places Order
POST /orders/
Authorization: Bearer BUYER_TOKEN
{
  "fish_product_uid": "PRODUCT_UID",
  "quantity": 5
}
# Save order uid as ORDER_UID

# 8. Seller Views Orders
GET /orders/seller/me
Authorization: Bearer SELLER_TOKEN

# 9. Update Order Status
PATCH /orders/ORDER_UID
{
  "status": "confirmed"
}

# 10. Buyer Checks Order
GET /orders/buyer/me
Authorization: Bearer BUYER_TOKEN
```

---

## 📚 Documentation Files

| File | Purpose |
|------|---------|
| **README.md** | Complete project overview |
| **SETUP.md** | Detailed setup instructions |
| **API_EXAMPLES.md** | All API endpoints with examples |
| **PROJECT_STRUCTURE.md** | Architecture and file organization |
| **QUICK_START.md** | This file - fastest way to start |

---

## 🔧 Common Commands

```bash
# Start server
python run.py

# Start with custom port
uvicorn app.main:app --port 8001 --reload

# Check if server is running
curl http://localhost:8000/health

# View logs
# (logs appear in terminal where server is running)

# Stop server
# Press Ctrl+C in terminal
```

---

## 🐛 Troubleshooting

### ❌ "Connection refused" to Neo4j
- Check Neo4j Aura instance is running
- Verify credentials in `.env`
- Ensure URI uses `bolt+s://` (not `bolt://`)

### ❌ "Module not found"
```bash
pip install -r requirements.txt
```

### ❌ "Port already in use"
```bash
# Use different port
uvicorn app.main:app --port 8001
```

### ❌ "Invalid token"
- Token expires after 24 hours
- Login again to get new token

---

## 🎯 Next Steps

1. ✅ **Explore API Docs**: http://localhost:8000/docs
2. ✅ **Read API Examples**: Open `API_EXAMPLES.md`
3. ✅ **Understand Structure**: Read `PROJECT_STRUCTURE.md`
4. ✅ **Build Frontend**: Connect your React/Vue/Angular app
5. ✅ **Deploy**: Follow production deployment guide in README

---

## 💡 Pro Tips

1. **Use the interactive docs** at `/docs` - it's the fastest way to test
2. **Save your tokens** - they're valid for 24 hours
3. **Check product quantity** - orders automatically reduce inventory
4. **Use filters** - search products by name, type, price, seller
5. **Monitor orders** - both buyers and sellers can track order status

---

## 🆘 Need Help?

- 📖 **Full Documentation**: See `README.md`
- 🔧 **Setup Issues**: See `SETUP.md`
- 📝 **API Reference**: See `API_EXAMPLES.md`
- 🏗️ **Architecture**: See `PROJECT_STRUCTURE.md`

---

**Happy Coding! 🐟🚀**
