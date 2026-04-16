"""
Script to run both the FastAPI backend and Streamlit frontend.
Run with: python run.py
"""
import subprocess
import sys
import time
import threading
import os

def run_api():
    """Run the FastAPI backend server."""
    print("Starting FastAPI backend on http://localhost:8000")
    subprocess.run([
        sys.executable, "-m", "uvicorn", 
        "api:app", 
        "--host", "0.0.0.0", 
        "--port", "8000",
        "--reload"
    ])

def run_streamlit():
    """Run the Streamlit frontend."""
    time.sleep(2)  # Wait for API to start
    print("Starting Streamlit frontend on http://localhost:8501")
    subprocess.run([
        sys.executable, "-m", "streamlit", 
        "run", "app.py",
        "--server.port", "8501"
    ])

if __name__ == "__main__":
    # Change to script directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # Initialize database first
    from database import init_database
    init_database()
    print("Database initialized!")
    
    # Run API in a separate thread
    api_thread = threading.Thread(target=run_api, daemon=True)
    api_thread.start()
    
    # Run Streamlit in main thread
    run_streamlit()
