"""Health checks and monitoring"""

from fastapi import APIRouter
from sqlalchemy import text
from app.utils.database import SessionLocal
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/health")
async def health_check():
    """Service health check"""
    return {
        "status": "healthy",
        "service": "VoiceSync AI API",
        "version": "1.0.0",
        "timestamp": "2024-01-01T00:00:00Z"
    }


@router.get("/health/db")
async def database_health():
    """Database connectivity check"""
    try:
        db = SessionLocal()
        result = db.execute(text("SELECT 1"))
        db.close()
        
        return {
            "status": "healthy",
            "database": "PostgreSQL",
            "connection": "OK"
        }
    except Exception as e:
        logger.error(f"Database health check failed: {str(e)}")
        return {
            "status": "unhealthy",
            "database": "PostgreSQL",
            "error": str(e)
        }


@router.get("/health/redis")
async def redis_health():
    """Redis connectivity check"""
    try:
        import redis
        from app.config import settings
        
        r = redis.from_url(settings.REDIS_URL)
        r.ping()
        
        return {
            "status": "healthy",
            "cache": "Redis",
            "connection": "OK"
        }
    except Exception as e:
        logger.error(f"Redis health check failed: {str(e)}")
        return {
            "status": "unhealthy",
            "cache": "Redis",
            "error": str(e)
        }
