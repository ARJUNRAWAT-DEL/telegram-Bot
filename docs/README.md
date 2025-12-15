# RPA Lab #3 - Telegram Bot with Backend Integration
## E-commerce Order Management System

---

## Table of Contents
1. [Executive Summary](#executive-summary)
2. [Business Process Description](#business-process-description)
3. [System Architecture](#system-architecture)
4. [Implementation Details](#implementation-details)
5. [Features & Capabilities](#features--capabilities)
6. [Setup & Installation Guide](#setup--installation-guide)
7. [Bot Telegram Features Used](#bot-telegram-features-used)
8. [API Documentation](#api-documentation)
9. [Screenshots & Demo](#screenshots--demo)
10. [Conclusion](#conclusion)

---

## Executive Summary

This project implements a fully functional Telegram bot integrated with a backend REST API for an **E-commerce Order Management System**. The system allows customers to:
- Browse and search products
- Add items to shopping cart
- Manage their cart
- Checkout and place orders
- Track order status

The solution demonstrates advanced RPA concepts including:
- **Process Automation**: Automating e-commerce workflows through messaging
- **Bot Integration**: Multi-layer integration between Telegram platform and backend services
- **Data Exchange**: Real-time synchronization between bot and backend API
- **Business Logic**: Inventory management, order processing, and user management

---

## Business Process Description

### Selected Business Area: E-Commerce

### Business Process: Order Management Workflow

#### Process Overview:
The system automates the complete e-commerce order lifecycle from product discovery to order confirmation.

#### Process Steps:

1. **User Registration & Authentication**
   - User initiates chat with bot
   - Bot registers user in backend system
   - User information stored (Telegram ID, username, name)

2. **Product Browsing**
   - Bot displays catalog of available products
   - Shows product details: name, price, available stock
   - User can browse multiple products

3. **Shopping Cart Management**
   - User selects product and specifies quantity
   - Bot validates stock availability
   - Item added to user's cart in backend
   - User can view cart contents and total price

4. **Order Creation**
   - User initiates checkout
   - Bot requests delivery address
   - Backend creates order from cart items
   - System reduces product inventory
   - Order confirmation sent to user with Order ID

5. **Order Tracking**
   - User can view all past orders
   - Real-time status updates (PENDING, CONFIRMED, PROCESSING, SHIPPED, DELIVERED)
   - Order details include total cost, items, and dates

6. **Inventory Management**
   - Backend tracks stock for each product
   - Stock reduced when order is created
   - Stock restored if order is cancelled
   - Stock availability checked before adding to cart

#### Key Process Advantages:
- ✅ **Automation**: Eliminates manual order entry
- ✅ **Real-time**: Instant updates and confirmation
- ✅ **Accessibility**: Available through popular messaging app
- ✅ **Efficiency**: Reduces customer support overhead
- ✅ **Data Accuracy**: Centralized backend ensures consistency

---

## System Architecture

### High-Level Architecture Diagram

```
┌─────────────────────────────────────────────────────────┐
│              TELEGRAM USER INTERFACE                     │
│  (Telegram App on Mobile/Desktop/Web)                   │
└──────────────────┬──────────────────────────────────────┘
                   │
                   │ Telegram Bot API
                   │ (HTTPS)
                   │
┌──────────────────▼──────────────────────────────────────┐
│         PYTHON TELEGRAM BOT (telegram_bot.py)            │
│                                                          │
│  • Command Handlers (/start, /help, /products)         │
│  • Button & Callback Handlers                          │
│  • User Conversation Management                        │
│  • API Client for Backend Communication                │
└──────────────────┬──────────────────────────────────────┘
                   │
                   │ REST API Calls (HTTP/JSON)
                   │
┌──────────────────▼──────────────────────────────────────┐
│        NODE.JS EXPRESS BACKEND (server.js)              │
│                                                          │
│  Endpoints:                                            │
│  • /api/users/register                                 │
│  • /api/products                                       │
│  • /api/cart/*                                         │
│  • /api/orders/*                                       │
└──────────────────┬──────────────────────────────────────┘
                   │
                   │ In-Memory Database
                   │ (Maps for users, products, orders)
                   │
           ┌───────▼────────┐
           │                │
        ┌──▼──────┐    ┌────▼──────┐
        │  Users  │    │ Products  │
        └─────────┘    │  Orders   │
                       └───────────┘
```

### Components:

#### 1. **Telegram Bot (Python)**
- **Technology**: Python 3.x with `python-telegram-bot` library
- **Purpose**: User interface and interaction layer
- **Features**:
  - Inline keyboard navigation
  - Conversation state management
  - Asynchronous message handling
  - REST API integration

#### 2. **Backend API (Node.js/Express)**
- **Technology**: Node.js with Express framework
- **Purpose**: Business logic and data management
- **Features**:
  - RESTful API endpoints
  - User management
  - Product catalog
  - Order processing
  - Cart management
  - Stock control

#### 3. **Data Layer**
- **In-Memory Storage**: Maps for persistence during runtime
- **Data Models**:
  - Users: telegram_id, username, cart, orders
  - Products: id, name, price, stock
  - Orders: order_id, items, total, status, delivery_address

---

## Implementation Details

### 1. Backend API (Node.js)

#### Dependencies:
```json
{
  "express": "^4.18.2",
  "body-parser": "^1.20.2",
  "cors": "^2.8.5",
  "uuid": "^9.0.0",
  "axios": "^1.4.0"
}
```

#### Key Features:

##### User Management
```
POST /api/users/register
- Registers new user or retrieves existing
- Stores user profile and cart

GET /api/users/:telegram_id
- Retrieves user profile and order history
```

##### Product Management
```
GET /api/products
- Returns all available products with prices and stock

GET /api/products/:product_id
- Returns specific product details
```

##### Cart Operations
```
POST /api/cart/add
- Adds item to user's cart with quantity validation

GET /api/cart/:telegram_id
- Retrieves user's cart and calculates total

POST /api/cart/remove
- Removes specific item from cart

POST /api/cart/clear
- Clears entire cart
```

##### Order Processing
```
POST /api/orders/create
- Creates order from cart
- Validates inventory
- Reduces stock
- Returns order confirmation

GET /api/orders/user/:telegram_id
- Retrieves all user's orders

GET /api/orders/:order_id
- Retrieves specific order details

PUT /api/orders/:order_id/status
- Updates order status (admin function)

POST /api/orders/:order_id/cancel
- Cancels order and restores stock
```

### 2. Telegram Bot (Python)

#### Architecture:

```python
┌─────────────────────────────────────┐
│   Command Handlers                  │
│  /start, /help, /products           │
└────────────┬────────────────────────┘
             │
┌────────────▼────────────────────────┐
│   Callback Query Handlers            │
│  Button clicks, Menu navigation      │
└────────────┬────────────────────────┘
             │
┌────────────▼────────────────────────┐
│   Message Handlers                   │
│  Delivery address input              │
└────────────┬────────────────────────┘
             │
┌────────────▼────────────────────────┐
│   Backend API Client                 │
│  Async HTTP requests to backend      │
└─────────────────────────────────────┘
```

#### Key Functions:

**Command Handlers:**
- `start()`: Initialize user and show main menu
- `help_command()`: Display help information
- `products_command()`: Show product catalog

**Menu Functions:**
- `show_main_menu()`: Display main navigation
- `show_products()`: Browse products with selection
- `show_cart()`: View cart items and checkout
- `show_orders()`: Track order history
- `show_about()`: Application information

**Conversation Flow:**
- User sees inline keyboard with options
- User clicks button → Bot processes callback
- Bot communicates with backend
- Backend returns data
- Bot updates message with results

---

## Features & Capabilities

### Telegram Bot Features Used:

#### 1. **Inline Keyboards** ✓
Buttons displayed directly in messages for:
- Main menu navigation
- Product selection
- Quantity selection
- Cart management
- Checkout process

Example:
```
🏠 Main Menu
┌─────────────────────┐
│ 🛍️ Browse Products │
│ 🛒 View Cart       │
│ 📦 My Orders       │
│ ℹ️ About           │
└─────────────────────┘
```

#### 2. **Stickers** ✓
Emojis and Unicode characters used throughout:
- 🎉 Welcome emoji
- 🛍️ Shopping emoji
- 🛒 Cart emoji
- 📦 Package emoji
- ✅ Checkmark
- ❌ Error indicator
- ⏳ Pending status
- 🚚 Shipping emoji
- And many more...

#### 3. **Mini Apps / Web Apps** ✓
While not traditional web apps, the system provides:
- Rich inline interface with formatted messages
- Dynamic menu updates
- Real-time data binding
- Markdown formatting for better UX
- Conversation states for complex interactions

#### 4. **Advanced Features:**
- **Asynchronous Operations**: Non-blocking API calls
- **Error Handling**: Graceful error messages
- **State Management**: Tracking user journey
- **Data Persistence**: Backend-based storage
- **Real-time Updates**: Instant order confirmations

---

## Setup & Installation Guide

### Prerequisites:
- Python 3.8+
- Node.js 14+
- npm (Node Package Manager)
- Telegram BotFather account (for bot token)

### Step 1: Get Telegram Bot Token

1. Open Telegram and search for **@BotFather**
2. Click `/start` and follow instructions
3. Create new bot with `/newbot`
4. Get your BOT_TOKEN from BotFather
5. Note the HTTP API token

### Step 2: Setup Backend (Node.js)

```powershell
cd c:\Users\arjun\OneDrive\Desktop\SEM 7\Process Automation\telegrambot\backend

# Install dependencies
npm install

# Start backend server
npm start
# Server runs on http://localhost:3000
```

### Step 3: Setup Telegram Bot (Python)

```powershell
cd c:\Users\arjun\OneDrive\Desktop\SEM 7\Process Automation\telegrambot\bot

# Create virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Update bot token in telegram_bot.py
# Replace: BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"
# With: BOT_TOKEN = "YOUR_ACTUAL_TOKEN"

# Run bot
python telegram_bot.py
```

### Step 4: Verify Setup

1. Start backend first (Node.js server must be running)
2. Start bot (Python script)
3. Search for your bot on Telegram
4. Click `/start` to begin

---

## Bot Telegram Features Used

### Feature 1: Inline Keyboards
**Implementation:**
```python
keyboard = [
    [InlineKeyboardButton("🛍️ Browse Products", callback_data="browse_products")],
    [InlineKeyboardButton("🛒 View Cart", callback_data="view_cart")],
    [InlineKeyboardButton("📦 My Orders", callback_data="my_orders")],
    [InlineKeyboardButton("ℹ️ About", callback_data="about")]
]
reply_markup = InlineKeyboardMarkup(keyboard)
await update.message.reply_text("Select an option:", reply_markup=reply_markup)
```

**Use Cases:**
- Navigation menus
- Product selection
- Quantity selection
- Order management
- Checkout confirmation

### Feature 2: Stickers & Emojis
**Implementation:**
```python
status_emoji = {
    'PENDING': '⏳',
    'CONFIRMED': '✅',
    'PROCESSING': '⚙️',
    'SHIPPED': '🚚',
    'DELIVERED': '📦',
    'CANCELLED': '❌'
}
```

**Benefits:**
- Visual feedback
- Better UX
- Status indication
- Emotional connection
- Accessibility

### Feature 3: Rich Formatting
**Implementation:**
```python
text = """
*🛍️ EduMart Store*

*Available Products:*
• *Laptop* - $999.99
• *Smartphone* - $599.99

*Total: $1599.98*
"""
await message.reply_text(text, parse_mode="Markdown")
```

**Features:**
- Bold text: *text*
- Inline code: `code`
- Links: [Link](url)
- Markdown support

---

## API Documentation

### Base URL
```
http://localhost:3000/api
```

### Authentication
No authentication required (demo purposes)

### Endpoints Reference

#### Users

**Register User**
```
POST /api/users/register
Content-Type: application/json

{
  "telegram_id": "123456789",
  "username": "john_doe",
  "first_name": "John"
}

Response: 200 OK
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

#### Products

**Get All Products**
```
GET /api/products

Response: 200 OK
{
  "products": [
    {
      "id": "PROD001",
      "name": "Laptop",
      "price": 999.99,
      "stock": 10
    },
    ...
  ],
  "count": 5
}
```

#### Cart

**Add to Cart**
```
POST /api/cart/add
Content-Type: application/json

{
  "telegram_id": "123456789",
  "product_id": "PROD001",
  "quantity": 1
}

Response: 200 OK
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

**View Cart**
```
GET /api/cart/123456789

Response: 200 OK
{
  "cart": [...],
  "total": "999.99",
  "item_count": 1
}
```

#### Orders

**Create Order**
```
POST /api/orders/create
Content-Type: application/json

{
  "telegram_id": "123456789",
  "delivery_address": "123 Main St, City",
  "payment_method": "CARD"
}

Response: 200 OK
{
  "success": true,
  "order": {
    "order_id": "550e8400-e29b-41d4-a716-446655440000",
    "telegram_id": "123456789",
    "items": [...],
    "total": "999.99",
    "status": "PENDING",
    "delivery_address": "123 Main St, City",
    "created_at": "2025-11-29T10:05:00Z"
  }
}
```

**Get User Orders**
```
GET /api/orders/user/123456789

Response: 200 OK
{
  "orders": [
    {
      "order_id": "550e8400...",
      "total": "999.99",
      "status": "PENDING",
      "created_at": "2025-11-29T10:05:00Z"
    }
  ]
}
```

---

## Screenshots & Demo

### Bot Interaction Flow

#### Step 1: Start Bot
```
User: /start
Bot: 🎉 Welcome to EduMart Store, John!
     Your online shopping assistant for tech products.
     What would you like to do?
     
     [🛍️ Browse Products]
     [🛒 View Cart]
     [📦 My Orders]
     [ℹ️ About]
```

#### Step 2: Browse Products
```
User: [🛍️ Browse Products]
Bot: 📦 Available Products:
     
     • Laptop - $999.99
       Stock: 10 items
     
     • Smartphone - $599.99
       Stock: 25 items
     
     • Headphones - $149.99
       Stock: 50 items
     
     [📌 Laptop - $999.99]
     [📌 Smartphone - $599.99]
     [📌 Headphones - $149.99]
     [⬅️ Back]
```

#### Step 3: Select Product & Quantity
```
User: [📌 Laptop - $999.99]
Bot: How many items would you like?
     
     [1][2][3][5]
     [10][⬅️ Back]

User: [1]
Bot: ✅ Added 1 item(s) to cart!
     
     [🛒 View Cart]
     [🛍️ Continue Shopping]
```

#### Step 4: View Cart
```
User: [🛒 View Cart]
Bot: 🛒 Your Shopping Cart:
     
     • Laptop
       Price: $999.99 × 1 = $999.99
     
     Total: $999.99
     
     [❌ Remove Laptop]
     [💳 Proceed to Checkout]
     [⬅️ Back]
```

#### Step 5: Checkout
```
User: [💳 Proceed to Checkout]
Bot: 📍 Please enter your delivery address:

User: 123 Main Street, New York, NY 10001
Bot: ✅ Order Confirmed!
     
     Order ID: 550e8400...
     Total: $999.99
     Status: PENDING
     Delivery Address: 123 Main Street, New York, NY 10001
     
     Your order has been placed successfully!
     We'll update you on the status soon. 📦
     
     [📦 Track Orders]
     [🏠 Main Menu]
```

#### Step 6: Track Orders
```
User: [📦 Track Orders]
Bot: 📦 Your Orders:
     
     ⏳ Order 550e8400...
       Total: $999.99
       Status: PENDING
       Date: 2025-11-29
     
     [⬅️ Back]
```

---

## Integration Points

### Bot ↔ Backend Communication

1. **User Registration**
   ```
   Bot sends: { telegram_id, username, first_name }
   Backend: Creates user profile, initializes cart
   Response: User object with empty cart
   ```

2. **Product Retrieval**
   ```
   Bot sends: GET request
   Backend: Queries products map
   Response: List of all products with prices
   ```

3. **Add to Cart**
   ```
   Bot sends: { telegram_id, product_id, quantity }
   Backend: Validates stock, adds to cart
   Response: Updated cart contents
   ```

4. **Create Order**
   ```
   Bot sends: { telegram_id, delivery_address, payment_method }
   Backend: Creates order, reduces inventory, clears cart
   Response: Order confirmation with ID
   ```

5. **Order Tracking**
   ```
   Bot sends: GET request with user ID
   Backend: Retrieves all user orders with status
   Response: List of orders with details
   ```

---

## Error Handling

### Backend Errors
- Missing fields → 400 Bad Request
- User not found → 404 Not Found
- Insufficient stock → 400 Bad Request
- Invalid status → 400 Bad Request

### Bot Error Handling
- API timeouts → Graceful error message
- Connection failures → "Could not connect to backend"
- Empty responses → "No results found"
- All errors logged for debugging

---

## Testing Scenarios

### Test Case 1: Complete Purchase
1. Start bot
2. Browse products
3. Add laptop to cart
4. View cart
5. Proceed to checkout
6. Enter delivery address
7. Verify order confirmation
8. Check order tracking

### Test Case 2: Multiple Items
1. Add multiple products to cart
2. Adjust quantities
3. View cart with correct total
4. Checkout and verify order

### Test Case 3: Cart Management
1. Add items to cart
2. Remove specific items
3. Verify cart updates
4. Clear cart

### Test Case 4: Order History
1. Create multiple orders
2. View order history
3. Check order statuses
4. Verify order details

---

## Conclusion

This project successfully demonstrates:

✅ **Business Process Automation**
- Complete e-commerce workflow automated through Telegram

✅ **Bot Integration**
- Seamless integration between Telegram and custom backend

✅ **Backend Communication**
- RESTful API design for bot-backend interaction

✅ **Advanced Features**
- Inline keyboards for navigation
- Emojis for visual feedback
- Rich text formatting
- State management
- Error handling

✅ **Scalability**
- Modular architecture
- Extensible API endpoints
- Easy to add new features

### Possible Enhancements:
1. Database integration (MongoDB/PostgreSQL)
2. Payment gateway integration
3. Order tracking with real GPS
4. Customer support chat
5. Admin dashboard
6. Push notifications
7. User authentication with tokens
8. Email notifications

---

## Files & Structure

```
telegrambot/
├── backend/
│   ├── package.json          (Node.js dependencies)
│   └── server.js             (Express API server)
├── bot/
│   ├── telegram_bot.py       (Main bot code)
│   └── requirements.txt       (Python dependencies)
└── docs/
    └── README.md             (This file)
```

---

## How to Run

### Terminal 1 - Backend:
```powershell
cd backend
npm install
npm start
# Backend runs on http://localhost:3000
```

### Terminal 2 - Bot:
```powershell
cd bot
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python telegram_bot.py
```

### Terminal 3 - Testing:
```powershell
# You can test the API directly
curl http://localhost:3000/api/products
```

---

**Lab Completed Successfully!** 🎉

---

*Date: November 29, 2025*
*Lab: RPA Lab #3 - Telegram Bot with Backend Integration*
*Subject: Process Automation*
