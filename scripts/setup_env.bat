@echo off
REM ============================================
REM Voice Agent RAG - Environment Setup Script
REM ============================================
REM This script helps set up environment files for deployment
REM Usage: setup_env.bat

setlocal enabledelayedexpansion

echo.
echo ============================================
echo   Voice Agent RAG - Environment Setup
echo ============================================
echo.

REM Get script directory
set "SCRIPT_DIR=%~dp0"
set "PROJECT_ROOT=%SCRIPT_DIR%.."

REM Check if .env exists
if not exist "%PROJECT_ROOT%\.env" (
    if exist "%PROJECT_ROOT%\.env.example" (
        copy "%PROJECT_ROOT%\.env.example" "%PROJECT_ROOT%\.env" >nul
        echo [OK] Created .env from .env.example
        echo [!] Please edit .env and add your API keys
    ) else (
        echo [ERROR] .env.example not found!
        exit /b 1
    )
) else (
    echo [OK] .env file exists
)

REM Sync to frontend
if not exist "%PROJECT_ROOT%\frontend\.env.local" (
    echo # Auto-generated from root .env > "%PROJECT_ROOT%\frontend\.env.local"
    for /f "tokens=*" %%a in ('findstr /b "LIVEKIT_" "%PROJECT_ROOT%\.env"') do (
        echo %%a >> "%PROJECT_ROOT%\frontend\.env.local"
    )
    echo [OK] Created frontend\.env.local
) else (
    echo [OK] frontend\.env.local exists
)

REM Create logs directory
if not exist "%PROJECT_ROOT%\logs" (
    mkdir "%PROJECT_ROOT%\logs"
    echo [OK] Created logs directory
) else (
    echo [OK] logs directory exists
)

REM Create chat-engine-storage directory
if not exist "%PROJECT_ROOT%\chat-engine-storage" (
    mkdir "%PROJECT_ROOT%\chat-engine-storage"
    echo [OK] Created chat-engine-storage directory
) else (
    echo [OK] chat-engine-storage directory exists
)

echo.
echo ============================================
echo   Environment Check Complete
echo ============================================
echo.
echo Required environment variables in .env:
echo   - LIVEKIT_URL (e.g., wss://your-project.livekit.cloud)
echo   - LIVEKIT_API_KEY
echo   - LIVEKIT_API_SECRET
echo   - OPENROUTER_API_KEY
echo   - DEEPGRAM_API_KEY
echo   - CARTESIA_API_KEY
echo.

echo [OK] Setup complete!
echo.

pause
