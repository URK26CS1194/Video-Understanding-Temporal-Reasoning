# HNX26PSI02: Video Understanding & Temporal Reasoning System

An AI-powered video understanding and temporal reasoning platform that analyzes surveillance and operational footage, detects and tracks entities across frames, extracts temporal events, mines event relationships (Allen's Interval Algebra), and answers natural-language questions with mandatory timestamps and interactive video seeking.

---

## 🌟 Key Capabilities

1. **Multi-Format Video Ingestion & Inspection**
   - Supports MP4, AVI, MOV, MKV, and WebM.
   - Extracts and displays FPS, resolution, frame counts, and duration.
   - Dynamic temporal frame sampling (optimized for short clips as well as long video streams).

2. **Persistent Multi-Object Tracking & Occlusion Handling**
   - Assigns unique, persistent human-readable IDs (`Person 1`, `Delivery Truck 1`, `Machine 1`).
   - Velocity-based trajectory estimation and IoU matching.
   - Preserves object identities even when entities are temporarily occluded behind obstacles.
   - Distinguishes stationary vs. moving states and calculates total scene residence time.

3. **Domain Event Detection**
   - Frame entry and departure detection.
   - Restricted area breaches (`Restricted Zone A` entry & exit events).
   - Safety alarm triggers (beacon pulse detection).
   - Machine idle and stoppage tracking.
   - Long-duration stationary/untouched item detection.

4. **Allen's Interval Temporal Algebra & Event Graphs**
   - Automatically computes relationships between all events:
     - `BEFORE` / `AFTER`
     - `DURING` / `OVERLAPS`
     - `FIRST` / `LAST`
     - `REPEATED`
     - `CAUSED_BY` / `FOLLOWED_BY` (causal proximity reasoning)

5. **Mandatory Timestamped Question Answering**
   - **Strict Rule:** Every answer contains exact video timestamps (`HH:MM:SS`), start/end ranges (`Start: HH:MM:SS | End: HH:MM:SS`), duration, and confidence scores.
   - Answers questions such as:
     - *"What happened before the safety alarm?"*
     - *"Who entered the restricted area after the delivery truck arrived?"*
     - *"How many times did the machine stop?"*
     - *"When did the person enter the restricted area?"*
     - *"Which object remained untouched for more than 2 minutes?"*
     - *"What happened between 00:02:15 and 00:03:30?"*
   - Interactive **"Jump to Timestamp"** button that seeks the video directly to the exact moment in the browser.

6. **Built-in Synthetic Factory Demo Generator**
   - Includes a 1-click synthetic surveillance video generator reproducing the exact operational scenario (person entering, delivery truck arriving, restricted zone entry, alarm beacon flashing, machine stopping, person leaving).
   - Enables immediate evaluation without needing to upload external files.

---

## 🏛️ System Architecture

```text
               Video Input (MP4 / AVI / MOV)
                            │
                            ▼
              Adaptive Temporal Frame Sampler
                            │
                            ▼
           Multi-Modal Object Detector (YOLO / CV)
                            │
                            ▼
         Multi-Object Tracker (Kalman / Velocity / IoU)
       ┌────────────────────┼────────────────────┐
       ▼                    ▼                    ▼
   Persistent ID      Occlusion Handler     Zone Analyzer
 (Person 1, Truck 1)   (Tracks across gaps)  (Restricted Area)
       │                    │                    │
       └────────────────────┼────────────────────┘
                            │
                            ▼
              Spatiotemporal Event Detector
                            │
                            ▼
               SQLite Event & Track Database
                            │
                            ▼
             Allen's Interval Algebra Engine
       (BEFORE, AFTER, DURING, FOLLOWED_BY, REPEATED)
                            │
                            ▼
              Temporal QA Reasoning Engine
                            │
                            ▼
   Mandatory Timestamped Answer + Jump to Timestamp
```

---

## 📂 Project Structure

```text
video_temporal_reasoning/
├── backend/
│   ├── app.py                 # FastAPI application & REST endpoints
│   ├── config.py              # Configuration & storage settings
│   ├── models/
│   │   └── schemas.py         # Pydantic schemas (Events, Objects, QA)
│   ├── database/
│   │   ├── db.py              # SQLite schema & database connection
│   │   └── repository.py      # CRUD repository with temporal indexing
│   ├── cv_engine/
│   │   ├── detector.py        # Object detector (YOLO + Adaptive CV fallback)
│   │   ├── tracker.py         # Multi-object tracker with persistent IDs
│   │   ├── zone_analyzer.py   # Restricted zone footprint analysis
│   │   ├── event_detector.py  # Structured event extraction
│   │   └── video_processor.py # End-to-end video pipeline coordinator
│   ├── temporal_engine/
│   │   ├── allen_algebra.py   # Allen's interval algebra relation engine
│   │   └── qa_reasoner.py     # Temporal question answering engine
│   └── utils/
│       ├── time_utils.py      # Timestamp parsing & duration formatting
│       └── demo_generator.py  # Synthetic factory video generator
├── frontend/
│   ├── index.html             # Single-page dashboard HTML
│   ├── css/style.css          # CSS import wrapper
│   └── js/app.js              # JS logic
├── static/
│   ├── style.css              # Cyber/Industrial dark mode UI theme
│   └── app.js                 # Frontend interactive logic
├── tests/
│   └── test_temporal_reasoning.py # Automated test suite
├── requirements.txt           # Project dependencies
├── run.py                     # One-click system launcher
└── README.md                  # System documentation
```

---

## 🚀 Quick Start Guide

### 1. Prerequisites
- Python 3.8+ (tested on Python 3.10+)

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Launch the System
```bash
python run.py
```
This will:
1. Initialize the SQLite event database.
2. Automatically pre-generate and analyze the synthetic factory surveillance demo video.
3. Start the FastAPI server on `http://127.0.0.1:8000`.
4. Automatically open your web browser to the dashboard!

---

## 🧪 Running Automated Tests

Run the unit and temporal logic tests:
```bash
python -m unittest tests/test_temporal_reasoning.py
```

All tests verify:
- Persistent object identity preservation across occlusion gaps.
- Allen interval algebra relations (`BEFORE`, `AFTER`, `FOLLOWED_BY`, `REPEATED`).
- Strict enforcement of mandatory timestamps on all QA responses.
- Accurate interval calculations and question parsing.

---

## 📡 REST API Reference

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/health` | System health check |
| `POST` | `/api/upload` | Upload MP4/AVI/MOV video and trigger analysis |
| `POST` | `/api/generate-demo` | Generate & process synthetic test surveillance video |
| `GET` | `/api/videos` | List all processed videos |
| `GET` | `/api/videos/{video_id}` | Get video metadata, events, tracks, relationships |
| `GET` | `/api/videos/{video_id}/events` | Fetch timeline of detected events |
| `GET` | `/api/videos/{video_id}/objects` | Fetch tracked objects and entity registry |
| `GET` | `/api/videos/{video_id}/relationships` | Fetch pairwise temporal relations |
| `POST` | `/api/videos/{video_id}/qa` | Ask a natural language question; returns timestamped answer |

### Event Schema Format:
```json
{
  "event_id": 3,
  "event_type": "restricted_area_entry",
  "object_id": "person_1",
  "object_label": "Person 1",
  "description": "Person 1 enters Restricted Zone A",
  "start_time": "00:00:18",
  "end_time": "00:00:23",
  "start_seconds": 18.0,
  "end_seconds": 23.0,
  "duration_seconds": 5.0,
  "confidence": 0.94,
  "zone": "Restricted Zone A"
}
```

### QA Response Format:
```json
{
  "question": "Who entered the restricted area after the delivery truck arrived?",
  "answer": "Person 1 entered the restricted area at 00:00:18, approximately 10 seconds after Delivery Truck 1 arrived at 00:00:08.",
  "what_happened": "Person 1 enters Restricted Zone A",
  "who_what_involved": ["Person 1", "Delivery Truck 1"],
  "when_it_happened": "00:00:18",
  "duration": "5 seconds",
  "timestamp_range": "Start: 00:00:18 | End: 00:00:23",
  "exact_start_time": "00:00:18",
  "exact_end_time": "00:00:23",
  "exact_start_seconds": 18.0,
  "exact_end_seconds": 23.0,
  "confidence": 0.94
}
```
