#!/bin/bash
# Check Voice Agent server status
# Similar to: systemctl status gunicorn

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

echo "========================================"
echo "Voice Agent Server Status"
echo "========================================"

if [ ! -f "$PID_FILE" ]; then
    echo -e "${RED}Status: NOT RUNNING${NC}"
    echo "PID file not found: $PID_FILE"
    exit 1
fi

PID=$(cat "$PID_FILE")

if ps -p "$PID" > /dev/null 2>&1; then
    echo -e "${GREEN}Status: RUNNING${NC}"
    echo "PID: $PID"
    echo ""
    echo "Process details:"
    ps -p "$PID" -o pid,ppid,%cpu,%mem,etime,cmd
    echo ""
    echo "Log files:"
    echo "  Access: $LOG_DIR/access.log"
    echo "  Error:  $LOG_DIR/error.log"
else
    echo -e "${RED}Status: NOT RUNNING (stale PID file)${NC}"
    echo "Stale PID: $PID"
    exit 1
fi
