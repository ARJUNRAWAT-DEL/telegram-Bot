const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');
const { v4: uuidv4 } = require('uuid');
const fs = require('fs');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(bodyParser.json());
app.use(cors());

// Database file path
const DB_FILE = path.join(__dirname, 'database.json');

// In-memory database
const orders = new Map();
const users = new Map();
const products = new Map();

// Load database from file or initialize
function loadDatabase() {
  if (fs.existsSync(DB_FILE)) {
    try {
      const data = JSON.parse(fs.readFileSync(DB_FILE, 'utf8'));
      
      // Load products
      if (data.products) {
        data.products.forEach(product => {
          products.set(product.id, product);
        });
      }
      
      // Load users
      if (data.users) {
        data.users.forEach(user => {
          users.set(user.telegram_id, user);
        });
      }
      
      // Load orders
      if (data.orders) {
        data.orders.forEach(order => {
          orders.set(order.id, order);
        });
      }
      
      console.log('✅ Database loaded from file');
    } catch (error) {
      console.log('⚠️ Error loading database, initializing fresh:', error.message);
      initializeProducts();
    }
  } else {
    initializeProducts();
  }
}

// Save database to file
function saveDatabase() {
  const data = {
    products: Array.from(products.values()),
    users: Array.from(users.values()),
    orders: Array.from(orders.values()),
    lastSaved: new Date().toISOString()
  };
  
  fs.writeFileSync(DB_FILE, JSON.stringify(data, null, 2), 'utf8');
}

// Initialize sample products
function initializeProducts() {
  const sampleProducts = [
    { 
      id: 'PROD001', 
      name: 'Laptop', 
      price: 999.99, 
      stock: 10,
      image: './images/PROD001.png',
      category: 'Electronics',
      description: 'High-performance laptop with SSD'
    },
    { 
      id: 'PROD002', 
      name: 'Smartphone', 
      price: 599.99, 
      stock: 25,
      image: './images/PROD002.png',
      category: 'Electronics',
      description: '5G enabled smartphone'
    },
    { 
      id: 'PROD003', 
      name: 'Headphones', 
      price: 149.99, 
      stock: 50,
      image: './images/PROD003.png',
      category: 'Audio',
      description: 'Noise-canceling wireless headphones'
    },
    { 
      id: 'PROD004', 
      name: 'Tablet', 
      price: 399.99, 
      stock: 15,
      image: './images/PROD004.png',
      category: 'Electronics',
      description: '10-inch touchscreen tablet'
    },
    { 
      id: 'PROD005', 
      name: 'Smartwatch', 
      price: 199.99, 
      stock: 30,
      image: './images/PROD005.png',
      category: 'Wearables',
      description: 'Fitness tracking smartwatch'
    }
  ];
  sampleProducts.forEach(product => {
    products.set(product.id, product);
  });
  
  saveDatabase();
}

loadDatabase();

// ===== USER ENDPOINTS =====

