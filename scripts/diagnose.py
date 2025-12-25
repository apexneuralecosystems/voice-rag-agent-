#!/usr/bin/env python3
"""
Voice Agent RAG - Deployment Diagnostic Script
Run this script to check if your deployment is properly configured.
"""

import os
import sys
import subprocess
import socket
from pathlib import Path

# Colors for output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def print_header(text):
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}  {text}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.RESET}")

def print_check(name, passed, details=""):
    status = f"{Colors.GREEN}✓ PASS{Colors.RESET}" if passed else f"{Colors.RED}✗ FAIL{Colors.RESET}"
    print(f"  {status} - {name}")
    if details and not passed:
        print(f"         {Colors.YELLOW}→ {details}{Colors.RESET}")

def print_warning(text):
    print(f"  {Colors.YELLOW}⚠ WARNING: {text}{Colors.RESET}")

def print_info(text):
    print(f"  {Colors.BLUE}ℹ {text}{Colors.RESET}")

def check_python_version():
    """Check Python version is 3.11+"""
    version = sys.version_info
    passed = version.major == 3 and version.minor >= 11
    print_check(
        f"Python version ({version.major}.{version.minor}.{version.micro})",
        passed,
        "Requires Python 3.11 or higher"
    )
    return passed

def check_node_version():
    """Check Node.js version"""
    try:
        result = subprocess.run(['node', '--version'], capture_output=True, text=True)
        version = result.stdout.strip()
        major = int(version.replace('v', '').split('.')[0])
        passed = major >= 18
        print_check(f"Node.js version ({version})", passed, "Requires Node.js 18 or higher")
        return passed
    except Exception:
        print_check("Node.js installed", False, "Node.js not found in PATH")
        return False

def check_env_file():
    """Check .env file exists and has required keys"""
    env_path = Path(__file__).parent.parent / ".env"
    if not env_path.exists():
        print_check(".env file exists", False, "Run: cp .env.example .env")
        return False
    
    required_keys = [
        'LIVEKIT_URL',
        'LIVEKIT_API_KEY', 
        'LIVEKIT_API_SECRET',
        'OPENROUTER_API_KEY',
        'DEEPGRAM_API_KEY',
        'CARTESIA_API_KEY'
    ]
    
    with open(env_path) as f:
        content = f.read()
    
    missing = []
    placeholder = []
    for key in required_keys:
        if key not in content:
            missing.append(key)
        elif f"{key}=your_" in content or f"{key}=" in content and content.split(f"{key}=")[1].split('\n')[0].strip() == '':
            placeholder.append(key)
    
    if missing:
        print_check(".env has all required keys", False, f"Missing: {', '.join(missing)}")
        return False
    elif placeholder:
        print_check(".env has all required keys", True)
        print_warning(f"Keys with placeholder values: {', '.join(placeholder)}")
        return True
    else:
        print_check(".env has all required keys", True)
        return True

def check_frontend_env():
    """Check frontend .env.local exists"""
    env_path = Path(__file__).parent.parent / "frontend" / ".env.local"
    passed = env_path.exists()
    print_check("Frontend .env.local exists", passed, "Run: cp .env frontend/.env.local")
    return passed

def check_dependencies():
    """Check Python dependencies"""
    try:
        import livekit
        print_check("livekit package installed", True)
    except ImportError:
        print_check("livekit package installed", False, "Run: pip install -r backend/requirements.txt")
        return False
    
    try:
        from livekit.agents.voice import Agent
        print_check("livekit-agents 1.0+ installed", True)
    except ImportError:
        print_check("livekit-agents 1.0+ installed", False, "Run: pip install --upgrade livekit-agents>=1.0.0")
        return False
    
    return True

def check_port_available(port):
    """Check if a port is available"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(('localhost', port))
            return True
        except socket.error:
            return False

def check_ports():
    """Check required ports are available"""
    port_8103 = check_port_available(8103)
    print_check("Port 8103 (frontend) available", port_8103, "Kill process using port 8103")
    return port_8103

def check_directories():
    """Check required directories exist"""
    base = Path(__file__).parent.parent
    
    logs_dir = base / "logs"
    if not logs_dir.exists():
        logs_dir.mkdir(exist_ok=True)
        print_check("logs/ directory", True, "Created")
    else:
        print_check("logs/ directory exists", True)
    
    docs_dir = base / "docs"
    print_check("docs/ directory exists", docs_dir.exists(), "RAG documents directory missing")
    
    return docs_dir.exists()

def check_livekit_url():
    """Validate LiveKit URL format"""
    env_path = Path(__file__).parent.parent / ".env"
    if not env_path.exists():
        return False
    
    with open(env_path) as f:
        for line in f:
            if line.startswith('LIVEKIT_URL='):
                url = line.split('=', 1)[1].strip()
                if url.startswith('wss://'):
                    print_check("LiveKit URL format (wss://)", True)
                    return True
                elif url.startswith('ws://'):
                    print_check("LiveKit URL format", True)
                    print_warning("Using ws:// (insecure). Use wss:// for production.")
                    return True
                else:
                    print_check("LiveKit URL format", False, "Must start with wss:// or ws://")
                    return False
    return False

def check_memory():
    """Check available memory"""
    try:
        import psutil
        mem = psutil.virtual_memory()
        available_gb = mem.available / (1024**3)
        total_gb = mem.total / (1024**3)
        passed = available_gb >= 2.0
        print_check(
            f"Available memory ({available_gb:.1f}GB / {total_gb:.1f}GB)",
            passed,
            "Need at least 2GB available for embedding model"
        )
        return passed
    except ImportError:
        print_info("Install psutil to check memory: pip install psutil")
        return True

def check_pm2():
    """Check PM2 is installed"""
    try:
        result = subprocess.run(['pm2', '--version'], capture_output=True, text=True)
        version = result.stdout.strip()
        print_check(f"PM2 installed ({version})", True)
        return True
    except Exception:
        print_check("PM2 installed", False, "Run: npm install -g pm2")
        return False

def main():
    print(f"\n{Colors.BOLD}Voice Agent RAG - Deployment Diagnostics{Colors.RESET}")
    print(f"Running checks...\n")
    
    all_passed = True
    
    # System Requirements
    print_header("System Requirements")
    all_passed &= check_python_version()
    all_passed &= check_node_version()
    all_passed &= check_memory()
    
    # Environment Configuration
    print_header("Environment Configuration")
    all_passed &= check_env_file()
    all_passed &= check_frontend_env()
    all_passed &= check_livekit_url()
    
    # Dependencies
    print_header("Dependencies")
    all_passed &= check_dependencies()
    all_passed &= check_pm2()
    
    # Runtime
    print_header("Runtime")
    all_passed &= check_ports()
    all_passed &= check_directories()
    
    # Summary
    print_header("Summary")
    if all_passed:
        print(f"  {Colors.GREEN}{Colors.BOLD}All checks passed! Ready for deployment.{Colors.RESET}")
    else:
        print(f"  {Colors.RED}{Colors.BOLD}Some checks failed. Please fix the issues above.{Colors.RESET}")
    
    print()
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())
