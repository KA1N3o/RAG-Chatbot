import os
import time
from dotenv import load_dotenv
from supabase import create_client
import requests

load_dotenv()

def check_supabase():
    print("Checking Supabase connection...")
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")
    if not url or not key:
        print("❌ SUPABASE_URL or SUPABASE_KEY not found in .env")
        return False
    
    try:
        sb = create_client(url, key)
        start = time.time()
        res = sb.table("documents").select("count", count="exact").limit(1).execute()
        end = time.time()
        print(f"✅ Supabase connected in {end - start:.2f}s. Count: {res.count}")
        return True
    except Exception as e:
        print(f"❌ Supabase connection failed: {e}")
        return False

def check_ollama():
    print("\nChecking Ollama connection...")
    base_url = os.getenv("BASE_URL") or "http://localhost:11434"
    try:
        start = time.time()
        # Check if Ollama is running
        res = requests.get(f"{base_url}/api/tags", timeout=5)
        if res.status_code == 200:
            models = [m['name'] for m in res.json().get('models', [])]
            print(f"✅ Ollama is running. Models: {models}")
            
            # Check if qwen2.5:3b is available
            if "qwen2.5:3b" in models:
                print("✅ Model 'qwen2.5:3b' found.")
            else:
                print("❌ Model 'qwen2.5:3b' NOT found. Please run 'ollama pull qwen2.5:3b'")
                
            # Check embedding model
            if "embeddinggemma:300m" in models:
                print("✅ Model 'embeddinggemma:300m' found.")
            else:
                print("❌ Model 'embeddinggemma:300m' NOT found. Please run 'ollama pull embeddinggemma:300m'")
                
            return True
        else:
            print(f"❌ Ollama returned status code: {res.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print(f"❌ Could not connect to Ollama at {base_url}. Is it running?")
        return False
    except Exception as e:
        print(f"❌ Ollama check failed: {e}")
        return False

if __name__ == "__main__":
    print("--- DIAGNOSTIC START ---")
    sb_ok = check_supabase()
    ollama_ok = check_ollama()
    print("\n--- DIAGNOSTIC END ---")
    if sb_ok and ollama_ok:
        print("✅ All systems appear operational.")
    else:
        print("⚠️ Some systems are down.")
