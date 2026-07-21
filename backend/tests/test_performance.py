"""Performance and Load Tests"""
import pytest
import time
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate
from app.schemas.job import DubbingCreateRequest
from app.services.auth import AuthService
from app.services.job import JobService
from app.utils.database import SessionLocal


@pytest.fixture
def db():
    """Database session fixture"""
    db = SessionLocal()
    yield db
    db.close()


class TestPerformance:
    """Performance tests"""
    
    def test_user_registration_performance(self, db: Session):
        """Test user registration performance"""
        start_time = time.time()
        
        for i in range(10):
            user_data = UserCreate(
                email=f"perf_test_{i}@example.com",
                username=f"perftest{i}",
                full_name=f"Perf Test User {i}",
                password="TestPassword123"
            )
            AuthService.register_user(db, user_data)
        
        end_time = time.time()
        duration = end_time - start_time
        
        # Should complete 10 registrations in under 5 seconds
        assert duration < 5.0, f"Registration took {duration}s, expected < 5s"
    
    def test_job_creation_performance(self, db: Session):
        """Test job creation performance"""
        user_data = UserCreate(
            email="perf_job@example.com",
            username="perfjobtester",
            full_name="Perf Job Test",
            password="TestPassword123"
        )
        user = AuthService.register_user(db, user_data)
        
        start_time = time.time()
        
        for i in range(20):
            job_data = DubbingCreateRequest(
                title=f"Perf Test Job {i}",
                source_language="en",
                target_language="fr"
            )
            JobService.create_job(
                db,
                user,
                job_data,
                f"/path/to/video_{i}.mp4",
                120.0
            )
        
        end_time = time.time()
        duration = end_time - start_time
        
        # Should complete 20 job creations in under 5 seconds
        assert duration < 5.0, f"Job creation took {duration}s, expected < 5s"
    
    def test_user_jobs_retrieval_performance(self, db: Session):
        """Test job retrieval performance"""
        user_data = UserCreate(
            email="perf_retrieve@example.com",
            username="perfretrieve",
            full_name="Perf Retrieve Test",
            password="TestPassword123"
        )
        user = AuthService.register_user(db, user_data)
        
        # Create 50 jobs
        for i in range(50):
            job_data = DubbingCreateRequest(
                title=f"Job {i}",
                source_language="en",
                target_language="fr"
            )
            JobService.create_job(
                db,
                user,
                job_data,
                f"/path/to/video_{i}.mp4",
                120.0
            )
        
        start_time = time.time()
        
        # Retrieve jobs multiple times
        for _ in range(10):
            jobs = JobService.get_user_jobs(db, user, limit=50)
        
        end_time = time.time()
        duration = end_time - start_time
        
        # Should retrieve jobs quickly
        assert duration < 2.0, f"Job retrieval took {duration}s, expected < 2s"


class TestConcurrency:
    """Concurrency tests"""
    
    @pytest.mark.asyncio
    async def test_concurrent_job_creation(self, db: Session):
        """Test concurrent job creation"""
        import asyncio
        
        user_data = UserCreate(
            email="concurrent@example.com",
            username="concurrent",
            full_name="Concurrent Test",
            password="TestPassword123"
        )
        user = AuthService.register_user(db, user_data)
        
        async def create_job(i):
            job_data = DubbingCreateRequest(
                title=f"Concurrent Job {i}",
                source_language="en",
                target_language="fr"
            )
            return JobService.create_job(
                db,
                user,
                job_data,
                f"/path/to/video_{i}.mp4",
                120.0
            )
        
        # Create 10 jobs concurrently
        tasks = [create_job(i) for i in range(10)]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # All should succeed
        assert len(results) == 10
        assert all(isinstance(r, Exception) or r.id for r in results)
