"""Health Check Routes"""
from fastapi import APIRouter
from sqlalchemy import text
from app.utils.database import SessionLocal
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/health")
async def health_check():
    """
    Health check endpoint
    """
    return {
        "status": "healthy",
        "service": "VoiceSync AI API",
        "version": "1.0.0"
    }


@router.get("/health/db")
async def database_health():
    """
    Database health check
    """
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
