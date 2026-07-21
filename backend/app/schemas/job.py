"""Job and Dubbing Schemas"""
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List
from enum import Enum


class JobStatusEnum(str, Enum):
    """Job status enumeration"""
    QUEUED = "queued"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class VideoQualityEnum(str, Enum):
    """Video quality enumeration"""
    QUALITY_720P = "720p"
    QUALITY_1080P = "1080p"
    QUALITY_4K = "4K"


class DubbingSegmentBase(BaseModel):
    """Base dubbing segment schema"""
    start_time: float
    end_time: float
    original_text: str
    translated_text: Optional[str] = None


class DubbingSegmentResponse(DubbingSegmentBase):
    """Dubbing segment response schema"""
    id: int
    job_id: int
    status: str
    transcription_confidence: Optional[float] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class JobCreate(BaseModel):
    """Job creation schema"""
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    source_language: str = Field(..., min_length=2, max_length=10)
    target_language: str = Field(..., min_length=2, max_length=10)
    video_quality: VideoQualityEnum = VideoQualityEnum.QUALITY_1080P
    preserve_voice: bool = True
    sync_lips: bool = True
    voice_id: Optional[str] = None


class JobUpdate(BaseModel):
    """Job update schema"""
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[JobStatusEnum] = None
    progress: Optional[int] = Field(None, ge=0, le=100)


class JobResponse(BaseModel):
    """Job response schema"""
    id: int
    user_id: int
    title: str
    description: Optional[str]
    status: str
    progress: int
    source_language: str
    target_language: str
    video_quality: str
    preserve_voice: bool
    sync_lips: bool
    voice_id: Optional[str]
    video_duration: Optional[float]
    estimated_duration: Optional[int]
    created_at: datetime
    updated_at: datetime
    started_at: Optional[datetime]
    completed_at: Optional[datetime]
    error_message: Optional[str]
    retry_count: int

    class Config:
        from_attributes = True


class JobDetailResponse(JobResponse):
    """Detailed job response with segments"""
    segments: List[DubbingSegmentResponse] = []


class VoiceBase(BaseModel):
    """Base voice schema"""
    name: str
    language: str
    gender: str
    accent: Optional[str] = None
    description: Optional[str] = None


class VoiceResponse(VoiceBase):
    """Voice response schema"""
    id: str
    sample_url: Optional[str]
    preview_audio_url: Optional[str]
    quality: str
    cost_per_minute: float
    is_available: bool
    provider: str
    created_at: datetime

    class Config:
        from_attributes = True


class UserVoiceCreate(BaseModel):
    """User voice creation schema"""
    name: str = Field(..., min_length=1, max_length=255)
    gender: Optional[str] = None
    accent: Optional[str] = None
    description: Optional[str] = None


class UserVoiceResponse(BaseModel):
    """User voice response schema"""
    id: int
    user_id: int
    name: str
    status: str
    is_published: bool
    gender: Optional[str]
    accent: Optional[str]
    description: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class DubbingCreateRequest(BaseModel):
    """Dubbing creation request"""
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    source_language: str = Field(..., min_length=2, max_length=10)
    target_language: str = Field(..., min_length=2, max_length=10)
    video_quality: VideoQualityEnum = VideoQualityEnum.QUALITY_1080P
    preserve_voice: bool = True
    sync_lips: bool = True
    voice_id: Optional[str] = None


class DubbingJobResponse(BaseModel):
    """Response for dubbing job creation"""
    job_id: int
    status: str
    created_at: datetime
    estimated_duration: Optional[int]
    message: str = "Dubbing job created successfully"
