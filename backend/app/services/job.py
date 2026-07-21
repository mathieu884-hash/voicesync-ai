"""Job Service"""
from sqlalchemy.orm import Session
from datetime import datetime
from app.models.job import Job, DubbingSegment, Voice, UserVoice, JobStatus, VideoQuality
from app.models.user import User
from app.schemas.job import JobCreate, DubbingCreateRequest
from fastapi import HTTPException, status
import logging
import uuid

logger = logging.getLogger(__name__)


class JobService:
    """Job management service"""

    @staticmethod
    def create_job(
        db: Session,
        user: User,
        job_create: DubbingCreateRequest,
        input_video_path: str,
        video_duration: float
    ) -> Job:
        """Create a new dubbing job"""
        try:
            # Estimate processing duration (rough estimate)
            estimated_duration = int(video_duration * 1.5)  # 1.5x video duration
            
            job = Job(
                user_id=user.id,
                title=job_create.title,
                description=job_create.description,
                status=JobStatus.QUEUED,
                progress=0,
                input_video_path=input_video_path,
                video_duration=video_duration,
                video_quality=job_create.video_quality,
                source_language=job_create.source_language,
                target_language=job_create.target_language,
                preserve_voice=job_create.preserve_voice,
                sync_lips=job_create.sync_lips,
                voice_id=job_create.voice_id,
                estimated_duration=estimated_duration,
            )
            
            db.add(job)
            db.commit()
            db.refresh(job)
            
            logger.info(f"Job created: {job.id} by user {user.id}")
            return job
        except Exception as e:
            db.rollback()
            logger.error(f"Failed to create job: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create job"
            )

    @staticmethod
    def get_job(db: Session, job_id: int, user: User = None) -> Job:
        """Get a job by ID"""
        job = db.query(Job).filter(Job.id == job_id).first()
        
        if not job:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Job not found"
            )
        
        # Check ownership
        if user and job.user_id != user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied"
            )
        
        return job

    @staticmethod
    def get_user_jobs(db: Session, user: User, skip: int = 0, limit: int = 10) -> list:
        """Get all jobs for a user"""
        jobs = db.query(Job).filter(
            Job.user_id == user.id
        ).order_by(Job.created_at.desc()).offset(skip).limit(limit).all()
        
        return jobs

    @staticmethod
    def update_job_status(
        db: Session,
        job: Job,
        status: JobStatus,
        progress: int = None,
        error_message: str = None
    ) -> Job:
        """Update job status and progress"""
        try:
            job.status = status
            
            if progress is not None:
                job.progress = min(progress, 100)
            
            if status == JobStatus.PROCESSING and not job.started_at:
                job.started_at = datetime.utcnow()
            
            if status == JobStatus.COMPLETED:
                job.completed_at = datetime.utcnow()
                job.progress = 100
            
            if status == JobStatus.FAILED:
                job.error_message = error_message
                job.completed_at = datetime.utcnow()
            
            job.updated_at = datetime.utcnow()
            db.commit()
            db.refresh(job)
            
            logger.info(f"Job {job.id} status updated to {status}")
            return job
        except Exception as e:
            db.rollback()
            logger.error(f"Failed to update job status: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to update job"
            )

    @staticmethod
    def cancel_job(db: Session, job: Job) -> Job:
        """Cancel a job"""
        if job.status in [JobStatus.COMPLETED, JobStatus.FAILED, JobStatus.CANCELLED]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Cannot cancel job with status {job.status}"
            )
        
        return JobService.update_job_status(db, job, JobStatus.CANCELLED)

    @staticmethod
    def add_segment(
        db: Session,
        job: Job,
        start_time: float,
        end_time: float,
        original_text: str
    ) -> DubbingSegment:
        """Add a segment to a job"""
        try:
            segment = DubbingSegment(
                job_id=job.id,
                start_time=start_time,
                end_time=end_time,
                original_text=original_text,
                status="pending"
            )
            
            db.add(segment)
            db.commit()
            db.refresh(segment)
            
            return segment
        except Exception as e:
            db.rollback()
            logger.error(f"Failed to add segment: {str(e)}")
            raise


class VoiceService:
    """Voice management service"""

    @staticmethod
    def get_voices(
        db: Session,
        language: str = None,
        gender: str = None,
        skip: int = 0,
        limit: int = 50
    ) -> list:
        """Get available voices with optional filters"""
        query = db.query(Voice).filter(Voice.is_available == True)
        
        if language:
            query = query.filter(Voice.language == language)
        
        if gender:
            query = query.filter(Voice.gender == gender)
        
        voices = query.order_by(Voice.name).offset(skip).limit(limit).all()
        return voices

    @staticmethod
    def get_voice(db: Session, voice_id: str) -> Voice:
        """Get a voice by ID"""
        voice = db.query(Voice).filter(Voice.id == voice_id).first()
        
        if not voice:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Voice not found"
            )
        
        return voice

    @staticmethod
    def create_user_voice(
        db: Session,
        user: User,
        name: str,
        sample_audio_path: str,
        gender: str = None,
        accent: str = None,
        description: str = None
    ) -> UserVoice:
        """Create a user-cloned voice"""
        try:
            user_voice = UserVoice(
                user_id=user.id,
                name=name,
                sample_audio_path=sample_audio_path,
                status="processing",
                gender=gender,
                accent=accent,
                description=description,
            )
            
            db.add(user_voice)
            db.commit()
            db.refresh(user_voice)
            
            logger.info(f"User voice created: {user_voice.id} by user {user.id}")
            return user_voice
        except Exception as e:
            db.rollback()
            logger.error(f"Failed to create user voice: {str(e)}")
            raise

    @staticmethod
    def get_user_voices(db: Session, user: User, skip: int = 0, limit: int = 20) -> list:
        """Get user's custom voices"""
        voices = db.query(UserVoice).filter(
            UserVoice.user_id == user.id
        ).order_by(UserVoice.created_at.desc()).offset(skip).limit(limit).all()
        
        return voices
