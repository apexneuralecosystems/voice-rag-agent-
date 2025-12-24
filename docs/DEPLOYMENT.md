# Production Deployment Guide - Gunicorn Equivalents

This document explains how to deploy the Voice Agent RAG backend in production, similar to how you would use Gunicorn for traditional web applications.

## Important Note

This is a **LiveKit Worker Agent**, not a traditional WSGI/ASGI web server. Therefore, Gunicorn and Uvicorn don't apply. However, we provide equivalent production-grade deployment methods below.

## Quick Start (Simplest Method)

### Windows
```bash
start_production.bat
```

### Linux/macOS
```bash
chmod +x start_production.sh
./start_production.sh
```

## Production Deployment Options

### 1. Direct Command (Like `gunicorn app:app`)

**Development:**
```bash
python voice_agent_openai.py dev
```

**Production (equivalent to running Gunicorn):**
```bash
python voice_agent_openai.py start
```

### 2. PM2 (Recommended - Like Gunicorn + Supervisor)

PM2 provides:
- Process management
- Auto-restart on failure
- Load balancing (if needed)
- Log management
- Monitoring

**Install PM2:**
```bash
npm install -g pm2
```

**Quick Start:**
```bash
# Start backend with PM2
pm2 start python --name "voice-agent" -- voice_agent_openai.py start

# Start with ecosystem file (recommended)
pm2 start ecosystem.config.js

# Monitor
pm2 monit

# View logs
pm2 logs voice-agent

# Auto-start on system boot
pm2 startup
pm2 save
```

**Common PM2 Commands:**
```bash
pm2 list              # List all processes
pm2 restart voice-agent   # Restart the agent
pm2 stop voice-agent      # Stop the agent
pm2 delete voice-agent    # Remove from PM2
pm2 logs --lines 100      # View last 100 log lines
```

### 3. Systemd (Linux - Like Gunicorn Service)

**Setup:**
```bash
# 1. Edit voice-agent.service with your paths
# 2. Copy to systemd
sudo cp voice-agent.service /etc/systemd/system/

# 3. Reload and enable
sudo systemctl daemon-reload
sudo systemctl enable voice-agent

# 4. Start the service
sudo systemctl start voice-agent
```

**Management:**
```bash
sudo systemctl status voice-agent   # Check status
sudo systemctl restart voice-agent  # Restart
sudo systemctl stop voice-agent     # Stop
sudo journalctl -u voice-agent -f   # View logs
```

### 4. Docker (Containerized Deployment)

**Build and run:**
```bash
docker-compose up -d
```

**Management:**
```bash
docker-compose logs -f        # View logs
docker-compose restart        # Restart
docker-compose down          # Stop
```

## Comparison with Gunicorn

| Gunicorn Command | Voice Agent Equivalent |
|-----------------|------------------------|
| `gunicorn app:app` | `python voice_agent_openai.py start` |
| `gunicorn app:app --workers 4` | Not applicable (LiveKit manages concurrency) |
| `gunicorn app:app --daemon` | `pm2 start ecosystem.config.js` |
| `gunicorn app:app --reload` | `python voice_agent_openai.py dev` |
| Running as systemd service | Use provided `voice-agent.service` |

## Production Checklist

Before deploying to production:

- [ ] Set all API keys in `.env` file
- [ ] Test locally with `python voice_agent_openai.py dev`
- [ ] Choose a deployment method (PM2 recommended)
- [ ] Configure auto-restart on failure
- [ ] Set up log rotation
- [ ] Configure firewall (if applicable)
- [ ] Test connection to LiveKit
- [ ] Monitor logs for errors

## Recommended Setup for Different Environments

### Small Deployment (VPS/Single Server)
**Use PM2:**
```bash
pm2 start ecosystem.config.js
pm2 save
pm2 startup
```

### Linux Production Server
**Use Systemd:**
```bash
sudo systemctl enable voice-agent
sudo systemctl start voice-agent
```

### Cloud/Container Environment
**Use Docker:**
```bash
docker-compose up -d
```

### Development
**Use built-in dev mode:**
```bash
python voice_agent_openai.py dev
```

## Monitoring and Logs

### PM2
```bash
pm2 monit              # Real-time monitoring
pm2 logs voice-agent   # Live logs
```

### Systemd
```bash
sudo journalctl -u voice-agent -f
```

### Docker
```bash
docker-compose logs -f backend
```

## Environment Variables

Required in `.env`:
```env
CARTESIA_API_KEY=your_key
LIVEKIT_URL=wss://your-livekit-url
LIVEKIT_API_KEY=your_key
LIVEKIT_API_SECRET=your_secret
OPENROUTER_API_KEY=your_key
DEEPGRAM_API_KEY=your_key
```

## Troubleshooting

### Process Won't Start
```bash
# Check logs
pm2 logs voice-agent --lines 50

# Check environment
python voice_agent_openai.py dev  # Test in dev mode
```

### SSL Certificate Issues (Windows)
Use `start_production.bat` instead of direct Python command.

### Port Already in Use
Check and kill any existing process:
```bash
# Find process
lsof -i :PORT_NUMBER  # Linux/macOS
netstat -ano | findstr :PORT  # Windows

# Kill process
kill -9 PID  # Linux/macOS
taskkill /PID pid /F  # Windows
```

## Need Help?

- Check the main [README.md](./README.md)
- LiveKit Documentation: https://docs.livekit.io/
- PM2 Documentation: https://pm2.keymetrics.io/
