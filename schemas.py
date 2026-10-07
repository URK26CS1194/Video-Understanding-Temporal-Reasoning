from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class VideoMetadata(BaseModel):
    video_id: str
    filename: str
    filepath: str
    duration: float
    duration_formatted: str
    fps: float
    width: int
    height: int
    total_frames: int
    status: str = "uploaded"  # uploaded, processing, completed, error
    error_message: Optional[str] = None
    processed_at: Optional[str] = None

class TrackedObjectInfo(BaseModel):
    track_id: int
    object_id: str
    label: str
    class_name: str
    first_seen_seconds: float
    last_seen_seconds: float
    first_seen_time: str
    last_seen_time: str
    duration_seconds: float
    is_stationary: bool = False
    in_restricted_area: bool = False
    max_confidence: float = 1.0
    trajectory_points: int = 0

class EventItem(BaseModel):
    event_id: int
    event_type: str
    object_id: str
    object_label: str
    description: str
    start_time: str
    end_time: str
    start_seconds: float
    end_seconds: float
    duration_seconds: float
    confidence: float
    zone: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)

class EventRelationship(BaseModel):
    rel_id: int
    event_a_id: int
    event_b_id: int
    event_a_desc: str
    event_b_desc: str
    relationship: str  # BEFORE, AFTER, DURING, OVERLAPS, FIRST, LAST, REPEATED, CAUSED_BY, FOLLOWED_BY
    delta_seconds: float
    delta_formatted: str

class TemporalQuery(BaseModel):
    video_id: str
    question: str

class QAAnswer(BaseModel):
    question: str
    answer: str
    what_happened: str
    who_what_involved: List[str]
    when_it_happened: str
    duration: str
    before_context: Optional[str] = None
    after_context: Optional[str] = None
    timestamp_range: str
    exact_start_time: str
    exact_end_time: str
    exact_start_seconds: float
    exact_end_seconds: float
    confidence: float
    matched_events: List[EventItem] = Field(default_factory=list)
    relationships: List[str] = Field(default_factory=list)
    is_uncertain: bool = False

class VideoAnalysisResult(BaseModel):
    metadata: VideoMetadata
    events: List[EventItem]
    objects: List[TrackedObjectInfo]
    relationships: List[EventRelationship]
    timeline_summary: List[str]
