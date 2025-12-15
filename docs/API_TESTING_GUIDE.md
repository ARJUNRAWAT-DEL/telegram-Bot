# API Testing Guide

## Overview

This guide helps you test the E-commerce Backend API using curl or Postman.

## Prerequisites

- Backend running on http://localhost:3000
- curl installed (Windows, macOS, Linux)
- Or Postman application

## Test Cases

### 1. Health Check

**Test if server is running:**

```bash
curl http://localhost:3000/api/health
```

**Expected Response:**
```json
{
  "status": "OK",
  "timestamp": "2025-11-29T10:00:00.000Z"
}
```

---

### 2. User Registration

**Register a new user:**

```bash
curl -X POST http://localhost:3000/api/users/register \
  -H "Content-Type: application/json" \
  -d '{
    "telegram_id": "123456789",
    "username": "john_doe",
    "first_name": "John"
  }'
```

**Expected Response:**
```json
{
  "success": true,
  "user": {
    "telegram_id": "123456789",
    "username": "john_doe",
    "first_name": "John",
    "created_at": "2025-11-29T10:00:00Z",
    "cart": [],
    "orders": []
  }
}
```

---

### 3. Get All Products

**Fetch all available products:**

```bash
curl http://localhost:3000/api/products
```

**Expected Response:**
```json
{
  "products": [
    {
      "id": "PROD001",
      "name": "Laptop",
      "price": 999.99,
      "stock": 10
    },
    {
      "id": "PROD002",
      "name": "Smartphone",
      "price": 599.99,
      "stock": 25
    },
    {
      "id": "PROD003",
      "name": "Headphones",
      "price": 149.99,
      "stock": 50
    },
    {
      "id": "PROD004",
      "name": "Tablet",
      "price": 399.99,
      "stock": 15
    },
    {
      "id": "PROD005",
      "name": "Smartwatch",
      "price": 199.99,
      "stock": 30
    }
  ],
  "count": 5
}
```

---

### 4. Get Specific Product

**Fetch details of a specific product:**

```bash
curl http://localhost:3000/api/products/PROD001
```

**Expected Response:**
```json
{
  "id": "PROD001",
  "name": "Laptop",
  "price": 999.99,
  "stock": 10
}
```

---

### 5. Add Item to Cart

**Add product to user's cart:**

```bash
curl -X POST http://localhost:3000/api/cart/add \
  -H "Content-Type: application/json" \
  -d '{
    "telegram_id": "123456789",
    "product_id": "PROD001",
    "quantity": 1
  }'
```

**Expected Response:**
```json
{
  "success": true,
  "cart": [
    {
      "product_id": "PROD001",
      "name": "Laptop",
      "price": 999.99,
      "quantity": 1
    }
  ]
}
```

---

### 6. View Cart

**Get user's shopping cart:**

```bash
curl http://localhost:3000/api/cart/123456789
```

**Expected Response:**
```json
{
  "cart": [
    {
      "product_id": "PROD001",
      "name": "Laptop",
      "price": 999.99,
      "quantity": 1
    }
  ],
  "total": "999.99",
  "item_count": 1
}
```

---

### 7. Add Multiple Items

**Add different products to cart:**

```bash
curl -X POST http://localhost:3000/api/cart/add \
  -H "Content-Type: application/json" \
  -d '{
    "telegram_id": "123456789",
    "product_id": "PROD002",
    "quantity": 2
  }'
```

---

### 8. Remove Item from Cart

**Remove specific product from cart:**

```bash
curl -X POST http://localhost:3000/api/cart/remove \
  -H "Content-Type: application/json" \
  -d '{
    "telegram_id": "123456789",
    "product_id": "PROD001"
  }'
```

**Expected Response:**
```json
{
  "success": true,
  "cart": [
    {
      "product_id": "PROD002",
      "name": "Smartphone",
      "price": 599.99,
      "quantity": 2
    }
  ]
}
```

---

### 9. Create Order

**Place an order from cart:**

```bash
curl -X POST http://localhost:3000/api/orders/create \
  -H "Content-Type: application/json" \
  -d '{
    "telegram_id": "123456789",
    "delivery_address": "123 Main Street, New York, NY 10001",
    "payment_method": "CARD"
  }'
```

**Expected Response:**
```json
{
  "success": true,
  "order": {
    "order_id": "550e8400-e29b-41d4-a716-446655440000",
    "telegram_id": "123456789",
    "user": "john_doe",
    "items": [
      {
        "product_id": "PROD002",
        "name": "Smartphone",
        "price": 599.99,
        "quantity": 2
      }
    ],
    "total": "1199.98",
    "status": "PENDING",
    "delivery_address": "123 Main Street, New York, NY 10001",
    "payment_method": "CARD",
    "created_at": "2025-11-29T10:05:00.000Z",
    "updated_at": "2025-11-29T10:05:00.000Z"
  }
}
```

---

### 10. Get User Orders

**Retrieve all orders for a user:**

```bash
curl http://localhost:3000/api/orders/user/123456789
```

