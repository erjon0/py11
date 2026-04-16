"""
News Sharing Platform - Run Script
This script starts both the FastAPI backend and Streamlit frontend.
"""

import subprocess
import sys
import time
import webbrowser
from threading import Thread


def run_api():
    """Run the FastAPI backend"""
    subprocess.run([
        sys.executable, "-m", "uvicorn", 
        "main:app", 
        "--host", "0.0.0.0", 
        "--port", "8000",
        "--reload"
    ])


def run_streamlit():
    """Run the Streamlit frontend"""
    subprocess.run([
        sys.executable, "-m", "streamlit", 
        "run", "app.py",
        "--server.port", "8501",
        "--server.headless", "true"
    ])


def main():
    print("=" * 50)
    print("📰 NEWS SHARING PLATFORM")
    print("=" * 50)
    print()
    print("Starting servers...")
    print()
    
    # Start API in a separate thread
    api_thread = Thread(target=run_api, daemon=True)
    api_thread.start()
    print("✅ FastAPI backend starting on http://localhost:8000")
    print("   API Documentation: http://localhost:8000/docs")
    
    # Give API time to start
    time.sleep(2)
    
    # Start Streamlit in a separate thread
    streamlit_thread = Thread(target=run_streamlit, daemon=True)
    streamlit_thread.start()
    print("✅ Streamlit frontend starting on http://localhost:8501")
    
    print()
    print("=" * 50)
    print("Press Ctrl+C to stop all servers")
    print("=" * 50)
    
    # Open browser
    time.sleep(3)
    webbrowser.open("http://localhost:8501")
    
    # Keep main thread alive
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down...")
        sys.exit(0)


if __name__ == "__main__":
    main()
