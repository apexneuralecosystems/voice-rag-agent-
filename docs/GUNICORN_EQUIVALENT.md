# Quick Reference: Gunicorn-Equivalent Commands

## The Short Answer

**Instead of Gunicorn, use one of these methods:**

### ⭐ Method 1: Server Management Scripts (RECOMMENDED - Most Gunicorn-like)

These scripts provide the closest experience to using Gunicorn:

```bash
# First time setup - make scripts executable
chmod +x server_start.sh server_stop.sh server_restart.sh server_status.sh

# Start server in daemon mode (like: gunicorn app:app --daemon)
./server_start.sh

# Check server status (like: systemctl status gunicorn)
./server_status.sh

# Restart server (like: systemctl restart gunicorn)
./server_restart.sh

# Stop server (like: systemctl stop gunicorn)
./server_stop.sh
```

**Features:**
- ✓ Runs as background daemon
- ✓ PID file management
- ✓ Automatic logging to `logs/` directory
- ✓ Process status checking
- ✓ Graceful shutdown

### Method 2: Direct Command

**Development Mode (like `gunicorn --reload app:app`):**
```bash
python voice_agent_openai.py dev
```

**Production Mode (like `gunicorn app:app`):**
```bash
python voice_agent_openai.py start
```

### Method 3: PM2 Process Manager (like Gunicorn + Supervisor)
```bash
# Using PM2 (recommended for multi-process management)
pm2 start ecosystem.config.js

# Or directly:
pm2 start python --name "voice-agent" -- voice_agent_openai.py start
```

---

## Why Not Gunicorn?

This is a **LiveKit Worker Agent**, not a traditional WSGI/ASGI web application:
- **Gunicorn/Uvicorn** → For Flask, Django, FastAPI (HTTP servers)
- **This project** → LiveKit agent (WebRTC/real-time communication)

The LiveKit framework has its own process management built-in.

---

## Quick Comparison Table

| What You Need | Gunicorn Example | Voice Agent Command |
|---------------|------------------|---------------------|
| **Development** | `gunicorn --reload app:app` | `python voice_agent_openai.py dev` |
| **Production** | `gunicorn app:app` | `python voice_agent_openai.py start` |
| **With Workers** | `gunicorn -w 4 app:app` | `python voice_agent_openai.py start` (LiveKit handles concurrency) |
| **As Daemon** | `gunicorn -D app:app` | `pm2 start ecosystem.config.js` |
| **Systemd Service** | Create gunicorn.service | Use provided `voice-agent.service` |
| **Logs** | `--access-logfile` | Built-in logging + PM2/systemd logs |

---

## Platform-Specific Quick Start

### Windows Production
```bash
start_production.bat
```

### Linux/macOS Production
```bash
chmod +x start_production.sh
./start_production.sh
```

### Any Platform with PM2 (Recommended)
```bash
npm install -g pm2
pm2 start ecosystem.config.js
pm2 save
pm2 startup
```

---

## Most Common Production Setup

**What most people use (equivalent to Gunicorn in production):**

```bash
# 1. Install PM2
npm install -g pm2

# 2. Start the agent
pm2 start ecosystem.config.js

# 3. Save and auto-start on reboot
pm2 save
pm2 startup

# 4. Monitor
pm2 monit
```

That's it! Your agent is now running in production mode with auto-restart, log management, and monitoring.

---

## Need More Details?

See [DEPLOYMENT.md](./DEPLOYMENT.md) for comprehensive deployment guide.
