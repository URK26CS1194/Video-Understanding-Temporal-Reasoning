import os
import uuid
import shutil
from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Query, BackgroundTasks
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, List

from backend.config import UPLOAD_DIR, STATIC_DIR, FRONTEND_DIR, ALLOWED_EXTENSIONS
from backend.database.db import init_db
from backend.database.repository import VideoRepository
from backend.cv_engine.video_processor import VideoProcessor
from backend.temporal_engine.qa_reasoner import TemporalQAReasoner
from backend.models.schemas import (
    VideoMetadata, EventItem, TrackedObjectInfo,
    EventRelationship, QAAnswer, TemporalQuery
)
from backend.utils.demo_generator import generate_synthetic_factory_video

# Initialize Database
init_db()

app = FastAPI(
    title="HNX26PSI02: Video Understanding & Temporal Reasoning API",
    description="AI-powered video event detection, multi-object tracking, temporal reasoning, and timestamped QA.",
    version="1.0.0"
)

# Enable CORS for frontend flexibility
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

repo = VideoRepository()
processor = VideoProcessor(repo)
qa_engine = TemporalQAReasoner(repo)

# Serve uploaded videos statically
app.mount("/media", StaticFiles(directory=UPLOAD_DIR), name="media")
# Serve frontend assets
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

@app.get("/api/health")
def health_check():
    return {"status": "ok", "system": "HNX26PSI02 Video Understanding & Temporal Reasoning"}

@app.post("/api/upload")
async def upload_video(file: UploadFile = File(...)):
    """Uploads a video (MP4/AVI/MOV), inspects metadata, and runs full analysis."""
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported format '{ext}'. Supported formats: {', '.join(ALLOWED_EXTENSIONS)}"
        )

    video_id = str(uuid.uuid4())[:8]
    clean_filename = f"{video_id}_{file.filename}"
    saved_path = os.path.join(UPLOAD_DIR, clean_filename)

    with open(saved_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        # Inspect and process video
        meta = processor.inspect_metadata(video_id, saved_path, file.filename)
        result = processor.process_video(video_id)
        return {
            "message": "Video uploaded and analyzed successfully",
            "video_id": video_id,
            "metadata": result.metadata,
            "events_count": len(result.events),
            "objects_count": len(result.objects),
            "relationships_count": len(result.relationships)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed processing video: {str(e)}")

@app.post("/api/generate-demo")
def generate_demo_video():
    """Generates a synthetic surveillance video for instant testing and analyzes it."""
    video_id = "demo_factory"
    filename = "demo_factory_surveillance.mp4"
    filepath = os.path.join(UPLOAD_DIR, filename)

    generate_synthetic_factory_video(filepath, duration_sec=45, fps=20)
    meta = processor.inspect_metadata(video_id, filepath, filename)
    result = processor.process_video(video_id)

    return {
        "message": "Demo factory surveillance video generated and processed successfully",
        "video_id": video_id,
        "metadata": result.metadata,
        "events_count": len(result.events),
        "objects_count": len(result.objects),
        "relationships_count": len(result.relationships)
    }

@app.get("/api/videos", response_model=List[VideoMetadata])
def list_videos():
    return repo.list_videos()

@app.get("/api/videos/{video_id}")
def get_video_details(video_id: str):
    meta = repo.get_video(video_id)
    if not meta:
        raise HTTPException(status_code=404, detail="Video not found")
    events = repo.get_events(video_id)
    objects = repo.get_tracked_objects(video_id)
    relationships = repo.get_relationships(video_id)
    
    # URL for streaming in browser
    video_url = f"/media/{os.path.basename(meta.filepath)}"

    return {
        "metadata": meta,
        "video_url": video_url,
        "events": events,
        "objects": objects,
        "relationships": relationships
    }

@app.get("/api/videos/{video_id}/events", response_model=List[EventItem])
def get_video_events(video_id: str):
    events = repo.get_events(video_id)
    return events

@app.get("/api/videos/{video_id}/objects", response_model=List[TrackedObjectInfo])
def get_video_objects(video_id: str):
    return repo.get_tracked_objects(video_id)

@app.get("/api/videos/{video_id}/relationships", response_model=List[EventRelationship])
def get_video_relationships(video_id: str):
    return repo.get_relationships(video_id)

@app.post("/api/videos/{video_id}/qa", response_model=QAAnswer)
def answer_temporal_question(video_id: str, payload: TemporalQuery):
    """
    Answers natural language temporal queries.
    Enforces mandatory timestamp format, event intervals, durations, and jump parameters.
    """
    if not payload.question or not payload.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")
    return qa_engine.answer_question(video_id, payload.question.strip())

# Serve Frontend HTML
@app.get("/")
def get_index():
    index_file = os.path.join(FRONTEND_DIR, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return {"message": "Frontend not found"}
