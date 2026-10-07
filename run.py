import os
import sys
import webbrowser
import threading
import time

# Ensure backend package can be imported from current working directory
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def prepare_demo():
    """Generates the demo video and pre-processes it so the system works out of the box."""
    from backend.config import UPLOAD_DIR
    from backend.database.db import init_db
    from backend.database.repository import VideoRepository
    from backend.cv_engine.video_processor import VideoProcessor
    from backend.utils.demo_generator import generate_synthetic_factory_video

    init_db()
    repo = VideoRepository()
    
    # Check if demo already processed
    existing = repo.get_video("demo_factory")
    if not existing:
        print("[System] Generating synthetic surveillance demo video...")
        demo_path = os.path.join(UPLOAD_DIR, "demo_factory_surveillance.mp4")
        generate_synthetic_factory_video(demo_path, duration_sec=45, fps=20)
        
        print("[System] Analyzing video events, tracks, and temporal relationships...")
        processor = VideoProcessor(repo)
        processor.inspect_metadata("demo_factory", demo_path, "demo_factory_surveillance.mp4")
        result = processor.process_video("demo_factory")
        print(f"[System] Demo analysis complete! Found {len(result.events)} events, {len(result.objects)} objects.")

def open_browser():
    time.sleep(1.5)
    webbrowser.open("http://127.0.0.1:8000")

if __name__ == "__main__":
    try:
        import uvicorn
    except ImportError:
        print("ERROR: uvicorn is not installed. Please run: pip install -r requirements.txt")
        sys.exit(1)

    print("=================================================================")
    print(" HNX26PSI02: Video Understanding & Temporal Reasoning System ")
    print("=================================================================")
    
    try:
        prepare_demo()
    except Exception as e:
        print(f"[Warning] Could not pre-generate demo video: {e}")

    threading.Thread(target=open_browser, daemon=True).start()
    
    print("[System] Starting server at http://127.0.0.1:8000 ...")
    uvicorn.run("backend.app:app", host="127.0.0.1", port=8000, reload=False)
