# Quick Reference Guide

## 🚀 Quick Start (5 minutes)

### 1. Initial Setup (One-time)
```powershell
cd c:\Users\arjun\OneDrive\Desktop\SEM 7\Process Automation\telegrambot
setup.bat  # Let it complete
```

### 2. Get Bot Token
- Open Telegram → Search @BotFather
- Type `/newbot` → Follow prompts
- Copy HTTP API token

### 3. Configure Token
- Open `bot/telegram_bot.py`
- Find `BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"`
- Replace with your actual token

### 4. Start System
```powershell
# Terminal 1
start-backend.bat

# Terminal 2 (after backend starts)
start-bot.bat

# Terminal 3 (optional - for API testing)
# Use commands from API_TESTING_GUIDE.md
```

### 5. Test on Telegram
- Search your bot name
- Send `/start` command
- Browse products and place order

---

## 📁 Important Files

| File | Purpose | Action |
|------|---------|--------|
| `bot/telegram_bot.py` | Main bot code | Edit BOT_TOKEN here |
| `backend/server.js` | API server | npm start |
| `docs/README.md` | Main report | Read for details |
| `docs/API_TESTING_GUIDE.md` | Test APIs | Reference for testing |
| `setup.bat` | Auto setup | Run once |
| `start-backend.bat` | Start backend | Run in Terminal 1 |
| `start-bot.bat` | Start bot | Run in Terminal 2 |

---

## 🔧 Common Commands

### Backend Management
```bash
cd backend
npm install          # Install dependencies
npm start            # Start server on port 3000
```

### Bot Management
```bash
cd bot
python -m venv venv                    # Create env
venv\Scripts\activate                  # Activate env
pip install -r requirements.txt        # Install packages
python telegram_bot.py                 # Run bot
```

### API Testing
```bash
# Health check
curl http://localhost:3000/api/health

# Get all products
curl http://localhost:3000/api/products

# Register user (replace values)
curl -X POST http://localhost:3000/api/users/register -H "Content-Type: application/json" -d '{"telegram_id":"123","username":"test","first_name":"Test"}'
```

---

## 🐛 Troubleshooting

### Issue: "Bot doesn't respond"
```powershell
# Check 1: Backend running?
# Windows: Search for Node processes or open http://localhost:3000

# Check 2: Bot token correct?
# Open telegram_bot.py and verify BOT_TOKEN

# Check 3: Python version?
python --version  # Should be 3.8+
```

### Issue: "Cannot connect to localhost:3000"
```powershell
# Check 1: Backend started?
# Look for "E-commerce Backend Server running on..."

# Check 2: Port already in use?
netstat -ano | findstr :3000
# Kill process: taskkill /PID <PID> /F
```

### Issue: "ModuleNotFoundError"
```powershell
cd bot
venv\Scripts\activate
pip install --upgrade -r requirements.txt
```

---

## 📊 API Quick Reference

### Base URL
```
http://localhost:3000/api
```

### Core Endpoints

**Register User**
```
POST /api/users/register
Body: {"telegram_id":"123","username":"user","first_name":"Name"}
```

**Get Products**
```
GET /api/products
```

**Add to Cart**
```
POST /api/cart/add
Body: {"telegram_id":"123","product_id":"PROD001","quantity":1}
```

**Create Order**
```
POST /api/orders/create
Body: {"telegram_id":"123","delivery_address":"...","payment_method":"CARD"}
```

**View Orders**
```
GET /api/orders/user/123
```

---

## 🎯 Bot Commands

| Command | Result |
|---------|--------|
| `/start` | Main menu |
| `/help` | Help info |
| `/products` | Product list |
| Button Click | Menu navigation |
| Type Message | Delivery address |

---

## 📦 Sample Product IDs

| Product | ID | Price |
|---------|-------|-------|
| Laptop | PROD001 | $999.99 |
| Smartphone | PROD002 | $599.99 |
| Headphones | PROD003 | $149.99 |
| Tablet | PROD004 | $399.99 |
| Smartwatch | PROD005 | $199.99 |

---

## 🔐 Security Notes

