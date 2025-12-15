@echo off
REM Start Backend Server

echo.
echo ========================================
echo  Starting Backend Server (Node.js)
echo ========================================
echo.

cd backend

echo [*] Starting server on http://localhost:3000
echo [*] Press Ctrl+C to stop the server
echo.

npm start

pause
