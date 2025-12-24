#!/bin/bash
# Server Production Deployment Script (Gunicorn-equivalent)
# Usage: ./server_start.sh [OPTIONS]
#
# This script provides Gunicorn-like server deployment for the Voice Agent backend
# Similar to: gunicorn app:app -b 0.0.0.0:8000 -w 4 --daemon

set -e

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
APP_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
VENV_DIR="$APP_DIR/venv"
LOG_DIR="$APP_DIR/logs"
PID_FILE="$LOG_DIR/voice-agent.pid"
ACCESS_LOG="$LOG_DIR/access.log"
ERROR_LOG="$LOG_DIR/error.log"
BACKEND_DIR="$APP_DIR/backend"

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Create logs directory if it doesn't exist
mkdir -p "$LOG_DIR"

echo -e "${GREEN}======================================${NC}"
echo -e "${GREEN}Voice Agent RAG - Server Deployment${NC}"
echo -e "${GREEN}(Gunicorn-equivalent for LiveKit)${NC}"
echo -e "${GREEN}======================================${NC}"

# Check if .env exists
if [ ! -f "$APP_DIR/.env" ]; then
    echo -e "${RED}Error: .env file not found!${NC}"
    echo "Please copy .env.example to .env and configure your API keys"
    exit 1
fi

# Activate virtual environment
if [ -d "$VENV_DIR" ]; then
    echo -e "${YELLOW}Activating virtual environment...${NC}"
    source "$VENV_DIR/bin/activate"
else
    echo -e "${YELLOW}Warning: Virtual environment not found at $VENV_DIR${NC}"
    echo "Proceeding without virtual environment activation"
fi

# Check if already running
if [ -f "$PID_FILE" ]; then
    OLD_PID=$(cat "$PID_FILE")
    if ps -p "$OLD_PID" > /dev/null 2>&1; then
        echo -e "${YELLOW}Voice Agent is already running with PID: $OLD_PID${NC}"
        echo "Use '$SCRIPT_DIR/server_stop.sh' to stop it first, or '$SCRIPT_DIR/server_restart.sh' to restart"
        exit 1
    else
        echo -e "${YELLOW}Removing stale PID file${NC}"
        rm -f "$PID_FILE"
    fi
fi

# Change to backend directory
cd "$BACKEND_DIR"

# Start the server in background (daemon mode)
echo -e "${GREEN}Starting Voice Agent in daemon mode...${NC}"
nohup python -u voice_agent_openai.py start >> "$ACCESS_LOG" 2>> "$ERROR_LOG" &
SERVER_PID=$!

# Save PID
echo $SERVER_PID > "$PID_FILE"

# Wait a moment to check if it started successfully
sleep 2

if ps -p $SERVER_PID > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Voice Agent started successfully!${NC}"
    echo -e "${GREEN}  PID: $SERVER_PID${NC}"
    echo -e "${GREEN}  Logs: $LOG_DIR${NC}"
    echo ""
    echo "Useful commands:"
    echo "  View logs:    tail -f $ACCESS_LOG"
    echo "  View errors:  tail -f $ERROR_LOG"
    echo "  Stop server:  $SCRIPT_DIR/server_stop.sh"
    echo "  Check status: $SCRIPT_DIR/server_status.sh"
else
    echo -e "${RED}✗ Failed to start Voice Agent${NC}"
    echo "Check error logs: cat $ERROR_LOG"
    rm -f "$PID_FILE"
    exit 1
fi
