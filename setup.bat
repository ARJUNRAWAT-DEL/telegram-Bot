@echo off
REM Startup script for E-commerce Telegram Bot System

echo.
echo ========================================
echo  E-Commerce Telegram Bot Setup
echo ========================================
echo.

REM Check if Node.js is installed
where node >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Node.js is not installed or not in PATH
    echo Please install Node.js from https://nodejs.org/
    pause
    exit /b 1
)

REM Check if Python is installed
where python >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python from https://www.python.org/
    pause
    exit /b 1
)

echo [OK] Node.js found: 
node --version
echo.

echo [OK] Python found: 
python --version
echo.

REM Setup Backend
echo ========================================
echo  Setting up Backend (Node.js)...
echo ========================================
cd backend
echo [*] Installing Node.js dependencies...
call npm install
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Failed to install Node.js dependencies
    pause
    exit /b 1
)
echo [OK] Backend setup complete!
echo.
cd ..

REM Setup Bot
echo ========================================
echo  Setting up Bot (Python)...
echo ========================================
cd bot
echo [*] Creating Python virtual environment...
python -m venv venv
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Failed to create virtual environment
    pause
    exit /b 1
)

echo [*] Activating virtual environment...
call venv\Scripts\activate.bat

echo [*] Installing Python dependencies...
pip install -r requirements.txt
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Failed to install Python dependencies
    pause
    exit /b 1
)
echo [OK] Bot setup complete!
echo.
cd ..

echo ========================================
echo  Setup Completed Successfully!
echo ========================================
echo.
echo [IMPORTANT] Next Steps:
echo.
echo 1. Get Telegram Bot Token:
echo    - Open Telegram and search for @BotFather
echo    - Send /newbot and follow instructions
echo    - Copy the HTTP API token
echo.
echo 2. Configure Bot Token:
echo    - Open bot/telegram_bot.py in a text editor
echo    - Find: BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"
echo    - Replace with your actual token
echo.
echo 3. Start the System:
echo    - Run start-backend.bat in Terminal 1
echo    - Run start-bot.bat in Terminal 2
echo.
echo 4. Test the Bot:
echo    - Search for your bot on Telegram
echo    - Send /start command
echo.
echo ========================================
echo.
pause
