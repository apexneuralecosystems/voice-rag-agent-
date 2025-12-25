# Real-Time RAG Voice Agent

A real-time voice-powered RAG (Retrieval-Augmented Generation) agent built with [Cartesia](https://go.cartesia.ai/akshay) for speech synthesis, [Deepgram](https://deepgram.com/) for speech-to-text, and [OpenRouter](https://openrouter.ai/) for LLM capabilities.

## 🚀 Features

- Real-time voice interaction with RAG-powered responses
- Multiple implementation options for flexibility
- LiveKit integration for scalable real-time communication
- Production-ready deployment scripts
- Organized project structure

## 📁 Project Structure

```
Voice-Agent-RAG/
├── backend/           # Backend LiveKit agent application
├── frontend/          # Next.js web interface
├── scripts/           # Server management scripts
├── deployment/        # Production deployment configs (PM2, systemd)
├── docs/             # Documentation
├── logs/             # Application logs (generated)
└── chat-engine-storage/  # RAG vector storage (generated)
```

> 📘 **See [PROJECT_STRUCTURE.md](./PROJECT_STRUCTURE.md) for detailed folder organization**

## 📋 Prerequisites

Before you begin, ensure you have the following installed:
- **Python 3.11 or 3.12** (NOT 3.14 - see note below) - [Download here](https://www.python.org/)
- **Node.js 18 or later** - [Download here](https://nodejs.org/)
- **Git** - [Download here](https://git-scm.com/)

You'll also need API keys from:
- [Cartesia](https://go.cartesia.ai/akshay) - Voice synthesis
- [Deepgram](https://deepgram.com/) - Speech-to-text
- [LiveKit](https://livekit.io/) - Real-time communication
- [OpenRouter](https://openrouter.ai/) - LLM capabilities

## 🚀 Step-by-Step Setup Guide

Follow these steps to set up and run the project on a new system.

### Step 1: Clone the Repository
```bash
git clone <your-repository-url>
cd Voice-Agent-RAG
```

### Step 2: Set Up Python Virtual Environment
```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```
> **Note:** You should see `(venv)` in your terminal prompt, indicating the virtual environment is active.

### Step 3: Install Backend Dependencies
```bash
cd backend
pip install -r requirements.txt
cd ..
```

### Step 4: Configure Environment Variables
1. Copy the example environment file:
   ```bash
   # On Windows:
   copy .env.example .env
   
   # On macOS/Linux:
   cp .env.example .env
   ```

2. Edit `.env` file and add your API keys:
   ```env
   CARTESIA_API_KEY=your_cartesia_api_key
   LIVEKIT_URL=your_livekit_url
   LIVEKIT_API_KEY=your_livekit_api_key
   LIVEKIT_API_SECRET=your_livekit_api_secret
   OPENROUTER_API_KEY=your_openrouter_api_key
   DEEPGRAM_API_KEY=your_deepgram_api_key
   ```

### Step 5: Install Frontend Dependencies
```bash
cd frontend
npm install
cd ..
```

### Step 6: Start the Backend Agent
Open a terminal window and run:

**For Development (with auto-reload):**
```bash
# Option 1: Using the script (Windows)
scripts\run_backend.bat

# Option 2: Manual (Windows with Python 3.12)
cd backend
py -3.12 voice_agent_openai.py dev

# Option 3: Manual (Linux/macOS)
source venv/bin/activate
cd backend
python3.12 voice_agent_openai.py dev
```

> ⚠️ **Important:** You MUST use Python 3.11 or 3.12. Python 3.14 has compatibility issues with LiveKit packages.

**For Production:**
```bash
# Option 1: Using production script (recommended)
# Windows:
scripts\start_production.bat

# Linux/macOS:
chmod +x scripts/start_production.sh
scripts/start_production.sh

# Option 2: Manual
venv\Scripts\activate  # Windows
# source venv/bin/activate  # macOS/Linux
cd backend
python voice_agent_openai.py start
```

> **Note:** On Windows, if you encounter SSL certificate issues, you can use the provided batch file:
> ```bash
> run_backend.bat
> ```
> This automatically handles SSL certificate settings.

### Step 7: Start the Frontend UI
Open a **new** terminal window and run:
```bash
cd frontend
npm run dev
```

The frontend will typically be available at `http://localhost:3000` (check terminal output for exact URL).

## 🛠 Quick Reference Commands

### Backend Commands
| Command | Purpose |
|---------|---------|
| `cd backend && python voice_agent_openai.py dev` | Start backend in development mode (auto-reload) |
| `cd backend && python voice_agent_openai.py start` | Start backend in production mode |
| `scripts\run_backend.bat` | Start backend on Windows (handles SSL issues) |
| `scripts\start_production.bat` | **Production start script (Windows)** |
| `scripts/start_production.sh` | **Production start script (Linux/macOS)** |
| `scripts/server_start.sh` | **Start as daemon (Gunicorn-like)** |
| `scripts/server_stop.sh` | **Stop daemon server** |
| `scripts/server_restart.sh` | **Restart daemon server** |
| `scripts/server_status.sh` | **Check server status** |

### Frontend Commands
| Command | Purpose |
|---------|---------|
| `npm run dev` | Start frontend development server |
| `npm run build` | Build frontend for production |
| `npm start` | Start frontend production server |

### PM2 Production Commands (Gunicorn-equivalent)
| Command | Purpose |
|---------|---------|
| `pm2 start deployment/ecosystem.config.js` | Start both backend & frontend with PM2 |
| `pm2 start python --name "voice-agent" -- voice_agent_openai.py start` | Start backend only with PM2 |
| `pm2 list` | List all PM2 processes |
| `pm2 logs voice-agent` | View backend logs |
| `pm2 restart voice-agent` | Restart backend |
| `pm2 stop voice-agent` | Stop backend |
| `pm2 delete voice-agent` | Remove backend from PM2 |
| `pm2 monit` | Monitor all processes |
| `pm2 save` | Save current PM2 process list |

### Setup Commands Summary
```bash
# 1. Clone repository
git clone <your-repository-url>
cd Voice-Agent-RAG

# 2. Set up Python environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # macOS/Linux

# 3. Install backend dependencies
cd backend
pip install -r requirements.txt
cd ..

# 4. Configure environment
copy .env.example .env  # Windows
# cp .env.example .env  # macOS/Linux
# Then edit .env with your API keys

# 5. Install frontend dependencies
cd frontend
npm install
cd ..

# 6. Start backend (in one terminal) 
# Option 1: Using script
scripts\run_backend.bat  # Windows
# scripts/run_backend.sh  # Linux/macOS

# Option 2: Manual
cd backend
python voice_agent_openai.py dev

# 7. Start frontend (in another terminal)
cd frontend
npm run dev
```

## 🌐 Testing & Deployment

### Testing with LiveKit Playground
Connect your agent to the [LiveKit Agents Playground](https://agents-playground.livekit.io/) to test voice interactions.

### Production Deployment

> 📘 **For detailed production deployment instructions including Gunicorn-equivalent commands, see [docs/DEPLOYMENT.md](./docs/DEPLOYMENT.md)**

For production deployment, the LiveKit agent uses its own process management system. **Note:** This is a LiveKit worker agent, not a traditional web server, so Gunicorn/Uvicorn don't apply. Instead, use the following production-grade alternatives:

#### Option 1: Simple Production Start (Gunicorn-equivalent)

**Windows:**
```bash
# Use the production startup script
scripts\start_production.bat
```

**Linux/macOS:**
```bash
# Make the script executable
chmod +x scripts/start_production.sh

# Run the production script
scripts/start_production.sh
```

**Or directly:**
```bash
# Activate virtual environment
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/macOS

# Start in production mode
cd backend
python voice_agent_openai.py start
```

**Server Deployment (Gunicorn-equivalent for servers):**
```bash
# Linux/Ubuntu Server Production Command
cd /path/to/Voice-Agent-RAG/backend
source ../venv/bin/activate
nohup python voice_agent_openai.py start > ../logs/server.log 2>&1 &

# Or with explicit binding and logging (similar to gunicorn -b 0.0.0.0:8000)
nohup python -u voice_agent_openai.py start >> ../logs/server.log 2>&1 &

# Check if it's running
ps aux | grep voice_agent

# View logs
tail -f ../logs/server.log
```

**Windows Server:**
```powershell
# Run in background
Start-Process -NoNewWindow -FilePath "python" -ArgumentList "voice_agent_openai.py","start" -RedirectStandardOutput "logs\server.log" -RedirectStandardError "logs\error.log"

# Or use the batch script
start /B scripts\start_production.bat
```

**Server Management Scripts (Recommended - Gunicorn-like interface):**

We've provided server management scripts that mimic Gunicorn/systemd commands:

```bash
# Make scripts executable (first time only)
chmod +x scripts/server_start.sh scripts/server_stop.sh scripts/server_restart.sh scripts/server_status.sh

# Start server (similar to: gunicorn app:app --daemon)
scripts/server_start.sh

# Check status (similar to: systemctl status gunicorn)
scripts/server_status.sh

# Stop server (similar to: systemctl stop gunicorn)
scripts/server_stop.sh

# Restart server (similar to: systemctl restart gunicorn)
scripts/server_restart.sh
```

These scripts provide:
- ✓ Daemon mode (background process)
- ✓ PID file management
- ✓ Automatic logging to `logs/` directory
- ✓ Process monitoring
- ✓ Graceful shutdown

#### Option 2: PM2 Process Manager (Recommended for Production)

PM2 provides process management similar to Gunicorn + Supervisor:

```bash
# Install PM2 globally
npm install -g pm2

# Start the backend with PM2
pm2 start python --name "voice-agent" -- voice_agent_openai.py start

# Start frontend with PM2
cd frontend
pm2 start npm --name "voice-agent-frontend" -- start

# View logs
pm2 logs voice-agent

# Monitor processes
pm2 monit

# Setup PM2 to restart on system reboot
pm2 startup
pm2 save
```

**PM2 Ecosystem File** (`deployment/ecosystem.config.js`):
```javascript
module.exports = {
  apps: [
    {
      name: 'voice-agent-backend',
      script: 'python',
      args: 'voice_agent_openai.py start',
      cwd: require('path').join(process.cwd(), 'backend'),
      interpreter: 'none',
      env: {
        NODE_ENV: 'production',
      },
      error_file: './logs/backend-error.log',
      out_file: './logs/backend-out.log',
      log_date_format: 'YYYY-MM-DD HH:mm:ss Z',
    },
    {
      name: 'voice-agent-frontend',
      script: 'npm',
      args: 'start',
      cwd: '/path/to/Voice-Agent-RAG/frontend',
      env: {
        NODE_ENV: 'production',
      },
    },
  ],
};
```

Then run: `pm2 start deployment/ecosystem.config.js`

#### Option 3: Systemd Service (Linux Production)

For Linux servers, use systemd (equivalent to running Gunicorn as a service):

1. **Edit the service file** `deployment/voice-agent.service`:
   ```ini
   [Unit]
   Description=Voice Agent RAG - LiveKit Worker
   After=network.target

   [Service]
   Type=simple
   User=youruser
   WorkingDirectory=/path/to/Voice-Agent-RAG/backend
   Environment="PATH=/path/to/Voice-Agent-RAG/venv/bin"
   ExecStart=/path/to/Voice-Agent-RAG/venv/bin/python voice_agent_openai.py start
   Restart=always
   RestartSec=10

   [Install]
   WantedBy=multi-user.target
   ```

2. **Install and start the service**:
   ```bash
   # Copy service file
   sudo cp deployment/voice-agent.service /etc/systemd/system/

   # Reload systemd
   sudo systemctl daemon-reload

   # Enable service to start on boot
   sudo systemctl enable voice-agent

   # Start the service
   sudo systemctl start voice-agent

   # Check status
   sudo systemctl status voice-agent

   # View logs
   sudo journalctl -u voice-agent -f
   ```

#### Option 4: Docker Deployment

Create a `Dockerfile`:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose ports (if needed)
# EXPOSE 8000

# Run the agent
CMD ["python", "voice_agent_openai.py", "start"]
```

Create `docker-compose.yml`:
```yaml
version: '3.8'

services:
  backend:
    build: .
    container_name: voice-agent-backend
    env_file: .env
    restart: unless-stopped
    volumes:
      - ./chat-engine-storage:/app/chat-engine-storage
      - ./docs:/app/docs

  frontend:
    build: ./frontend
    container_name: voice-agent-frontend
    ports:
      - "3000:3000"
    restart: unless-stopped
    depends_on:
      - backend
```

Run with Docker:
```bash
# Build and start
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

### 🔄 Production Checklist

- [ ] All API keys configured in `.env`
- [ ] Virtual environment activated
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Frontend built (`cd frontend && npm run build`)
- [ ] Process manager configured (PM2/systemd/Docker)
- [ ] Logs directory created
- [ ] Firewall rules configured (if applicable)
- [ ] Auto-restart on failure enabled
- [ ] Monitoring setup (optional)

## 🔧 Troubleshooting

### Common Setup Issues

#### SSL Certificate Issues (Windows)
If you encounter SSL certificate errors, use the `run_backend.bat` file which automatically sets:
```batch
set REQUESTS_CA_BUNDLE=
set SSL_CERT_FILE=
```

#### Port Already in Use
If you get a "port already in use" error:
- Frontend: Check and kill any process using port 8103
- Backend: Check the LiveKit agent configuration for port settings

```bash
# Windows - Find and kill process on port
netstat -ano | findstr :8103
taskkill /PID <PID> /F

# Linux/macOS
lsof -i :8103
kill -9 <PID>
```

#### Virtual Environment Not Activating
Make sure you're in the project root directory and the `venv` folder exists. Recreate if necessary:
```bash
rmdir /s venv  # Windows
# rm -rf venv  # macOS/Linux
python -m venv venv
```

#### Python 3.14 Compatibility Issues
**Error:** `AttributeError` when importing LiveKit plugins (silero, deepgram, etc.)

**Cause:** Python 3.14 has namespace package issues with LiveKit plugins.

**Solution:** Use Python 3.11 or 3.12 instead:
```bash
# Windows - use py launcher to select version
py -3.12 voice_agent_openai.py dev

# Linux/macOS - install Python 3.12
sudo apt install python3.12 python3.12-venv  # Ubuntu/Debian
python3.12 -m venv venv
source venv/bin/activate
```

#### Agent Not Speaking / No Audio Output
**Symptoms:** 
- Frontend shows "NEURAL LINK ONLINE" but agent doesn't greet
- Console shows `trackID: undefined`

**Causes & Solutions:**
1. **Backend not receiving jobs**: Verify `agent: true` is in the token grant (`frontend/app/api/token/route.ts`)
2. **Wrong Python version**: Use Python 3.11 or 3.12, not 3.14
3. **LiveKit Agents API mismatch**: Ensure code uses `AgentSession.start()` pattern (already fixed in current codebase)

---

## 🚨 Server Deployment Errors & Solutions

### 1. LiveKit Connection Errors

#### Error: `Failed to connect to LiveKit server`
**Cause:** Invalid LiveKit credentials or network issues.
**Solution:**
```bash
# Verify your .env file has correct values:
LIVEKIT_URL=wss://your-project.livekit.cloud  # Must start with wss://
LIVEKIT_API_KEY=your_api_key
LIVEKIT_API_SECRET=your_api_secret

# Test connectivity
curl -I https://your-project.livekit.cloud
```

#### Error: `WebSocket connection failed`
**Cause:** Firewall blocking WebSocket connections.
**Solution:**
```bash
# Allow outbound connections on ports 443, 7880-7881
sudo ufw allow out 443/tcp
sudo ufw allow out 7880:7881/tcp
```

---

### 2. Python/Dependency Errors

#### Error: `ModuleNotFoundError: No module named 'livekit'`
**Cause:** Dependencies not installed or wrong Python environment.
**Solution:**
```bash
# Ensure virtual environment is active
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# Reinstall dependencies
pip install -r backend/requirements.txt
```

#### Error: `livekit.agents.voice.Agent not found`
**Cause:** Old LiveKit Agents version (needs 1.0+).
**Solution:**
```bash
pip install --upgrade livekit-agents>=1.0.0
```

#### Error: `SSL: CERTIFICATE_VERIFY_FAILED`
**Cause:** SSL certificate issues, common on Windows.
**Solution:**
```bash
# Install certifi
pip install certifi

# Or set environment variables
export SSL_CERT_FILE=$(python -c "import certifi; print(certifi.where())")
export REQUESTS_CA_BUNDLE=$(python -c "import certifi; print(certifi.where())")
```

---

### 3. Memory & Resource Errors

#### Error: `MemoryError` or `Killed`
**Cause:** HuggingFace embedding model requires ~2GB RAM.
**Solution:**
```bash
# Check available memory
free -h  # Linux
Get-Process | Sort-Object WorkingSet -Descending | Select-Object -First 5  # Windows

# Add swap space (Linux)
sudo fallocate -l 4G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

#### Error: `torch.cuda.OutOfMemoryError`
**Cause:** GPU memory exhausted (if using CUDA).
**Solution:**
```python
# Force CPU-only mode in voice_agent_openai.py
import os
os.environ["CUDA_VISIBLE_DEVICES"] = ""
```

---

### 4. API Key & Authentication Errors

#### Error: `401 Unauthorized` from OpenRouter/Cartesia/Deepgram
**Cause:** Invalid or expired API keys.
**Solution:**
```bash
# Verify API keys are set correctly
cat .env | grep API_KEY

# Test API key directly
curl -H "Authorization: Bearer $OPENROUTER_API_KEY" https://openrouter.ai/api/v1/models
```

#### Error: `CARTESIA_API_KEY is not set`
**Cause:** Environment variables not loaded.
**Solution:**
```bash
# Ensure .env file exists in project root
ls -la .env

# Source the .env file manually
export $(cat .env | xargs)
```

---

### 5. Frontend Build/Runtime Errors

#### Error: `ENOENT: no such file or directory, open '.env.local'`
**Cause:** Missing frontend environment file.
**Solution:**
```bash
cd frontend
cp ../.env .env.local
# Or create with required variables:
echo "LIVEKIT_API_KEY=your_key" > .env.local
echo "LIVEKIT_API_SECRET=your_secret" >> .env.local
echo "LIVEKIT_URL=your_url" >> .env.local
```

#### Error: `Error: listen EADDRINUSE: address already in use :::8103`
**Cause:** Port 8103 is already in use.
**Solution:**
```bash
# Find and kill the process
# Linux/macOS
lsof -ti:8103 | xargs kill -9

# Windows
netstat -ano | findstr :8103
taskkill /PID <PID> /F
```

---

### 6. PM2/Process Manager Errors

#### Error: `pm2: command not found`
**Cause:** PM2 not installed globally.
**Solution:**
```bash
npm install -g pm2
```

#### Error: `[PM2] Spawning PM2 daemon with pm2_home`
**Cause:** PM2 daemon starting for first time (not an error).
**Solution:** This is normal. PM2 creates its daemon on first run.

#### Error: `Script not found`
**Cause:** Wrong working directory in PM2 config.
**Solution:**
```bash
# Edit deployment/ecosystem.config.js
# Ensure cwd paths are correct for your server

# Or start manually with absolute paths
pm2 start /full/path/to/backend/voice_agent_openai.py --interpreter python
```

---

### 7. Systemd Service Errors

#### Error: `Failed to start voice-agent.service: Unit not found`
**Cause:** Service file not copied to systemd.
**Solution:**
```bash
sudo cp deployment/voice-agent.service /etc/systemd/system/
sudo systemctl daemon-reload
```

#### Error: `Main process exited, code=exited, status=1/FAILURE`
**Cause:** Python script error or missing dependencies.
**Solution:**
```bash
# Check logs
sudo journalctl -u voice-agent -n 50

# Test manually first
cd /path/to/project/backend
source ../venv/bin/activate
python voice_agent_openai.py dev
```

---

### 8. Network & Firewall Issues

#### Error: `Connection refused` or `Connection timed out`
**Cause:** Firewall blocking connections.
**Solution:**
```bash
# Linux - Open required ports
sudo ufw allow 8103/tcp  # Frontend
sudo ufw allow 443/tcp   # HTTPS/WSS

# Check firewall status
sudo ufw status
```

#### Error: `CORS policy: No 'Access-Control-Allow-Origin'`
**Cause:** Frontend and backend on different origins.
**Solution:** Configure your reverse proxy (Nginx) to handle CORS:
```nginx
location /api {
    add_header 'Access-Control-Allow-Origin' '*';
    add_header 'Access-Control-Allow-Methods' 'GET, POST, OPTIONS';
}
```

---

### 9. Docker Deployment Errors

#### Error: `Cannot connect to the Docker daemon`
**Cause:** Docker service not running.
**Solution:**
```bash
# Start Docker
sudo systemctl start docker

# Or on Windows/macOS, start Docker Desktop
```

#### Error: `ERROR: for backend  Cannot start service`
**Cause:** Build failed or missing environment variables.
**Solution:**
```bash
# Rebuild with no cache
docker-compose build --no-cache

# Check .env file exists
docker-compose config
```

---

### 10. Quick Diagnostic Commands

```bash
# Check if backend is running
ps aux | grep voice_agent  # Linux/macOS
tasklist | findstr python  # Windows

# Check ports in use
netstat -tulpn | grep LISTEN  # Linux
netstat -ano | findstr LISTENING  # Windows

# Test LiveKit connectivity
curl -v wss://your-project.livekit.cloud

# Check Python version
python --version  # Should be 3.11+

# Check Node.js version
node --version   # Should be 18+

# View PM2 logs
pm2 logs --lines 100

# View systemd logs
sudo journalctl -u voice-agent -f

# Check disk space
df -h  # Linux
Get-PSDrive  # Windows
```

---

## 📚 Additional Resources

### Project Documentation
- [Project Structure](./PROJECT_STRUCTURE.md) - Detailed folder organization
- [Deployment Guide](./docs/DEPLOYMENT.md) - Comprehensive deployment instructions
- [Server Commands](./docs/SERVER_COMMANDS.md) - Production server command reference
- [Gunicorn Equivalent](./docs/GUNICORN_EQUIVALENT.md) - Gunicorn comparison guide

### External APIs & Tools
- [LiveKit Documentation](https://docs.livekit.io/)
- [Cartesia API Docs](https://docs.cartesia.ai/)
- [Deepgram API Docs](https://developers.deepgram.com/)
- [OpenRouter Documentation](https://openrouter.ai/docs)
- [PM2 Process Manager](https://pm2.keymetrics.io/)

---

**Made with ❤️ using LiveKit, Cartesia, Deepgram, and OpenRouter**
