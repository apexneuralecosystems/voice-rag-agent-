// ============================================
// Voice Agent RAG - PM2 Ecosystem Configuration
// ============================================
// Usage:
//   pm2 start deployment/ecosystem.config.js
//   pm2 logs
//   pm2 monit
//   pm2 save && pm2 startup

const path = require("path");

module.exports = {
  apps: [
    // ==========================================
    // Backend - LiveKit Voice Agent
    // ==========================================
    {
      name: "voiceai-backend",
      script: "python",
      args: "voice_agent_openai.py start",
      cwd: path.join(__dirname, "..", "backend"),
      interpreter: "none",

      // Environment
      env: {
        ENV: "production",
        PYTHONUNBUFFERED: "1",
        PYTHONDONTWRITEBYTECODE: "1"
      },

      // Process management
      instances: 1,
      autorestart: true,
      watch: false,
      max_restarts: 10,
      restart_delay: 5000,

      // Memory management
      max_memory_restart: "2G",

      // Logging
      error_file: path.join(__dirname, "..", "logs", "backend-error.log"),
      out_file: path.join(__dirname, "..", "logs", "backend-out.log"),
      log_date_format: "YYYY-MM-DD HH:mm:ss Z",
      merge_logs: true,

      // Startup
      wait_ready: true,
      listen_timeout: 60000,
      kill_timeout: 10000,
    },

    // ==========================================
    // Frontend - Next.js Application (Standalone Mode)
    // ==========================================
    {
      name: "voiceai-frontend",
      script: ".next/standalone/server.js",
      cwd: path.join(__dirname, "..", "frontend"),
      interpreter: "node",

      // Environment
      env: {
        NODE_ENV: "production",
        PORT: 8103,
        HOSTNAME: "0.0.0.0"
      },

      // Process management
      instances: 1,
      autorestart: true,
      watch: false,
      max_restarts: 10,
      restart_delay: 3000,

      // Memory management
      max_memory_restart: "512M",

      // Logging
      error_file: path.join(__dirname, "..", "logs", "frontend-error.log"),
      out_file: path.join(__dirname, "..", "logs", "frontend-out.log"),
      log_date_format: "YYYY-MM-DD HH:mm:ss Z",
      merge_logs: true,

      // Startup
      wait_ready: true,
      listen_timeout: 30000,
      kill_timeout: 5000,
    }
  ],

  // ==========================================
  // Deployment Configuration (Optional)
  // ==========================================
  deploy: {
    production: {
      user: "deploy",
      host: ["your-server.com"],
      ref: "origin/main",
      repo: "git@github.com:your-repo/voice-rag-agent.git",
      path: "/opt/voice-rag-agent",
      "pre-deploy-local": "",
      "post-deploy": "cd backend && pip install -r requirements.txt && cd ../frontend && npm install && npm run build && pm2 reload ecosystem.config.js --env production",
      "pre-setup": ""
    }
  }
};