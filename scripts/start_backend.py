import os
import sys
import subprocess

def start_backend():
    # List of environment variables to unset
    bad_keys = ['SSL_CERT_FILE', 'REQUESTS_CA_BUNDLE', 'CURL_CA_BUNDLE']
    
    env = os.environ.copy()
    for key in bad_keys:
        if key in env:
            print(f"Removing problematic env var: {key}")
            del env[key]
    
    script_path = os.path.join("backend", "voice_agent_openai.py")
    print(f"Starting backend from {script_path}...")
    
    try:
        # Pass all CLI args (like 'dev') to the script
        args = [sys.executable, script_path] + sys.argv[1:]
        subprocess.check_call(args, env=env)
    except subprocess.CalledProcessError as e:
        print(f"Backend exited with code {e.returncode}")
        sys.exit(e.returncode)
    except KeyboardInterrupt:
        print("Backend stopped.")

if __name__ == "__main__":
    start_backend()
