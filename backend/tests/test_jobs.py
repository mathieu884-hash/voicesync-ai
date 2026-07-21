"""Tests for Job Service"""
import pytest
from sqlalchemy.orm import Session
from app.models.job import Job, JobStatus
from app.models.user import User
from app.schemas.job import DubbingCreateRequest
from app.services.job import JobService, VoiceService
from app.utils.database import SessionLocal
from app.services.auth import AuthService
from app.schemas.user import UserCreate


@pytest.fixture
def db():
    """Database session fixture"""
    db = SessionLocal()
    yield db
    db.close()


@pytest.fixture
def test_user(db: Session):
    """Create test user"""
    user_data = UserCreate(
        email="jobtest@example.com",
        username="jobtest",
        full_name="Job Test User",
        password="TestPassword123"
    )
    return AuthService.register_user(db, user_data)


class TestJobCreation:
    """Test job creation"""
    
    def test_create_job_success(self, db: Session, test_user: User):
        """Test successful job creation"""
        job_data = DubbingCreateRequest(
            title="Test Dubbing Job",
            description="Test description",
            source_language="en",
            target_language="fr",
            preserve_voice=True,
            sync_lips=True
        )
        
        job = JobService.create_job(
            db,
            test_user,
            job_data,
            "/path/to/video.mp4",
            120.0
        )
        
        assert job.title == job_data.title
        assert job.user_id == test_user.id
        assert job.status == JobStatus.QUEUED
        assert job.progress == 0
    
    def test_job_has_estimated_duration(self, db: Session, test_user: User):
        """Test job has estimated duration"""
        job_data = DubbingCreateRequest(
            title="Test Job",
            source_language="en",
            target_language="fr"
        )
        
        job = JobService.create_job(
            db,
            test_user,
            job_data,
            "/path/to/video.mp4",
            100.0
        )
        
        assert job.estimated_duration is not None
        assert job.estimated_duration > 0


class TestJobRetrieval:
    """Test job retrieval"""
    
    def test_get_job_success(self, db: Session, test_user: User):
        """Test retrieving job"""
        job_data = DubbingCreateRequest(
            title="Test Job",
            source_language="en",
            target_language="fr"
        )
        
        created_job = JobService.create_job(
            db,
            test_user,
            job_data,
            "/path/to/video.mp4",
            120.0
        )
        
        retrieved_job = JobService.get_job(db, created_job.id, test_user)
        
        assert retrieved_job.id == created_job.id
        assert retrieved_job.title == created_job.title
    
    def test_get_job_not_found(self, db: Session, test_user: User):
        """Test getting non-existent job"""
        with pytest.raises(Exception):
            JobService.get_job(db, 9999, test_user)
    
    def test_get_user_jobs(self, db: Session, test_user: User):
        """Test retrieving user's jobs"""
        job_data = DubbingCreateRequest(
            title="Job 1",
            source_language="en",
            target_language="fr"
        )
        
        JobService.create_job(db, test_user, job_data, "/path/to/video1.mp4", 120.0)
        JobService.create_job(db, test_user, job_data, "/path/to/video2.mp4", 150.0)
        
        jobs = JobService.get_user_jobs(db, test_user, limit=10)
        
        assert len(jobs) >= 2


class TestJobStatusUpdate:
    """Test job status updates"""
    
    def test_update_job_status(self, db: Session, test_user: User):
        """Test updating job status"""
        job_data = DubbingCreateRequest(
            title="Test Job",
            source_language="en",
            target_language="fr"
        )
        
        job = JobService.create_job(
            db,
            test_user,
            job_data,
            "/path/to/video.mp4",
            120.0
        )
        
        updated_job = JobService.update_job_status(
            db,
            job,
            JobStatus.PROCESSING,
            progress=50
        )
        
        assert updated_job.status == JobStatus.PROCESSING
        assert updated_job.progress == 50
    
    def test_complete_job(self, db: Session, test_user: User):
        """Test completing a job"""
        job_data = DubbingCreateRequest(
            title="Test Job",
            source_language="en",
            target_language="fr"
        )
        
        job = JobService.create_job(
            db,
            test_user,
            job_data,
            "/path/to/video.mp4",
            120.0
        )
        
        completed_job = JobService.update_job_status(
            db,
            job,
            JobStatus.COMPLETED
        )
        
        assert completed_job.status == JobStatus.COMPLETED
        assert completed_job.progress == 100
        assert completed_job.completed_at is not None


class TestJobCancellation:
    """Test job cancellation"""
    
    def test_cancel_queued_job(self, db: Session, test_user: User):
        """Test cancelling a queued job"""
        job_data = DubbingCreateRequest(
            title="Test Job",
            source_language="en",
            target_language="fr"
        )
        
        job = JobService.create_job(
            db,
            test_user,
            job_data,
            "/path/to/video.mp4",
            120.0
        )
        
        cancelled_job = JobService.cancel_job(db, job)
        
        assert cancelled_job.status == JobStatus.CANCELLED
    
    def test_cannot_cancel_completed_job(self, db: Session, test_user: User):
        """Test cannot cancel completed job"""
        job_data = DubbingCreateRequest(
            title="Test Job",
            source_language="en",
            target_language="fr"
        )
        
        job = JobService.create_job(
            db,
            test_user,
            job_data,
            "/path/to/video.mp4",
            120.0
        )
        
        JobService.update_job_status(db, job, JobStatus.COMPLETED)
        
        with pytest.raises(Exception):
            JobService.cancel_job(db, job)
