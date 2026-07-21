"""Updated Schemas Package"""
from app.schemas.user import (
    UserCreate,
    UserResponse,
    LoginRequest,
    TokenResponse,
    ChangePasswordRequest,
)
from app.schemas.job import (
    JobCreate,
    JobResponse,
    JobDetailResponse,
    VoiceResponse,
    UserVoiceCreate,
    UserVoiceResponse,
    DubbingCreateRequest,
    DubbingJobResponse,
)

__all__ = [
    # User schemas
    "UserCreate",
    "UserResponse",
    "LoginRequest",
    "TokenResponse",
    "ChangePasswordRequest",
    # Job schemas
    "JobCreate",
    "JobResponse",
    "JobDetailResponse",
    "VoiceResponse",
    "UserVoiceCreate",
    "UserVoiceResponse",
    "DubbingCreateRequest",
    "DubbingJobResponse",
]
