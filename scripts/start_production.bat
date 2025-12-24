@echo off
REM Production startup script for Voice Agent RAG backend (Windows)
REM This serves the same purpose as Gunicorn for traditional web apps

echo 🚀 Starting Voice Agent in Production Mode...

REM Get the directory where this script is located
set SCRIPT_DIR=%~dp0
set APP_DIR=%SCRIPT_DIR%..
set BACKEND_DIR=%APP_DIR%\backend

REM Activate virtual environment if it exists
if exist "%APP_DIR%\venv\Scripts\activate" (
    echo 📦 Activating virtual environment...
    call "%APP_DIR%\venv\Scripts\activate"
)

REM Check if .env file exists
if not exist "%APP_DIR%\.env" (
    echo ❌ Error: .env file not found!
    echo Please copy .env.example to .env and configure your API keys
exit /b 1
)

REM Fix SSL certificate issues on Windows
set REQUESTS_CA_BUNDLE=
set SSL_CERT_FILE=

REM Change to backend directory and start
cd /d "%BACKEND_DIR%"
echo 🎙️  Starting LiveKit Voice Agent...
python voice_agent_openai.py start
