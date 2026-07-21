"""Celery Task Queue Configuration"""
from celery import Celery
from app.config import settings
import logging

logger = logging.getLogger(__name__)

celery_app = Celery(
    "voicesync_ai",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,
    task_soft_time_limit=25 * 60,
    worker_prefetch_multiplier=1,
    worker_max_tasks_per_child=1000,
)


@celery_app.task(bind=True, max_retries=3)
def process_dubbing_task(self, job_id: int, user_id: int):
    """
    Asynchronous task to process dubbing job
    """
    try:
        from app.utils.database import SessionLocal
        from app.models.job import Job
        from app.models.user import User
        from app.services.dubbing_pipeline import DubbingPipelineService
        import asyncio
        
        db = SessionLocal()
        
        try:
            job = db.query(Job).filter(Job.id == job_id).first()
            user = db.query(User).filter(User.id == user_id).first()
            
            if not job or not user:
                logger.error(f"Job or user not found: job_id={job_id}, user_id={user_id}")
                return {"status": "failed", "error": "Job or user not found"}
            
            pipeline = DubbingPipelineService()
            result = asyncio.run(pipeline.process_dubbing_job(db, job, user))
            
            logger.info(f"Dubbing task completed: {result}")
            return result
        
        finally:
            db.close()
    
    except Exception as exc:
        logger.error(f"Dubbing task failed: {str(exc)}")
        raise self.retry(exc=exc, countdown=60 * (2 ** self.request.retries))


@celery_app.task
def cleanup_old_jobs():
    """
    Periodic task to cleanup old temporary files
    """
    import os
    import shutil
    from datetime import datetime, timedelta
    
    try:
        temp_dir = "temp"
        if os.path.exists(temp_dir):
            cutoff_time = (datetime.utcnow() - timedelta(hours=24)).timestamp()
            
            for dirname in os.listdir(temp_dir):
                dirpath = os.path.join(temp_dir, dirname)
                if os.path.isdir(dirpath):
                    dir_time = os.path.getmtime(dirpath)
                    if dir_time < cutoff_time:
                        shutil.rmtree(dirpath)
                        logger.info(f"Cleaned up temporary directory: {dirpath}")
        
        return {"status": "success", "message": "Cleanup completed"}
    
    except Exception as e:
        logger.error(f"Cleanup task failed: {str(e)}")
        return {"status": "failed", "error": str(e)}
