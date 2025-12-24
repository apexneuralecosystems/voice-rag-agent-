# Voice Agent RAG - Project Structure

This document describes the organization of the Voice Agent RAG project.

## 📁 Directory Structure

```
Voice-Agent-RAG/
├── backend/                    # Backend application code
│   ├── voice_agent_openai.py  # Main LiveKit agent implementation
│   ├── requirements.txt        # Python dependencies
│   └── __init__.py            # Backend package initializer
│
├── frontend/                   # Next.js frontend application
│   ├── app/                   # Next.js app directory
│   ├── public/                # Static assets
│   ├── package.json           # Node.js dependencies
│   └── ...                    # Other Next.js files
│
├── scripts/                    # Deployment and utility scripts
│   ├── server_start.sh        # Start server as daemon (Linux/macOS)
│   ├── server_stop.sh         # Stop daemon server
│   ├── server_restart.sh      # Restart daemon server
│   ├── server_status.sh       # Check server status
│   ├── start_production.sh    # Production startup (Linux/macOS)
│   ├── start_production.bat   # Production startup (Windows)
│   └── run_backend.bat        # Development startup (Windows)
│
├── deployment/                 # Production deployment configurations
│   ├── ecosystem.config.js    # PM2 process manager config
│   └── voice-agent.service    # Systemd service file
│
├── docs/                       # Documentation
│   ├── DEPLOYMENT.md          # Full deployment guide
│   ├── SERVER_COMMANDS.md     # Server command reference
│   ├── GUNICORN_EQUIVALENT.md # Gunicorn comparison guide
│   └── DeepSeek.pdf          # Additional documentation
│
├── chat-engine-storage/        # RAG index storage (generated)
│   ├── docstore.json
│   ├── index_store.json
│   └── *_vector_store.json
│
├── logs/                       # Application logs (generated)
│   ├── access.log
│   ├── error.log
│   └── voice-agent.pid
│
├── .env                        # Environment variables (not in git)
├── .env.example               # Environment template
├── .gitignore                 # Git ignore rules
└── README.md                  # Main project documentation
```

## 📂 Directory Descriptions

### `/backend`
Contains the core LiveKit voice agent application.
- **Main file**: `voice_agent_openai.py` - LiveKit agent with RAG capabilities
- **Dependencies**: `requirements.txt` - Python packages (LiveKit, LlamaIndex, OpenAI, etc.)

### `/frontend`
Next.js-based web interface for the voice agent.
- Built with Next.js 14+ and TypeScript
- Provides UI for interacting with the LiveKit agent

### `/scripts`
Executable scripts for running and managing the application.
- **Server management**: `server_*.sh` - Daemon-style server control (Gunicorn-equivalent)
- **Production**: `start_production.*` - Simple production startup
- **Development**: `run_backend.bat` - Quick development startup

### `/deployment`
Production deployment configuration files.
- **PM2**: `ecosystem.config.js` - Process manager configuration
- **Systemd**: `voice-agent.service` - Linux service definition

### `/docs`
Comprehensive project documentation.
- **DEPLOYMENT.md**: Complete deployment instructions
- **SERVER_COMMANDS.md**: Server command reference
- **GUNICORN_EQUIVALENT.md**: Gunicorn comparison for traditional web devs

### `/chat-engine-storage` (Generated)
Stores the RAG vector index and document store.
- Created automatically on first run
- Contains embeddings and indexed documents

### `/logs` (Generated)
Application logs and process management files.
- Created when using server management scripts
- Contains PID files for process tracking

## 🔄 File Relationships

```
Backend Startup Flow:
.env → backend/voice_agent_openai.py → LiveKit → Chat Engine

Frontend Startup Flow:
frontend/package.json → Next.js → localhost:3000

Production Deployment:
deployment/ecosystem.config.js → PM2 → backend/voice_agent_openai.py
OR
deployment/voice-agent.service → systemd → backend/voice_agent_openai.py
```

## 🚀 Quick Navigation

### To run the application:
- Development: `scripts/run_backend.bat` (Windows) or `cd backend && python voice_agent_openai.py dev`
- Production: `scripts/server_start.sh` (daemon mode) or `scripts/start_production.sh`

### To deploy:
1. Use PM2: `pm2 start deployment/ecosystem.config.js`
2. Use systemd: Copy `deployment/voice-agent.service` to `/etc/systemd/system/`

### To read documentation:
- **Getting Started**: `README.md`
- **Deployment**: `docs/DEPLOYMENT.md`
- **Server Commands**: `docs/SERVER_COMMANDS.md`

## 📝 Notes

- All scripts in `/scripts` are relative-path aware and can be run from anywhere
- The `/backend` directory is the working directory for the Python application
- Environment variables in `.env` are loaded automatically by scripts
- Logs are stored in `/logs` when using daemon mode

## 🔐 Files Not in Git

The following are excluded via `.gitignore`:
- `.env` - Contains sensitive API keys
- `venv/` - Python virtual environment
- `logs/` - Runtime logs
- `chat-engine-storage/` - Generated RAG index
- `node_modules/` - Node.js dependencies
- `frontend/.next/` - Next.js build files
