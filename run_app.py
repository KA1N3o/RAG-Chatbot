import subprocess
import sys
import time
import os

def run_services():
    print("Starting RAG Chatbot System...")
    print("-----------------------------------")
    
    # 1. Start Backend
    print("[1/2] Launching Backend (FastAPI)...")
    # Start uvicorn in the background, sharing the same console output
    backend_process = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "server:app", "--reload", "--host", "0.0.0.0", "--port", "8000"],
        cwd=os.getcwd(),
        env=os.environ.copy()
    )
    
    print("⏳ Waiting 5s for backend to initialize...")
    time.sleep(5)
    
    # 2. Start Frontend
    print("🔹 [2/2] Launching Frontend (Streamlit)...")
    frontend_process = subprocess.Popen(
        [sys.executable, "-m", "streamlit", "run", "streamlit_app.py"],
        cwd=os.getcwd(),
        env=os.environ.copy()
    )
    
    print("\n System is running in this single window!")
    print("   - Backend API: http://localhost:8000")
    print("   - Web App:     http://localhost:8501")
    print("\n Press Ctrl+C in this window to stop ALL services.\n")

    try:
        # Keep the script running to monitor processes
        while True:
            time.sleep(1)
            # Check if processes are still alive
            if backend_process.poll() is not None:
                print("\nBackend process exited unexpectedly.")
                break
            if frontend_process.poll() is not None:
                print("\nFrontend process exited unexpectedly.")
                break
    except KeyboardInterrupt:
        print("\nStopping all services...")
    finally:
        # Terminate processes gracefully
        backend_process.terminate()
        frontend_process.terminate()
        
        # Wait a bit to ensure they close
        try:
            backend_process.wait(timeout=3)
            frontend_process.wait(timeout=3)
        except subprocess.TimeoutExpired:
            backend_process.kill()
            frontend_process.kill()
            
        print("Shutdown complete.")

if __name__ == "__main__":
    run_services()
