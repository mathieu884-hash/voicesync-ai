"""Voices Routes"""
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from app.dependencies import get_current_active_user
from app.utils.database import get_db
from app.models.user import User
from app.schemas.job import VoiceResponse, UserVoiceResponse, UserVoiceCreate
from app.services.job import VoiceService
import logging
import os
from datetime import datetime

logger = logging.getLogger(__name__)

router = APIRouter()

# Voice upload directory
UPLOAD_DIR = "uploads/voices"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.get("/", response_model=list[VoiceResponse])
async def list_voices(
    language: str = None,
    gender: str = None,
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """
    List available voices
    
    - **language**: Filter by language code (e.g., "en", "fr")
    - **gender**: Filter by gender (male, female, neutral)
    - **skip**: Number of voices to skip
    - **limit**: Maximum number of voices to return
    """
    try:
        voices = VoiceService.get_voices(db, language, gender, skip, limit)
        return voices
    except Exception as e:
        logger.error(f"Error listing voices: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to list voices"
        )


@router.get("/{voice_id}", response_model=VoiceResponse)
async def get_voice(
    voice_id: str,
    db: Session = Depends(get_db)
):
    """
    Get voice details by ID
    """
    try:
        voice = VoiceService.get_voice(db, voice_id)
        return voice
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting voice: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get voice"
        )


@router.post("/clone", response_model=UserVoiceResponse, status_code=status.HTTP_201_CREATED)
async def clone_voice(
    name: str = Form(...),
    gender: str = Form(None),
    accent: str = Form(None),
    description: str = Form(None),
    audio: UploadFile = File(...),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Clone/create a custom voice from audio sample
    
    - **name**: Name for the cloned voice
    - **gender**: Voice gender
    - **accent**: Accent/region
    - **description**: Voice description
    - **audio**: Audio sample file (15-30 seconds)
    """
    try:
        # Validate file
        if not audio.filename:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No audio file provided"
            )
        
        # Save audio file
        content = await audio.read()
        filename = f"user_{current_user.id}_{datetime.utcnow().timestamp()}_{audio.filename}"
        filepath = os.path.join(UPLOAD_DIR, filename)
        
        with open(filepath, "wb") as f:
            f.write(content)
        
        # Create user voice
        user_voice = VoiceService.create_user_voice(
            db,
            current_user,
            name,
            filepath,
            gender,
            accent,
            description
        )
        
        return user_voice
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error cloning voice: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to clone voice"
        )


@router.get("/user/voices", response_model=list[UserVoiceResponse])
async def get_user_voices(
    skip: int = 0,
    limit: int = 20,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get user's custom cloned voices
    """
    try:
        user_voices = VoiceService.get_user_voices(db, current_user, skip, limit)
        return user_voices
    except Exception as e:
        logger.error(f"Error getting user voices: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get user voices"
        )
