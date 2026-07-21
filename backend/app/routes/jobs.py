"""Jobs Routes"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.dependencies import get_current_active_user
from app.utils.database import get_db
from app.models.user import User
from app.models.job import Job
from app.schemas.job import JobResponse, JobDetailResponse
from app.services.job import JobService
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/", response_model=list[JobResponse])
async def list_jobs(
    skip: int = 0,
    limit: int = 10,
    status: str = None,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    List all jobs for the current user
    
    - **skip**: Number of jobs to skip
    - **limit**: Maximum number of jobs to return
    - **status**: Filter by status (queued, processing, completed, failed, cancelled)
    """
    try:
        query = db.query(Job).filter(Job.user_id == current_user.id)
        
        if status:
            query = query.filter(Job.status == status)
        
        jobs = query.order_by(Job.created_at.desc()).offset(skip).limit(limit).all()
        return jobs
    except Exception as e:
        logger.error(f"Error listing jobs: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to list jobs"
        )


@router.get("/{job_id}", response_model=JobDetailResponse)
async def get_job(
    job_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get job details by ID
    """
    try:
        job = JobService.get_job(db, job_id, current_user)
        return job
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting job: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get job"
        )


@router.get("/{job_id}/download")
async def download_job_result(
    job_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Download the processed video result
    """
    try:
        job = JobService.get_job(db, job_id, current_user)
        
        if job.status != "completed":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Job is not completed yet"
            )
        
        if not job.output_video_path:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Output file not found"
            )
        
        # TODO: Implement file download
        return {"message": "Download endpoint - to be implemented"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error downloading job result: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to download file"
        )


@router.delete("/{job_id}")
async def delete_job(
    job_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Delete a job and its associated files
    """
    try:
        job = JobService.get_job(db, job_id, current_user)
        
        # Only allow deletion of completed or failed jobs
        if job.status not in ["completed", "failed", "cancelled"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot delete job that is still processing"
            )
        
        # TODO: Delete associated files
        db.delete(job)
        db.commit()
        
        return {"message": f"Job {job_id} deleted successfully", "status": "success"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting job: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete job"
        )
