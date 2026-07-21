"""Job and Dubbing Database Models"""
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Boolean, Integer, Float, ForeignKey, Text, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import enum

Base = declarative_base()


class JobStatus(str, enum.Enum):
    """Job status enumeration"""
    QUEUED = "queued"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class VideoQuality(str, enum.Enum):
    """Video quality enumeration"""
    QUALITY_720P = "720p"
    QUALITY_1080P = "1080p"
    QUALITY_4K = "4K"


class Job(Base):
    """Job model for tracking dubbing tasks"""
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(String(20), default=JobStatus.QUEUED, index=True, nullable=False)
    progress = Column(Integer, default=0, nullable=False)  # 0-100
    
    # Video information
    input_video_path = Column(String(255), nullable=False)
    output_video_path = Column(String(255), nullable=True)
    video_duration = Column(Float, nullable=True)  # in seconds
    video_quality = Column(String(10), default=VideoQuality.QUALITY_1080P, nullable=False)
    
    # Dubbing settings
    source_language = Column(String(10), nullable=False, index=True)
    target_language = Column(String(10), nullable=False, index=True)
    preserve_voice = Column(Boolean, default=True)
    sync_lips = Column(Boolean, default=True)
    voice_id = Column(String(100), nullable=True)  # Selected voice actor ID
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, index=True)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    
    # Error handling
    error_message = Column(Text, nullable=True)
    error_code = Column(String(50), nullable=True)
    
    # Processing metadata
    estimated_duration = Column(Integer, nullable=True)  # in seconds
    retry_count = Column(Integer, default=0)
    max_retries = Column(Integer, default=3)
    
    def __repr__(self):
        return f"<Job(id={self.id}, user_id={self.user_id}, status={self.status})>"


class DubbingSegment(Base):
    """Segments for tracking individual parts of dubbing"""
    __tablename__ = "dubbing_segments"
    
    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, ForeignKey("jobs.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Timing information
    start_time = Column(Float, nullable=False)  # in seconds
    end_time = Column(Float, nullable=False)  # in seconds
    
    # Content
    original_text = Column(Text, nullable=False)
    translated_text = Column(Text, nullable=True)
    
    # Processing status
    status = Column(String(20), default="pending", nullable=False)
    transcription_confidence = Column(Float, nullable=True)  # 0-1
    
    # Audio data
    original_audio_path = Column(String(255), nullable=True)
    dubbed_audio_path = Column(String(255), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<DubbingSegment(id={self.id}, job_id={self.job_id})>"


class Voice(Base):
    """Voice actors available for dubbing"""
    __tablename__ = "voices"
    
    id = Column(String(100), primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    language = Column(String(10), nullable=False, index=True)
    gender = Column(String(20), nullable=False)  # male, female, neutral
    accent = Column(String(100), nullable=True)
    
    # Voice metadata
    description = Column(Text, nullable=True)
    sample_url = Column(String(255), nullable=True)
    preview_audio_url = Column(String(255), nullable=True)
    
    # Quality and pricing
    quality = Column(String(20), default="standard", nullable=False)  # standard, premium
    cost_per_minute = Column(Float, default=0.0, nullable=False)  # in USD
    
    # Availability
    is_available = Column(Boolean, default=True, index=True)
    is_custom = Column(Boolean, default=False)  # User-cloned voice
    
    # Provider information
    provider = Column(String(50), nullable=False)  # elevenlabs, coqui, etc.
    provider_voice_id = Column(String(255), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<Voice(id={self.id}, name={self.name}, language={self.language})>"


class UserVoice(Base):
    """User-created/cloned voices"""
    __tablename__ = "user_voices"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    voice_id = Column(String(100), ForeignKey("voices.id"), nullable=True)
    
    name = Column(String(255), nullable=False)
    sample_audio_path = Column(String(255), nullable=False)
    
    # Status
    status = Column(String(20), default="processing", nullable=False)  # processing, ready, failed
    is_published = Column(Boolean, default=False)
    
    # Metadata
    gender = Column(String(20), nullable=True)
    accent = Column(String(100), nullable=True)
    description = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<UserVoice(id={self.id}, user_id={self.user_id}, name={self.name})>"
