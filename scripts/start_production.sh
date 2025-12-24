#!/bin/bash
# Production startup script for Voice Agent RAG backend
# This serves the same purpose as Gunicorn for traditional web apps

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
APP_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
BACKEND_DIR="$APP_DIR/backend"

echo "🚀 Starting Voice Agent in Production Mode..."

# Activate virtual environment if it exists
if [ -d "$APP_DIR/venv" ]; then
    echo "📦 Activating virtual environment..."
    source "$APP_DIR/venv/bin/activate"
fi

# Check if .env file exists
if [ ! -f "$APP_DIR/.env" ]; then
    echo "❌ Error: .env file not found!"
    echo "Please copy .env.example to .env and configure your API keys"
    exit 1
fi

# Load environment variables
export $(cat "$APP_DIR/.env" | grep -v '^#' | xargs)

# Change to backend directory and start
cd "$BACKEND_DIR"
echo "🎙️  Starting LiveKit Voice Agent..."
python voice_agent_openai.py start
