import os
from dotenv import dotenv_values

def compare_envs():
    backend_env = dotenv_values(".env") # Check root .env
    frontend_env = dotenv_values("frontend/.env.local")
    
    # Keys to compare
    keys = ["LIVEKIT_URL", "LIVEKIT_API_KEY", "LIVEKIT_API_SECRET", "OPENROUTER_API_KEY"]
    
    print("--- Credential Comparison ---")
    for key in keys:
        b_val = backend_env.get(key)
        f_val = frontend_env.get(key)
        
        if not b_val:
            print(f"❌ Backend missing {key}")
        if not f_val:
            print(f"❌ Frontend missing {key}")
            
        if b_val and f_val:
            if b_val == f_val:
                print(f"✅ {key}: MATCH")
            else:
                print(f"❌ {key}: MISMATCH")
                print(f"   Backend: {b_val[:5]}...")
                print(f"   Frontend: {f_val[:5]}...")

if __name__ == "__main__":
    compare_envs()
