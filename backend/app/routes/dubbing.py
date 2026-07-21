"""Dubbing Routes"""
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from app.dependencies import get_current_active_user
from app.utils.database import get_db
from app.models.user import User
from app.models.job import Job
from app.schemas.job import (
    DubbingCreateRequest,
    DubbingJobResponse,
    JobResponse,
    JobDetailResponse,
)
from app.services.job import JobService
import logging
import os
from datetime import datetime

logger = logging.getLogger(__name__)

router = APIRouter()

# Video upload directory
UPLOAD_DIR = "uploads/videos"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/create", response_model=DubbingJobResponse, status_code=status.HTTP_201_CREATED)
async def create_dubbing_job(
    title: str = Form(...),
    source_language: str = Form(...),
    target_language: str = Form(...),
    video_quality: str = Form("1080p"),
    preserve_voice: bool = Form(True),
    sync_lips: bool = Form(True),
    voice_id: str = Form(None),
    description: str = Form(None),
    video: UploadFile = File(...),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Create a new dubbing job
    
    - **title**: Job title
    - **source_language**: Source language code (e.g., "en")
    - **target_language**: Target language code (e.g., "fr")
    - **video_quality**: Output quality ("720p", "1080p", "4K")
    - **preserve_voice**: Keep original voice timbre
    - **sync_lips**: Enable lip synchronization
    - **voice_id**: Optional voice actor ID
    - **video**: Video file (max 2GB)
    """
    try:
        # Validate file
        if not video.filename:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No file provided"
            )
        
        # Check file size (2GB limit)
        content = await video.read()
        file_size = len(content)
        max_size = 2 * 1024 * 1024 * 1024  # 2GB
        
        if file_size > max_size:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail="File size exceeds 2GB limit"
            )
        
        # Save video file
        filename = f"{current_user.id}_{datetime.utcnow().timestamp()}_{video.filename}"
        filepath = os.path.join(UPLOAD_DIR, filename)
        
        with open(filepath, "wb") as f:
            f.write(content)
        
        # TODO: Get video duration using ffprobe or similar
        video_duration = 60.0  # Placeholder
        
        # Create job
        job_create = DubbingCreateRequest(
            title=title,
            description=description,
            source_language=source_language,
            target_language=target_language,
            video_quality=video_quality,
            preserve_voice=preserve_voice,
            sync_lips=sync_lips,
            voice_id=voice_id,
        )
        
        job = JobService.create_job(
            db,
            current_user,
            job_create,
            filepath,
            video_duration
        )
        
        return DubbingJobResponse(
            job_id=job.id,
            status=job.status,
            created_at=job.created_at,
            estimated_duration=job.estimated_duration,
            message="Dubbing job created successfully"
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating dubbing job: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create dubbing job"
        )


@router.post("/cancel/{job_id}", status_code=status.HTTP_200_OK)
async def cancel_dubbing_job(
    job_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Cancel a dubbing job
    """
    try:
        job = JobService.get_job(db, job_id, current_user)
        
        cancelled_job = JobService.cancel_job(db, job)
        
        return {
            "job_id": cancelled_job.id,
            "status": cancelled_job.status,
            "message": f"Job {job_id} cancelled successfully"
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error cancelling job: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to cancel job"
        )
