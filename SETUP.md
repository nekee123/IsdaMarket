# 🚀 IsdaMarket Setup Guide

## Step-by-Step Setup Instructions

### 1. Neo4j Aura Setup

1. Go to [https://neo4j.com/cloud/aura/](https://neo4j.com/cloud/aura/)
2. Sign up for a free account
3. Create a new database instance (Free tier is sufficient)
4. **IMPORTANT**: Save your credentials when shown (you won't see them again!)
   - Connection URI (e.g., `bolt+s://xxxxx.databases.neo4j.io:7687`)
   - Username (usually `neo4j`)
   - Password (auto-generated, save this!)

### 2. Environment Configuration

1. Copy the example environment file:
   ```bash
   copy .env.example .env
   ```

2. Edit `.env` file with your Neo4j credentials:
   ```env
   NEO4J_URI=bolt+s://your-instance-id.databases.neo4j.io:7687
   NEO4J_USER=neo4j
   NEO4J_PASSWORD=your-actual-password
   JWT_SECRET_KEY=generate-a-random-secret-key
   ```

3. Generate a secure JWT secret key:
   ```bash
   # Using Python
   python -c "import secrets; print(secrets.token_hex(32))"
   
   # Or using OpenSSL
   openssl rand -hex 32
   ```

### 3. Python Environment Setup

1. **Create virtual environment:**
   ```bash
   python -m venv venv
   ```

2. **Activate virtual environment:**
   
   **Windows:**
   ```bash
   venv\Scripts\activate
   ```
   
   **Linux/Mac:**
   ```bash
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

### 4. Run the Application

**Option 1: Using the run script**
```bash
python run.py
```

**Option 2: Using uvicorn directly**
```bash
uvicorn app.main:app --reload
```

**Option 3: Using the main module**
```bash
python -m app.main
```

### 5. Verify Installation

1. Open your browser and go to: `http://localhost:8000`
2. You should see a welcome message
3. Access API documentation: `http://localhost:8000/docs`

### 6. Test the API

#### Register a Seller
```bash
curl -X POST "http://localhost:8000/sellers/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Fish Market",
    "email": "seller@test.com",
    "contact_number": "1234567890",
    "password": "password123"
  }'
```

#### Login as Seller
```bash
curl -X POST "http://localhost:8000/auth/seller/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "seller@test.com",
    "password": "password123"
  }'
```

Save the `access_token` from the response!

#### Create a Product (use your token)
```bash
curl -X POST "http://localhost:8000/products/" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Fresh Tuna",
    "type": "Saltwater",
    "price": 29.99,
    "quantity": 50,
    "description": "Premium yellowfin tuna"
  }'
```

## Troubleshooting

### Connection Error to Neo4j
- Verify your Neo4j Aura instance is running
- Check that credentials in `.env` are correct
- Ensure the URI includes `bolt+s://` (not just `bolt://`)

### Module Not Found Errors
- Ensure virtual environment is activated
- Run `pip install -r requirements.txt` again

### Port Already in Use
- Change the port in `run.py` or use: `uvicorn app.main:app --port 8001`

### JWT Token Errors
- Ensure `JWT_SECRET_KEY` is set in `.env`
- Token expires after 24 hours by default (configurable)

## Next Steps

1. ✅ Register sellers and buyers
2. ✅ Create fish products
3. ✅ Place orders
4. ✅ Explore the API documentation at `/docs`
5. ✅ Build your frontend application!

## Production Deployment

For production deployment:
1. Set a strong `JWT_SECRET_KEY`
2. Use a production Neo4j instance
3. Configure CORS for your frontend domain
4. Use a production ASGI server (Gunicorn)
5. Enable HTTPS
6. Set up proper logging and monitoring

---

**Need help?** Check the main README.md or open an issue!
