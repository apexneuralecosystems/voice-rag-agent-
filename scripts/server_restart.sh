#!/bin/bash
# Restart the Voice Agent server
# Similar to: systemctl restart gunicorn

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Colors
GREEN='\033[0;32m'
NC='\033[0m'

echo -e "${GREEN}Restarting Voice Agent...${NC}"

# Stop the server
"$SCRIPT_DIR/server_stop.sh"

# Wait a moment
sleep 2

# Start the server
"$SCRIPT_DIR/server_start.sh"