**Expected Response:**
```json
{
  "orders": [
    {
      "order_id": "550e8400-e29b-41d4-a716-446655440000",
      "telegram_id": "123456789",
      "user": "john_doe",
      "items": [...],
      "total": "1199.98",
      "status": "PENDING",
      "delivery_address": "123 Main Street, New York, NY 10001",
      "created_at": "2025-11-29T10:05:00.000Z",
      "updated_at": "2025-11-29T10:05:00.000Z"
    }
  ]
}
```

---

### 11. Get Specific Order

**Retrieve details of a specific order:**

```bash
curl http://localhost:3000/api/orders/550e8400-e29b-41d4-a716-446655440000
```

**Expected Response:**
```json
{
  "order_id": "550e8400-e29b-41d4-a716-446655440000",
  "telegram_id": "123456789",
  "user": "john_doe",
  "items": [...],
  "total": "1199.98",
  "status": "PENDING",
  "delivery_address": "123 Main Street, New York, NY 10001",
  "payment_method": "CARD",
  "created_at": "2025-11-29T10:05:00.000Z",
  "updated_at": "2025-11-29T10:05:00.000Z"
}
```

---

### 12. Update Order Status

**Update order status (admin operation):**

```bash
curl -X PUT http://localhost:3000/api/orders/550e8400-e29b-41d4-a716-446655440000/status \
  -H "Content-Type: application/json" \
  -d '{
    "status": "PROCESSING"
  }'
```

**Valid Statuses:**
- PENDING
- CONFIRMED
- PROCESSING
- SHIPPED
- DELIVERED
- CANCELLED

**Expected Response:**
```json
{
  "success": true,
  "order": {
    "order_id": "550e8400-e29b-41d4-a716-446655440000",
    "status": "PROCESSING",
    "updated_at": "2025-11-29T10:10:00.000Z",
    ...
  }
}
```

---

### 13. Cancel Order

**Cancel an existing order:**

```bash
curl -X POST http://localhost:3000/api/orders/550e8400-e29b-41d4-a716-446655440000/cancel
```

**Expected Response:**
```json
{
  "success": true,
  "order": {
    "order_id": "550e8400-e29b-41d4-a716-446655440000",
    "status": "CANCELLED",
    "updated_at": "2025-11-29T10:15:00.000Z",
    ...
  }
}
```

---

### 14. Clear Cart

**Empty user's shopping cart:**

```bash
curl -X POST http://localhost:3000/api/cart/clear \
  -H "Content-Type: application/json" \
  -d '{
    "telegram_id": "123456789"
  }'
```

**Expected Response:**
```json
{
  "success": true,
  "message": "Cart cleared"
}
```

---

## Using Postman

1. **Import Collection:**
   - Open Postman
   - Create new Collection: "E-commerce API"

2. **Create Requests:**
   - Method: GET/POST/PUT
   - URL: http://localhost:3000/api/...
   - Headers: Content-Type: application/json
   - Body: Raw JSON

3. **Test:**
   - Click "Send"
   - View response in lower pane

---

## Windows PowerShell Alternative

If curl is not available on Windows:

```powershell
# Get Products
Invoke-WebRequest -Uri "http://localhost:3000/api/products" -UseBasicParsing

# Register User
$body = @{
    telegram_id = "123456789"
    username = "john_doe"
    first_name = "John"
} | ConvertTo-Json

Invoke-WebRequest -Uri "http://localhost:3000/api/users/register" `
  -Method POST `
  -Headers @{"Content-Type"="application/json"} `
  -Body $body `
  -UseBasicParsing
```

---

## Complete Testing Workflow

1. **Start Backend**
   ```bash
   npm start  # in backend directory
   ```

2. **Test Health**
   ```bash
   curl http://localhost:3000/api/health
   ```

3. **Register User**
   ```bash
   # Use curl from Test Case 2
   ```

4. **Browse Products**
   ```bash
   # Use curl from Test Case 3
   ```

5. **Add to Cart**
   ```bash
   # Use curl from Test Case 5
   ```

6. **Create Order**
   ```bash
   # Use curl from Test Case 9
   ```

7. **Track Order**
   ```bash
   # Use curl from Test Case 10
   ```

---

## Error Scenarios

### Missing Required Fields
```bash
curl -X POST http://localhost:3000/api/users/register \
  -H "Content-Type: application/json" \
  -d '{"username": "john_doe"}'
```

**Response: 400 Bad Request**
```json
{
  "error": "telegram_id is required"
}
```

### User Not Found
```bash
curl http://localhost:3000/api/users/999999999
```

**Response: 404 Not Found**
```json
{
  "error": "User not found"
}
```

### Insufficient Stock
```bash
curl -X POST http://localhost:3000/api/cart/add \
  -H "Content-Type: application/json" \
  -d '{
    "telegram_id": "123456789",
    "product_id": "PROD001",
    "quantity": 1000
  }'
```

**Response: 400 Bad Request**
```json
{
  "error": "Insufficient stock"
}
```

---

## Performance Tips

- Test health check first
- Create new users for each test session
- Use the same telegram_id within a session
- Monitor server logs for errors
- Use Postman for complex workflows

---

## Debugging

Enable verbose curl output:
```bash
curl -v http://localhost:3000/api/health
```

Check server logs in terminal running Node.js for detailed information.

---

**Good luck with testing!** 🚀
