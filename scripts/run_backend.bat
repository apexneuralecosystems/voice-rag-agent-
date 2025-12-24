@echo off
cd /d "%~dp0..\backend"
set REQUESTS_CA_BUNDLE=
set SSL_CERT_FILE=
python voice_agent_openai.py dev
