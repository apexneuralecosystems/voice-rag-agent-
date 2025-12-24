# 🚀 SERVER DEPLOYMENT COMMANDS - GUNICORN EQUIVALENT

## ⭐ THE ANSWER YOU'RE LOOKING FOR

### For Linux/Ubuntu Server (Production):

```bash
# Quick Start - Use our server management scripts
chmod +x server_start.sh
./server_start.sh
```

This runs the backend as a daemon (background process) with logging, just like Gunicorn!

---

## 📋 Complete Server Command Reference

### Start Server (Gunicorn equivalent)

**Option 1: Server Script (RECOMMENDED)**
```bash
./server_start.sh
```
- Runs in background (daemon mode)
- Creates PID file for management
- Logs to `logs/access.log` and `logs/error.log`
- **This is your Gunicorn equivalent!**

**Option 2: Manual daemon start**
```bash
cd /path/to/Voice-Agent-RAG
source venv/bin/activate
nohup python -u voice_agent_openai.py start >> logs/server.log 2>&1 &
```

**Option 3: Simple production start**
```bash
python voice_agent_openai.py start
```
(Runs in foreground - use screen/tmux or the scripts above for background)

---

### Manage Server

```bash
# Check if server is running
./server_status.sh

# Stop the server
./server_stop.sh

# Restart the server
./server_restart.sh

# View logs in real-time
tail -f logs/access.log
tail -f logs/error.log
```

---

## 🔄 Gunicorn Commands → Voice Agent Equivalent

| What You Want | Gunicorn Command | Voice Agent Equivalent |
|--------------|------------------|------------------------|
| **Start server** | `gunicorn app:app` | `./server_start.sh` or `python voice_agent_openai.py start` |
| **Start as daemon** | `gunicorn app:app --daemon` | `./server_start.sh` |
| **With workers** | `gunicorn app:app -w 4` | Not needed (LiveKit handles concurrency) |
| **Bind to address** | `gunicorn app:app -b 0.0.0.0:8000` | Not applicable (LiveKit manages connections) |
| **Check status** | `systemctl status gunicorn` | `./server_status.sh` |
| **Stop server** | `systemctl stop gunicorn` | `./server_stop.sh` |
| **Restart** | `systemctl restart gunicorn` | `./server_restart.sh` |
| **View logs** | `tail -f /var/log/gunicorn/access.log` | `tail -f logs/access.log` |
| **Reload** | `systemctl reload gunicorn` | `./server_restart.sh` |
| **Development** | `gunicorn app:app --reload` | `python voice_agent_openai.py dev` |

---

## 🖥️ Platform-Specific Commands

### Linux/Ubuntu Server
```bash
# Start
./server_start.sh

# Or with nohup:
nohup python voice_agent_openai.py start > logs/server.log 2>&1 &
```

### Windows Server
```powershell
# Start in background
Start-Process -NoNewWindow -FilePath "python" -ArgumentList "voice_agent_openai.py","start" -RedirectStandardOutput "logs\server.log" -RedirectStandardError "logs\error.log"

# Or use the batch file
start_production.bat
```

### Using PM2 (Works on all platforms)
```bash
npm install -g pm2
pm2 start ecosystem.config.js
pm2 save
```

---

## 📁 Server Management Scripts Overview

We provide 4 scripts that mimic traditional server management:

1. **`server_start.sh`** - Start the server as a daemon
2. **`server_stop.sh`** - Stop the server gracefully
3. **`server_restart.sh`** - Restart the server
4. **`server_status.sh`** - Check if server is running

### First Time Setup:
```bash
chmod +x server_start.sh server_stop.sh server_restart.sh server_status.sh
```

### Usage:
```bash
./server_start.sh    # Start
./server_status.sh   # Check status
./server_restart.sh  # Restart
./server_stop.sh     # Stop
```

---

## 🔧 Typical Server Deployment

Here's a typical deployment flow on a production server:

```bash
# 1. Clone repository
git clone <your-repo-url>
cd Voice-Agent-RAG

# 2. Setup Python environment
python3 -m venv venv
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
cp .env.example .env
nano .env  # Add your API keys

# 5. Make scripts executable
chmod +x server_start.sh server_stop.sh server_restart.sh server_status.sh

# 6. Create logs directory
mkdir -p logs

# 7. Start the server
./server_start.sh

# 8. Check it's running
./server_status.sh
```

---

## ⚙️ Advanced: Systemd Service (Like Gunicorn Service)

For production Linux servers, use systemd for automatic startup:

### Setup:
```bash
# 1. Edit the service file with your paths
# 2. Copy to systemd
sudo cp voice-agent.service /etc/systemd/system/

# 3. Enable and start
sudo systemctl daemon-reload
sudo systemctl enable voice-agent
sudo systemctl start voice-agent
```

### Manage:
```bash
sudo systemctl status voice-agent    # Check status
sudo systemctl restart voice-agent   # Restart
sudo systemctl stop voice-agent      # Stop
sudo journalctl -u voice-agent -f    # View logs
```

---

## 📊 Monitoring

### View Logs:
```bash
# Real-time access log
tail -f logs/access.log

# Real-time error log
tail -f logs/error.log

# Last 100 lines
tail -n 100 logs/access.log
```

### Check Process:
```bash
# Using our script
./server_status.sh

# Manual check
ps aux | grep voice_agent_openai

# Check with PID file
cat logs/voice-agent.pid
```

---

## 🆘 Troubleshooting

### Server won't start?
```bash
# Check error logs
cat logs/error.log

# Check if .env exists
ls -la .env

# Try running in foreground to see errors
python voice_agent_openai.py start
```

### Server not stopping?
```bash
# Force stop all voice agent processes
pkill -f voice_agent_openai

# Remove stale PID file
rm -f logs/voice-agent.pid
```

### Port already in use?
```bash
# Find process using the port
lsof -i :PORT_NUMBER

# Kill specific process
kill -9 PID
```

---

## 🎯 Summary

**For a production server, use:**
```bash
./server_start.sh  # This is your "gunicorn app:app --daemon" equivalent
```

**That's it!** All the complexity of daemon mode, PID management, and logging is handled for you.

---

## 📚 More Information

- Full deployment guide: [DEPLOYMENT.md](./DEPLOYMENT.md)
- Quick reference: [GUNICORN_EQUIVALENT.md](./GUNICORN_EQUIVALENT.md)
- Main README: [README.md](./README.md)
