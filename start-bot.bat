@echo off
REM Start Telegram Bot

echo.
echo ========================================
echo  Starting Telegram Bot (Python)
echo ========================================
echo.

cd bot

echo [*] Activating virtual environment...
call venv\Scripts\activate.bat

echo [*] Starting bot...
echo [*] Make sure backend is running on http://localhost:3000
echo [*] Press Ctrl+C to stop the bot
echo.

python telegram_bot.py

pause
