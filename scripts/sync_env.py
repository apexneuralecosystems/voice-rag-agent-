import os
from dotenv import dotenv_values

def sync_env():
    # Read frontend env
    frontend_env = dotenv_values("frontend/.env.local")
    if not frontend_env:
        print("❌ Could not read frontend/.env.local")
        return

    # Keys to copy
    target_keys = [
        "LIVEKIT_URL", 
        "LIVEKIT_API_KEY", 
        "LIVEKIT_API_SECRET", 
        "OPENROUTER_API_KEY", 
        "CARTESIA_VOICE_ID",
        "DEEPGRAM_API_KEY"
    ]
    
    # Check what we have
    new_env_content = ""
    for key in target_keys:
        val = frontend_env.get(key)
        if not val:
            # Try mapping from NEXT_PUBLIC variants if needed, or check os.environ
            if key == "LIVEKIT_URL":
                val = frontend_env.get("NEXT_PUBLIC_LIVEKIT_URL")
            
        if val:
            new_env_content += f"{key}={val}\n"
            print(f"✅ Found {key}")
        else:
            print(f"⚠️ Missing {key} in frontend config (might be needed)")

    # Write to backend/.env
    backend_env_path = "backend/.env"
    with open(backend_env_path, "w") as f:
        f.write(new_env_content)
    
    print(f"🎉 Successfully created {backend_env_path}")

if __name__ == "__main__":
    sync_env()
