"""Tests for Voice Service"""
import pytest
from sqlalchemy.orm import Session
from app.models.job import Voice, UserVoice
from app.models.user import User
from app.services.job import VoiceService
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
        email="voicetest@example.com",
        username="voicetest",
        full_name="Voice Test User",
        password="TestPassword123"
    )
    return AuthService.register_user(db, user_data)


class TestVoiceRetrieval:
    """Test voice retrieval"""
    
    def test_get_voices(self, db: Session):
        """Test getting available voices"""
        voices = VoiceService.get_voices(db)
        
        assert isinstance(voices, list)
    
    def test_get_voices_by_language(self, db: Session):
        """Test filtering voices by language"""
        voices = VoiceService.get_voices(db, language="en")
        
        assert isinstance(voices, list)
        for voice in voices:
            assert voice.language == "en"
    
    def test_get_voices_by_gender(self, db: Session):
        """Test filtering voices by gender"""
        voices = VoiceService.get_voices(db, gender="female")
        
        assert isinstance(voices, list)
        for voice in voices:
            assert voice.gender == "female"


class TestUserVoiceCreation:
    """Test user voice creation"""
    
    def test_create_user_voice(self, db: Session, test_user: User):
        """Test creating a user voice"""
        user_voice = VoiceService.create_user_voice(
            db,
            test_user,
            "My Custom Voice",
            "/path/to/sample.wav",
            gender="male",
            accent="British",
            description="My voice clone"
        )
        
        assert user_voice.user_id == test_user.id
        assert user_voice.name == "My Custom Voice"
        assert user_voice.status == "processing"
    
    def test_get_user_voices(self, db: Session, test_user: User):
        """Test retrieving user's voices"""
        VoiceService.create_user_voice(
            db,
            test_user,
            "Voice 1",
            "/path/to/sample1.wav"
        )
        
        VoiceService.create_user_voice(
            db,
            test_user,
            "Voice 2",
            "/path/to/sample2.wav"
        )
        
        user_voices = VoiceService.get_user_voices(db, test_user)
        
        assert len(user_voices) >= 2
        for voice in user_voices:
            assert voice.user_id == test_user.id
