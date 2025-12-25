import os
import sys
import subprocess

def install_safe():
    # List of environment variables to unset
    bad_keys = ['SSL_CERT_FILE', 'REQUESTS_CA_BUNDLE', 'CURL_CA_BUNDLE']
    
    env = os.environ.copy()
    for key in bad_keys:
        if key in env:
            print(f"Removing problematic env var: {key}")
            del env[key]
    
    # 1. Upgrade pip (fixes wheel detection issues)
    print("Upgrading pip...")
    try:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "--upgrade", "pip"],
            env=env
        )
        # Print pip version
        subprocess.check_call([sys.executable, "-m", "pip", "--version"], env=env)
    except Exception as e:
        print(f"Pip upgrade failed (non-critical): {e}")

    # 2. Install critical lightweight deps
    print("Installing critical dependencies...")
    subprocess.check_call(
        [sys.executable, "-m", "pip", "install", "python-dotenv", "certifi"],
        env=env
    )
    
    # 3. Install livekit binaries explicitly
    print("Attempting to install LiveKit binaries...")
    try:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "livekit", "livekit-agents", "--only-binary=:all:", "--prefer-binary"],
            env=env
        )
        print("LiveKit binary installation successful.")
    except subprocess.CalledProcessError:
        print("Could not find binaries for LiveKit. Attempting full install (might fail)...")
    
    # 4. Install full requirements
    requirements_path = os.path.join("backend", "requirements.txt")
    print(f"Installing all dependencies from {requirements_path}...")
    
    try:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "-r", requirements_path, "--only-binary=:all:", "--prefer-binary"],
            env=env
        )
        print("Full installation successful.")
    except subprocess.CalledProcessError as e:
        print(f"Full installation failed with code {e.returncode}. Critical deps should be installed.")

if __name__ == "__main__":
    install_safe()
