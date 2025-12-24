module.exports = {
  apps: [
    {
      name: "voiceai-api",
      script: "python",
      args: "voice_agent_openai.py start",
      cwd: require("path").join(process.cwd(), "backend"),
      interpreter: "none",
      env: {
        ENV: "production"
      },
      instances: 1,
      autorestart: true,
      watch: false,
      max_memory_restart: "1G",
      error_file: "./logs/backend-error.log",
      out_file: "./logs/backend-out.log",
      log_date_format: "YYYY-MM-DD HH:mm:ss Z",
      merge_logs: true
    },

    {
      name: "voiceai",
      script: "npm",
      args: "start",
      cwd: "./frontend",
      env: {
        NODE_ENV: "production",
        PORT: 8103,
        HOST: "0.0.0.0"
      },
      instances: 1,
      autorestart: true,
      watch: false,
      max_memory_restart: "512M",
      error_file: "./logs/frontend-error.log",
      out_file: "./logs/frontend-out.log",
      log_date_format: "YYYY-MM-DD HH:mm:ss Z",
      merge_logs: true
    }
  ]
};