// Register/Get User
app.post('/api/users/register', (req, res) => {
  try {
    const { telegram_id, username, first_name } = req.body;
    
    if (!telegram_id) {
      return res.status(400).json({ error: 'telegram_id is required' });
    }

    if (!users.has(telegram_id)) {
      users.set(telegram_id, {
        telegram_id,
        username: username || 'Unknown',
        first_name: first_name || 'User',
        created_at: new Date().toISOString(),
        cart: [],
        orders: []
      });
    }

    const user = users.get(telegram_id);
    res.json({ success: true, user });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Get User Profile
app.get('/api/users/:telegram_id', (req, res) => {
  try {
    const { telegram_id } = req.params;
    
    if (!users.has(telegram_id)) {
      return res.status(404).json({ error: 'User not found' });
    }

    const user = users.get(telegram_id);
    res.json(user);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// ===== PRODUCT ENDPOINTS =====

// Get All Products
app.get('/api/products', (req, res) => {
  try {
    const productList = Array.from(products.values());
    res.json({ products: productList, count: productList.length });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Get Product by ID
app.get('/api/products/:product_id', (req, res) => {
  try {
    const { product_id } = req.params;
    
    if (!products.has(product_id)) {
      return res.status(404).json({ error: 'Product not found' });
    }

    const product = products.get(product_id);
    res.json(product);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// ===== CART ENDPOINTS =====

// Add to Cart
app.post('/api/cart/add', (req, res) => {
  try {
    const { telegram_id, product_id, quantity } = req.body;
    
    if (!telegram_id || !product_id || !quantity) {
      return res.status(400).json({ error: 'Missing required fields' });
    }

    if (!users.has(telegram_id)) {
      return res.status(404).json({ error: 'User not found' });
    }

    if (!products.has(product_id)) {
      return res.status(404).json({ error: 'Product not found' });
    }

    const user = users.get(telegram_id);
    const product = products.get(product_id);

    // Check stock
    if (product.stock < quantity) {
      return res.status(400).json({ error: 'Insufficient stock' });
    }

    // Check if product already in cart
    const existingItem = user.cart.find(item => item.product_id === product_id);
    if (existingItem) {
      existingItem.quantity += quantity;
    } else {
      user.cart.push({
        product_id,
        name: product.name,
        price: product.price,
        quantity
      });
    }

    res.json({ success: true, cart: user.cart });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// View Cart
app.get('/api/cart/:telegram_id', (req, res) => {
  try {
    const { telegram_id } = req.params;
    
    if (!users.has(telegram_id)) {
      return res.status(404).json({ error: 'User not found' });
    }

    const user = users.get(telegram_id);
    const total = user.cart.reduce((sum, item) => sum + (item.price * item.quantity), 0);
    
    res.json({
      cart: user.cart,
      total: total.toFixed(2),
      item_count: user.cart.length
    });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Remove from Cart
app.post('/api/cart/remove', (req, res) => {
  try {
    const { telegram_id, product_id } = req.body;
    
    if (!telegram_id || !product_id) {
      return res.status(400).json({ error: 'Missing required fields' });
    }

    if (!users.has(telegram_id)) {
      return res.status(404).json({ error: 'User not found' });
    }

    const user = users.get(telegram_id);
    user.cart = user.cart.filter(item => item.product_id !== product_id);

    res.json({ success: true, cart: user.cart });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Clear Cart
app.post('/api/cart/clear', (req, res) => {
  try {
    const { telegram_id } = req.body;
    
    if (!telegram_id) {
      return res.status(400).json({ error: 'telegram_id is required' });
    }

    if (!users.has(telegram_id)) {
      return res.status(404).json({ error: 'User not found' });
    }

    const user = users.get(telegram_id);
    user.cart = [];

    res.json({ success: true, message: 'Cart cleared' });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// ===== ORDER ENDPOINTS =====

// Create Order
app.post('/api/orders/create', (req, res) => {
  try {
    const { telegram_id, delivery_address, payment_method } = req.body;
    
    if (!telegram_id || !delivery_address) {
      return res.status(400).json({ error: 'Missing required fields' });
    }

    if (!users.has(telegram_id)) {
      return res.status(404).json({ error: 'User not found' });
    }

    const user = users.get(telegram_id);
    
    if (user.cart.length === 0) {
      return res.status(400).json({ error: 'Cart is empty' });
    }

    // Create order
    const orderId = uuidv4();
    const orderTotal = user.cart.reduce((sum, item) => sum + (item.price * item.quantity), 0);
    
    const order = {
      order_id: orderId,
      telegram_id,
      user: user.username,
      items: [...user.cart],
      total: orderTotal.toFixed(2),
      status: 'PENDING',
      delivery_address,
      payment_method: payment_method || 'NOT_SPECIFIED',
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString()
    };

    // Update product stock
    user.cart.forEach(item => {
      const product = products.get(item.product_id);
      product.stock -= item.quantity;
    });

    // Clear cart
    user.cart = [];
    
    // Store order
    orders.set(orderId, order);
    user.orders.push(orderId);
    
    // Save database
    saveDatabase();

    res.json({ success: true, order });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Get User Orders
app.get('/api/orders/user/:telegram_id', (req, res) => {
  try {
    const { telegram_id } = req.params;
    
    if (!users.has(telegram_id)) {
      return res.status(404).json({ error: 'User not found' });
    }

    const user = users.get(telegram_id);
    const userOrders = user.orders.map(orderId => orders.get(orderId));

    res.json({ orders: userOrders });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Get Order by ID
app.get('/api/orders/:order_id', (req, res) => {
  try {
    const { order_id } = req.params;
    
    if (!orders.has(order_id)) {
      return res.status(404).json({ error: 'Order not found' });
    }

    const order = orders.get(order_id);
    res.json(order);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Update Order Status
app.put('/api/orders/:order_id/status', (req, res) => {
  try {
    const { order_id } = req.params;
    const { status } = req.body;

    if (!orders.has(order_id)) {
      return res.status(404).json({ error: 'Order not found' });
    }

    const validStatuses = ['PENDING', 'CONFIRMED', 'PROCESSING', 'SHIPPED', 'DELIVERED', 'CANCELLED'];
    if (!validStatuses.includes(status)) {
      return res.status(400).json({ error: 'Invalid status' });
    }

    const order = orders.get(order_id);
    order.status = status;
    order.updated_at = new Date().toISOString();

    res.json({ success: true, order });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Cancel Order
app.post('/api/orders/:order_id/cancel', (req, res) => {
  try {
    const { order_id } = req.params;
    
    if (!orders.has(order_id)) {
      return res.status(404).json({ error: 'Order not found' });
    }

    const order = orders.get(order_id);
    
    if (order.status === 'DELIVERED' || order.status === 'CANCELLED') {
      return res.status(400).json({ error: 'Cannot cancel order with status: ' + order.status });
    }

    // Restore product stock
    order.items.forEach(item => {
      const product = products.get(item.product_id);
      product.stock += item.quantity;
    });

    order.status = 'CANCELLED';
    order.updated_at = new Date().toISOString();
    
    // Save database
    saveDatabase();

    res.json({ success: true, order });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// ===== ADMIN ENDPOINTS =====

// Restock Product (Admin only)
app.post('/api/admin/restock', (req, res) => {
  try {
    const { admin_token, product_id, quantity } = req.body;
    
    // Simple admin token validation (in production, use JWT or proper auth)
    const ADMIN_TOKEN = process.env.ADMIN_TOKEN || 'admin-secret-key-2024';
    
    if (admin_token !== ADMIN_TOKEN) {
      return res.status(401).json({ error: 'Unauthorized: Invalid admin token' });
    }
    
    if (!product_id || !quantity || quantity <= 0) {
      return res.status(400).json({ error: 'Invalid product_id or quantity' });
    }
    
    if (!products.has(product_id)) {
      return res.status(404).json({ error: 'Product not found' });
    }
    
    const product = products.get(product_id);
    const previousStock = product.stock;
    product.stock += quantity;
    
    // Save database
    saveDatabase();
    
    res.json({
      success: true,
      message: `✅ Restocking successful!`,
      product: {
        id: product.id,
        name: product.name,
        previousStock,
        addedQuantity: quantity,
        newStock: product.stock,
        timestamp: new Date().toISOString()
      }
    });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Get Inventory Status
app.get('/api/admin/inventory', (req, res) => {
  try {
    const { admin_token } = req.query;
    
    // Simple admin token validation
    const ADMIN_TOKEN = process.env.ADMIN_TOKEN || 'admin-secret-key-2024';
    
    if (admin_token !== ADMIN_TOKEN) {
      return res.status(401).json({ error: 'Unauthorized: Invalid admin token' });
    }
    
    const inventory = Array.from(products.values()).map(product => ({
      id: product.id,
      name: product.name,
      price: product.price,
      stock: product.stock,
      category: product.category,
      description: product.description
    }));
    
    res.json({
      success: true,
      totalProducts: inventory.length,
      inventory
    });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Get Database Status
app.get('/api/admin/database-status', (req, res) => {
  try {
    const { admin_token } = req.query;
    
    // Simple admin token validation
    const ADMIN_TOKEN = process.env.ADMIN_TOKEN || 'admin-secret-key-2024';
    
    if (admin_token !== ADMIN_TOKEN) {
      return res.status(401).json({ error: 'Unauthorized: Invalid admin token' });
    }
    
    const stats = {
      totalUsers: users.size,
      totalProducts: products.size,
      totalOrders: orders.size,
      databaseFile: DB_FILE,
      fileExists: fs.existsSync(DB_FILE),
      timestamp: new Date().toISOString()
    };
    
    res.json({
      success: true,
      ...stats
    });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// ===== HEALTH CHECK =====

app.get('/api/health', (req, res) => {
  res.json({ status: 'OK', timestamp: new Date().toISOString() });
});

// ===== ERROR HANDLING =====

app.use((req, res) => {
  res.status(404).json({ error: 'Endpoint not found' });
});

// Start server
app.listen(PORT, () => {
  console.log(`E-commerce Backend Server running on http://localhost:${PORT}`);
  console.log(`API Health Check: http://localhost:${PORT}/api/health`);
});
