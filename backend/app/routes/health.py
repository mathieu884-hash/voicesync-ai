"""Health Check Routes"""
from fastapi import APIRouter, status
from datetime import datetime

router = APIRouter()


@router.get("/health", status_code=status.HTTP_200_OK)
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "VoiceSync AI Backend"
    }


@router.get("/health/live", status_code=status.HTTP_200_OK)
async def liveness_check():
    """Kubernetes liveness probe"""
    return {"status": "live"}


@router.get("/health/ready", status_code=status.HTTP_200_OK)
async def readiness_check():
    """Kubernetes readiness probe"""
    return {"status": "ready"}
