"""Application Configuration"""
from typing import List
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings from environment variables"""
    
    # Application
    APP_NAME: str = "VoiceSync AI"
    APP_VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    LOG_LEVEL: str = "INFO"
    
    # Database
    DATABASE_URL: str = "postgresql://user:password@db:5432/voicesync_db"
    DATABASE_ECHO: bool = False
    
    # Redis
    REDIS_URL: str = "redis://redis:6379/0"
    REDIS_DECODE_RESPONSES: bool = True
    
    # JWT
    JWT_SECRET_KEY: str = "your-super-secret-key-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION: int = 86400  # 24 hours
    
    # CORS
    CORS_ORIGINS: str = "http://localhost:3000,http://localhost:8000"
    
    # File Upload
    MAX_UPLOAD_SIZE: int = 2147483648  # 2GB
    ALLOWED_VIDEO_FORMATS: List[str] = ["mp4", "mkv", "avi", "mov", "flv", "webm"]
    ALLOWED_AUDIO_FORMATS: List[str] = ["mp3", "wav", "flac", "aac", "ogg"]
    
    # Processing
    MAX_VIDEO_DURATION: int = 3600  # 60 minutes
    DEFAULT_OUTPUT_QUALITY: str = "1080p"
    MAX_CONCURRENT_JOBS: int = 5
    JOB_TIMEOUT: int = 7200  # 2 hours
    
    # API Keys
    OPENAI_API_KEY: str = ""
    ELEVENLABS_API_KEY: str = ""
    DEEPL_API_KEY: str = ""
    WHISPER_API_KEY: str = ""
    
    # AWS
    AWS_ACCESS_KEY_ID: str = ""
    AWS_SECRET_ACCESS_KEY: str = ""
    AWS_REGION: str = "eu-west-1"
    AWS_S3_BUCKET: str = "voicesync-ai-videos"
    
    # Stripe
    STRIPE_SECRET_KEY: str = ""
    STRIPE_WEBHOOK_SECRET: str = ""
    
    # Email
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""
    SMTP_FROM_NAME: str = "VoiceSync AI"
    SMTP_FROM_EMAIL: str = "noreply@voicesync-ai.com"
    
    # Feature Flags
    FEATURE_VOICE_CLONING: bool = True
    FEATURE_REAL_TIME_SYNC: bool = False
    FEATURE_BATCH_PROCESSING: bool = True
    FEATURE_API_ACCESS: bool = True
    FEATURE_MARKETPLACE: bool = False
    
    # Model Configuration
    WHISPER_MODEL_SIZE: str = "base"
    WAV2LIP_MODEL: str = "checkpoints/wav2lip.pth"
    VOICE_CLONING_MODEL: str = "models/voice_cloning.pth"
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()


settings = get_settings()
