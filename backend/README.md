# E-Commerce Backend API Configuration
# This file contains instructions for setting up the backend

## Quick Start Guide

### Prerequisites
- Node.js 14 or higher
- npm (comes with Node.js)

### Installation Steps

1. Navigate to backend directory:
   ```bash
   cd backend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the server:
   ```bash
   npm start
   ```

   The server will start on `http://localhost:3000`

### Available Endpoints

#### Health Check
- GET /api/health - Check if server is running

#### Users
- POST /api/users/register - Register new user
- GET /api/users/:telegram_id - Get user profile

#### Products
- GET /api/products - Get all products
- GET /api/products/:product_id - Get specific product

#### Cart
- POST /api/cart/add - Add item to cart
- GET /api/cart/:telegram_id - View cart
- POST /api/cart/remove - Remove item from cart
- POST /api/cart/clear - Clear entire cart

#### Orders
- POST /api/orders/create - Create new order
- GET /api/orders/user/:telegram_id - Get user's orders
- GET /api/orders/:order_id - Get specific order
- PUT /api/orders/:order_id/status - Update order status
- POST /api/orders/:order_id/cancel - Cancel order

### Sample Products

The backend comes pre-loaded with 5 sample products:
1. Laptop - $999.99 (10 in stock)
2. Smartphone - $599.99 (25 in stock)
3. Headphones - $149.99 (50 in stock)
4. Tablet - $399.99 (15 in stock)
5. Smartwatch - $199.99 (30 in stock)

### Testing the API

You can test endpoints using curl or Postman:

```bash
# Test health
curl http://localhost:3000/api/health

# Get all products
curl http://localhost:3000/api/products

# Register user
curl -X POST http://localhost:3000/api/users/register \
  -H "Content-Type: application/json" \
  -d '{"telegram_id":"123","username":"testuser","first_name":"Test"}'
```

### Environment Variables

For production, consider using environment variables:
- PORT: Server port (default: 3000)
- NODE_ENV: development/production

### Troubleshooting

**Port 3000 already in use:**
```bash
# Windows: Find process using port 3000
netstat -ano | findstr :3000

# Kill process (replace PID with actual process ID)
taskkill /PID <PID> /F
```

**Connection refused errors:**
- Make sure backend is running
- Check that port 3000 is accessible
- Verify firewall settings

### Notes
- Data is stored in-memory (resets on server restart)
- For production, use a real database
- Add authentication and validation
- Implement HTTPS for security
