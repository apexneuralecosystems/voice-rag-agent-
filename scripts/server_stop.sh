#!/bin/bash
# Stop the Voice Agent server
# Similar to: pkill -f gunicorn

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
APP_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
LOG_DIR="$APP_DIR/logs"
PID_FILE="$LOG_DIR/voice-agent.pid"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

if [ ! -f "$PID_FILE" ]; then
    echo -e "${YELLOW}PID file not found. Server may not be running.${NC}"
    echo "Attempting to find and kill any running voice agent processes..."
    pkill -f "voice_agent_openai.py" && echo -e "${GREEN}✓ Stopped voice agent processes${NC}" || echo -e "${YELLOW}No running processes found${NC}"
    exit 0
fi

PID=$(cat "$PID_FILE")

if ps -p "$PID" > /dev/null 2>&1; then
    echo -e "${YELLOW}Stopping Voice Agent (PID: $PID)...${NC}"
    kill "$PID"
    
    # Wait for process to stop
    for i in {1..10}; do
        if ! ps -p "$PID" > /dev/null 2>&1; then
            echo -e "${GREEN}✓ Voice Agent stopped successfully${NC}"
            rm -f "$PID_FILE"
            exit 0
        fi
        sleep 1
    done
    
    # Force kill if still running
    echo -e "${YELLOW}Process still running, forcing stop...${NC}"
    kill -9 "$PID" 2>/dev/null || true
    echo -e "${GREEN}✓ Voice Agent forcefully stopped${NC}"
    rm -f "$PID_FILE"
else
    echo -e "${YELLOW}Process not running (stale PID file)${NC}"
    rm -f "$PID_FILE"
fi
