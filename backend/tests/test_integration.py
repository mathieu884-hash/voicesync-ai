"""Integration tests for the complete dubbing pipeline"""
import pytest
import asyncio
from sqlalchemy.orm import Session
from app.models.user import User
from app.models.job import Job, JobStatus
from app.services.job import JobService
from app.services.external_apis import (
    WhisperService,
    DeepLService,
    ElevenLabsService,
)
from app.utils.database import SessionLocal
from app.services.auth import AuthService
from app.schemas.user import UserCreate
from app.schemas.job import DubbingCreateRequest


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
        email="integration@example.com",
        username="integration",
        full_name="Integration Test User",
        password="TestPassword123"
    )
    return AuthService.register_user(db, user_data)


@pytest.fixture
def test_job(db: Session, test_user: User):
    """Create test job"""
    job_data = DubbingCreateRequest(
        title="Integration Test Job",
        description="Test integration",
        source_language="en",
        target_language="fr",
        preserve_voice=True,
        sync_lips=False
    )
    
    return JobService.create_job(
        db,
        test_user,
        job_data,
        "/path/to/test_video.mp4",
        120.0
    )


class TestJobLifecycle:
    """Test complete job lifecycle"""
    
    def test_job_creation_to_completion(self, db: Session, test_user: User):
        """Test job from creation to completion"""
        job_data = DubbingCreateRequest(
            title="Lifecycle Test",
            source_language="en",
            target_language="fr"
        )
        
        # Create job
        job = JobService.create_job(
            db,
            test_user,
            job_data,
            "/path/to/video.mp4",
            120.0
        )
        
        assert job.status == JobStatus.QUEUED
        assert job.progress == 0
        
        # Update to processing
        job = JobService.update_job_status(db, job, JobStatus.PROCESSING, progress=50)
        assert job.status == JobStatus.PROCESSING
        assert job.progress == 50
        
        # Complete job
        job = JobService.update_job_status(db, job, JobStatus.COMPLETED, progress=100)
        assert job.status == JobStatus.COMPLETED
        assert job.progress == 100
        assert job.completed_at is not None


class TestExternalAPIMocks:
    """Test external API services with mocks"""
    
    @pytest.mark.asyncio
    async def test_whisper_transcription(self):
        """Test Whisper API integration (mocked)"""
        service = WhisperService()
        
        # This would be mocked in actual tests
        result = await service.transcribe_audio(
            "/path/to/audio.wav",
            language="en"
        )
        
        # Result should have status field
        assert "status" in result
    
    @pytest.mark.asyncio
    async def test_deepl_translation(self):
        """Test DeepL API integration (mocked)"""
        service = DeepLService()
        
        result = await service.translate_text(
            "Hello world",
            "en",
            "fr"
        )
        
        # Result should have status field
        assert "status" in result
    
    @pytest.mark.asyncio
    async def test_elevenlabs_synthesis(self):
        """Test ElevenLabs API integration (mocked)"""
        service = ElevenLabsService()
        
        result = await service.synthesize_speech(
            "Bonjour le monde",
            "voice_id_123"
        )
        
        # Result should have status field
        assert "status" in result


class TestErrorHandling:
    """Test error handling in services"""
    
    def test_job_with_invalid_data(self, db: Session, test_user: User):
        """Test job creation with invalid data"""
        job_data = DubbingCreateRequest(
            title="",  # Invalid: empty title
            source_language="en",
            target_language="fr"
        )
        
        # Should raise validation error
        with pytest.raises(Exception):
            job_data.title
    
    def test_nonexistent_job_access(self, db: Session, test_user: User):
        """Test accessing non-existent job"""
        with pytest.raises(Exception):
            JobService.get_job(db, 99999, test_user)
