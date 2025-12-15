# Telegram Bot Setup Guide

## Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (comes with Python)
- Telegram account

### Step 1: Get Bot Token from BotFather

1. Open Telegram app
2. Search for `@BotFather`
3. Send `/start` command
4. Send `/newbot` command
5. Choose a name for your bot (e.g., "EduMart Bot")
6. Choose a username for your bot (must end with 'bot', e.g., "edumart_bot")
7. **Copy the HTTP API token** provided by BotFather

### Step 2: Setup Python Environment

1. Navigate to bot directory:
   ```powershell
   cd bot
   ```

2. Create virtual environment:
   ```powershell
   python -m venv venv
   ```

3. Activate virtual environment:
   ```powershell
   venv\Scripts\activate
   ```

### Step 3: Install Dependencies

```powershell
pip install -r requirements.txt
```

### Step 4: Configure Bot Token

1. Open `telegram_bot.py` in a text editor
2. Find line: `BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"`
3. Replace with your actual token from BotFather:
   ```python
   BOT_TOKEN = "123456789:ABCDefGHIjklMNOpqrSTUvwxyz"
   ```

### Step 5: Start the Bot

Make sure the backend is running first (on http://localhost:3000)

Then run:
```powershell
python telegram_bot.py
```

You should see:
```
🤖 Telegram Bot is starting...
Backend URL: http://localhost:3000/api
```

### Step 6: Test the Bot

1. Open Telegram
2. Search for your bot username (e.g., @edumart_bot)
3. Click `/start` or send `/start` command
4. You should see the welcome menu

## Bot Commands

- `/start` - Start bot and show main menu
- `/help` - Show help information
- `/products` - Browse products

## Features

✅ Browse product catalog
✅ Add items to cart
✅ View shopping cart
✅ Place orders
✅ Track order history
✅ Real-time backend integration
✅ Inline keyboard navigation
✅ Rich emoji support
✅ Order status tracking

## Troubleshooting

### Bot doesn't respond
- Check internet connection
- Verify bot token is correct
- Make sure backend is running
- Check bot token in @BotFather

### Connection errors
- Make sure Node.js backend is running on port 3000
- Check firewall settings
- Verify backend URL in code

### Module import errors
```powershell
# Reinstall dependencies
pip install --upgrade -r requirements.txt
```

### Python version errors
```powershell
# Check Python version
python --version  # Should be 3.8+

# If needed, install Python 3.8+ from python.org
```

## Architecture

```
Telegram User
     ↓
Telegram Server (Telegram Bot API)
     ↓
Python Telegram Bot (telegram_bot.py)
     ↓
Node.js Backend API (server.js)
     ↓
In-Memory Database (Maps)
```

## Configuration

### Backend URL
Edit `BACKEND_URL` variable to change backend address:
```python
BACKEND_URL = "http://localhost:3000/api"
```

### Logging
Logging is configured for INFO level. To change:
```python
logging.basicConfig(level=logging.DEBUG)  # For verbose logging
```

## API Integration

The bot integrates with backend through these calls:

1. **Register User** - On bot start
2. **Get Products** - When browsing catalog
3. **Add to Cart** - When user selects product
4. **Get Cart** - When user views cart
5. **Create Order** - When user checks out
6. **Get Orders** - When user views order history

## Performance Notes

- Async/await for non-blocking operations
- Timeout set to 10 seconds for API calls
- Graceful error handling for failures
- Memory efficient message handling

## Security Notes

For production deployment:
- Use environment variables for bot token
- Add rate limiting
- Implement user authentication
- Use HTTPS for backend
- Add input validation
- Implement logging and monitoring

## Development Tips

1. Use logging to debug issues:
   ```python
   logger.info("Debug message")
   logger.error("Error message")
   ```

2. Test API calls manually:
   ```powershell
   curl http://localhost:3000/api/health
   ```

3. Use Telegram's `/debug` mode for development

## Files

- `telegram_bot.py` - Main bot code
- `requirements.txt` - Python dependencies
- `README.md` - This file

## Support

For issues:
1. Check logs in terminal
2. Verify backend is running
3. Check bot token is correct
4. Verify internet connection
5. Check firewall rules