- ✅ Keep BOT_TOKEN private (don't commit)
- ✅ Use HTTPS in production
- ✅ Add authentication for real deployment
- ✅ Validate all user inputs
- ✅ Use environment variables for secrets

---

## 📈 System Requirements

| Requirement | Minimum | Recommended |
|-------------|---------|-------------|
| Python | 3.8 | 3.10+ |
| Node.js | 14 | 18+ |
| RAM | 2GB | 4GB+ |
| Disk | 500MB | 1GB |
| Internet | Required | Broadband |

---

## 🎓 Learning Path

1. **Understand Business Process**
   - Read: `docs/README.md` (Business Process section)

2. **Setup System**
   - Follow: Quick Start above
   - Run: setup.bat

3. **Explore Bot**
   - Test: Basic commands on Telegram
   - Try: Browse products, add to cart

4. **Test API**
   - Read: `docs/API_TESTING_GUIDE.md`
   - Test: All endpoints with curl

5. **Study Code**
   - Review: `backend/server.js` (endpoints)
   - Review: `bot/telegram_bot.py` (handlers)

6. **Deploy** (Optional)
   - Read: `docs/DEPLOYMENT_GUIDE.md`
   - Choose: Cloud provider
   - Deploy: Following guide

---

## 💡 Pro Tips

1. **Testing multiple users?**
   - Use different telegram_id values
   - Each user gets own cart and orders

2. **Want to reset?**
   - Restart backend (clears in-memory data)
   - Re-register users

3. **Adding new products?**
   - Edit `initializeProducts()` in `backend/server.js`
   - Restart backend

4. **Debug issues?**
   - Enable logging in both files
   - Check terminal output
   - Use Postman for API debugging

5. **Performance?**
   - In-memory storage is fast
   - Upgrade to database for production
   - Add caching for frequently accessed data

---

## 📱 Bot Interaction Example

```
START
  ↓
User opens Telegram → Searches your bot
  ↓
Types: /start
  ↓
Bot responds with 4 options (inline buttons)
  ↓
User clicks: 🛍️ Browse Products
  ↓
Bot shows 5 products with buttons
  ↓
User clicks: Laptop ($999.99)
  ↓
Bot asks: How many items?
  ↓
User clicks: 1
  ↓
Bot confirms: ✅ Added to cart!
  ↓
User clicks: 🛒 View Cart
  ↓
Bot shows: Cart items and total ($999.99)
  ↓
User clicks: 💳 Checkout
  ↓
Bot asks: Enter delivery address
  ↓
User types: 123 Main St, New York
  ↓
Bot confirms: Order created! ID: 550e8400...
  ↓
END
```

---

## 🎯 What To Submit

- ✅ All project files (backend, bot, docs)
- ✅ This quick reference
- ✅ Main report (README.md in docs/)
- ✅ All code files
- ✅ Setup instructions
- ✅ Documentation

---

## 📞 Getting Help

### Error in Bot?
→ Check: `bot/README.md`

### API Issues?
→ Check: `docs/API_TESTING_GUIDE.md`

### Architecture Questions?
→ Check: `docs/PROJECT_STRUCTURE.md`

### Deployment Help?
→ Check: `docs/DEPLOYMENT_GUIDE.md`

### General Issues?
→ Check: Terminal logs where bot/backend runs

---

## ✅ Verification Checklist

Before submission, verify:

- [ ] Backend starts without errors
- [ ] Bot token configured
- [ ] Bot starts and connects to backend
- [ ] Can send `/start` command
- [ ] Can browse products
- [ ] Can add to cart
- [ ] Can checkout with address
- [ ] Order confirmation appears
- [ ] Can view order history
- [ ] All documentation present

---

## 🚀 Next Steps (Optional)

1. Add database integration
2. Implement payment gateway
3. Add email notifications
4. Create admin dashboard
5. Deploy to Azure/AWS
6. Add product reviews
7. Implement wishlist
8. Add promotional codes

---

## 📚 Documentation Structure

```
docs/
├── README.md                    ← START HERE (main report)
├── API_TESTING_GUIDE.md        ← For API testing
├── PROJECT_STRUCTURE.md        ← For architecture
└── DEPLOYMENT_GUIDE.md         ← For production setup
```

---

**Remember**: Start with Backend → Then Bot → Then Test

Good luck! 🎉

---

*Last Updated: November 29, 2025*
*Lab: RPA Lab #3*
*Status: Ready for Submission*
