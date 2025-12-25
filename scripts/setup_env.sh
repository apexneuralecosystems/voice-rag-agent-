#!/bin/bash
# ============================================
# Voice Agent RAG - Environment Setup Script
# ============================================
# This script helps set up environment files for deployment
# Usage: ./setup_env.sh

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_header() {
    echo -e "\n${BLUE}============================================${NC}"
    echo -e "${BLUE}  $1${NC}"
    echo -e "${BLUE}============================================${NC}"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

print_header "Voice Agent RAG - Environment Setup"

# Check if .env exists
if [ ! -f "$PROJECT_ROOT/.env" ]; then
    if [ -f "$PROJECT_ROOT/.env.example" ]; then
        cp "$PROJECT_ROOT/.env.example" "$PROJECT_ROOT/.env"
        print_success "Created .env from .env.example"
        print_warning "Please edit .env and add your API keys"
    else
        print_error ".env.example not found!"
        exit 1
    fi
else
    print_success ".env file exists"
fi

# Sync to frontend
if [ ! -f "$PROJECT_ROOT/frontend/.env.local" ]; then
    # Copy relevant variables for frontend
    echo "# Auto-generated from root .env" > "$PROJECT_ROOT/frontend/.env.local"
    grep -E "^LIVEKIT_" "$PROJECT_ROOT/.env" >> "$PROJECT_ROOT/frontend/.env.local" 2>/dev/null || true
    print_success "Created frontend/.env.local"
else
    print_success "frontend/.env.local exists"
fi

# Create logs directory
if [ ! -d "$PROJECT_ROOT/logs" ]; then
    mkdir -p "$PROJECT_ROOT/logs"
    print_success "Created logs directory"
else
    print_success "logs directory exists"
fi

# Create chat-engine-storage directory
if [ ! -d "$PROJECT_ROOT/chat-engine-storage" ]; then
    mkdir -p "$PROJECT_ROOT/chat-engine-storage"
    print_success "Created chat-engine-storage directory"
else
    print_success "chat-engine-storage directory exists"
fi

print_header "Environment Check Complete"

# Show required variables
echo ""
echo "Required environment variables in .env:"
echo "  - LIVEKIT_URL (e.g., wss://your-project.livekit.cloud)"
echo "  - LIVEKIT_API_KEY"
echo "  - LIVEKIT_API_SECRET"
echo "  - OPENROUTER_API_KEY"
echo "  - DEEPGRAM_API_KEY"
echo "  - CARTESIA_API_KEY"
echo ""

# Check if variables are set
MISSING=0
for var in LIVEKIT_URL LIVEKIT_API_KEY LIVEKIT_API_SECRET OPENROUTER_API_KEY DEEPGRAM_API_KEY CARTESIA_API_KEY; do
    value=$(grep "^$var=" "$PROJECT_ROOT/.env" 2>/dev/null | cut -d '=' -f2)
    if [ -z "$value" ] || [[ "$value" == your_* ]]; then
        print_warning "$var is not configured"
        MISSING=1
    else
        print_success "$var is configured"
    fi
done

if [ $MISSING -eq 1 ]; then
    echo ""
    print_warning "Some environment variables need to be configured"
    echo "Edit $PROJECT_ROOT/.env to add your API keys"
fi

echo ""
print_success "Setup complete!"
