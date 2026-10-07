import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
STATIC_DIR = os.path.join(BASE_DIR, "static")
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")
DATA_DIR = os.path.join(BASE_DIR, "data")

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(STATIC_DIR, exist_ok=True)
os.makedirs(DATA_DIR, exist_ok=True)

# Processing parameters
FRAME_SAMPLE_RATE = 2.0  # Sample 2 frames per second for video understanding
MAX_OCCLUSION_FRAMES = 30  # Max frames to remember occluded object
STATIONARY_THRESHOLD_SECONDS = 10.0  # Threshold to mark object stationary
RESTRICTED_ZONE_RATIO = {
    # Default restricted area occupies bottom-right quadrant of factory floor
    "name": "Restricted Zone A",
    "x_min": 0.55,
    "y_min": 0.45,
    "x_max": 0.95,
    "y_max": 0.92
}

ALLOWED_EXTENSIONS = {".mp4", ".avi", ".mov", ".mkv", ".webm"}
