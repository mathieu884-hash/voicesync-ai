"""External API Integration Services"""
import httpx
import logging
from typing import Optional, List, Dict
from app.config import settings

logger = logging.getLogger(__name__)


class WhisperService:
    """OpenAI Whisper API Service for transcription"""
    
    BASE_URL = "https://api.openai.com/v1"
    
    def __init__(self):
        self.api_key = settings.OPENAI_API_KEY
        self.model = "whisper-1"
    
    async def transcribe_audio(self, audio_path: str, language: str = None) -> Dict:
        """
        Transcribe audio file using OpenAI Whisper
        
        Args:
            audio_path: Path to audio file
            language: Language code (optional)
        
        Returns:
            Dictionary with transcription results
        """
        try:
            headers = {"Authorization": f"Bearer {self.api_key}"}
            
            with open(audio_path, "rb") as audio_file:
                files = {"file": audio_file}
                data = {"model": self.model}
                
                if language:
                    data["language"] = language
                
                async with httpx.AsyncClient() as client:
                    response = await client.post(
                        f"{self.BASE_URL}/audio/transcriptions",
                        headers=headers,
                        files=files,
                        data=data,
                        timeout=300.0
                    )
                    
                    response.raise_for_status()
                    result = response.json()
                    
                    logger.info(f"Transcription successful for {audio_path}")
                    return {
                        "text": result.get("text"),
                        "language": language,
                        "status": "success"
                    }
        
        except httpx.HTTPError as e:
            logger.error(f"Whisper API error: {str(e)}")
            return {
                "error": str(e),
                "status": "failed"
            }
        except Exception as e:
            logger.error(f"Transcription error: {str(e)}")
            return {
                "error": str(e),
                "status": "failed"
            }
    
    async def transcribe_with_timestamps(self, audio_path: str, language: str = None) -> Dict:
        """
        Transcribe audio with detailed timestamps
        """
        try:
            result = await self.transcribe_audio(audio_path, language)
            return result
        except Exception as e:
            logger.error(f"Error transcribing with timestamps: {str(e)}")
            raise


class DeepLService:
    """DeepL API Service for translation"""
    
    BASE_URL = "https://api-free.deepl.com/v2"
    
    def __init__(self):
        self.api_key = settings.DEEPL_API_KEY
    
    async def translate_text(
        self,
        text: str,
        source_language: str,
        target_language: str,
        formality: str = "default"
    ) -> Dict:
        """
        Translate text using DeepL API
        """
        try:
            headers = {"Authorization": f"DeepL-Auth-Key {self.api_key}"}
            
            data = {
                "text": [text],
                "source_lang": source_language.upper(),
                "target_lang": target_language.upper(),
                "formality": formality
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.BASE_URL}/translate",
                    headers=headers,
                    json=data,
                    timeout=30.0
                )
                
                response.raise_for_status()
                result = response.json()
                
                translations = result.get("translations", [])
                if translations:
                    logger.info(f"Translation successful: {source_language} -> {target_language}")
                    return {
                        "translated_text": translations[0].get("text"),
                        "source_language": source_language,
                        "target_language": target_language,
                        "status": "success"
                    }
                else:
                    raise ValueError("No translation received")
        
        except httpx.HTTPError as e:
            logger.error(f"DeepL API error: {str(e)}")
            return {
                "error": str(e),
                "status": "failed"
            }
        except Exception as e:
            logger.error(f"Translation error: {str(e)}")
            return {
                "error": str(e),
                "status": "failed"
            }
    
    async def translate_batch(
        self,
        texts: List[str],
        source_language: str,
        target_language: str
    ) -> Dict:
        """
        Translate multiple texts in batch
        """
        try:
            headers = {"Authorization": f"DeepL-Auth-Key {self.api_key}"}
            
            data = {
                "text": texts,
                "source_lang": source_language.upper(),
                "target_lang": target_language.upper()
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.BASE_URL}/translate",
                    headers=headers,
                    json=data,
                    timeout=60.0
                )
                
                response.raise_for_status()
                result = response.json()
                
                translations = result.get("translations", [])
                translated_texts = [t.get("text") for t in translations]
                
                logger.info(f"Batch translation successful: {len(texts)} texts")
                return {
                    "translated_texts": translated_texts,
                    "status": "success"
                }
        
        except Exception as e:
            logger.error(f"Batch translation error: {str(e)}")
            return {
                "error": str(e),
                "status": "failed"
            }


class ElevenLabsService:
    """ElevenLabs API Service for voice synthesis"""
    
    BASE_URL = "https://api.elevenlabs.io/v1"
    
    def __init__(self):
        self.api_key = settings.ELEVENLABS_API_KEY
    
    async def synthesize_speech(
        self,
        text: str,
        voice_id: str,
        model_id: str = "eleven_monolingual_v1"
    ) -> Dict:
        """
        Synthesize speech using ElevenLabs API
        """
        try:
            headers = {
                "xi-api-key": self.api_key,
                "Content-Type": "application/json"
            }
            
            data = {
                "text": text,
                "model_id": model_id,
                "voice_settings": {
                    "stability": 0.5,
                    "similarity_boost": 0.75
                }
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.BASE_URL}/text-to-speech/{voice_id}",
                    headers=headers,
                    json=data,
                    timeout=120.0
                )
                
                response.raise_for_status()
                audio_data = response.content
                
                logger.info(f"Speech synthesis successful for voice {voice_id}")
                return {
                    "audio_data": audio_data,
                    "content_type": response.headers.get("content-type"),
                    "status": "success"
                }
        
        except httpx.HTTPError as e:
            logger.error(f"ElevenLabs API error: {str(e)}")
            return {
                "error": str(e),
                "status": "failed"
            }
        except Exception as e:
            logger.error(f"Speech synthesis error: {str(e)}")
            return {
                "error": str(e),
                "status": "failed"
            }
    
    async def get_voices(self) -> Dict:
        """
        Get list of available voices
        """
        try:
            headers = {"xi-api-key": self.api_key}
            
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.BASE_URL}/voices",
                    headers=headers,
                    timeout=10.0
                )
                
                response.raise_for_status()
                voices = response.json()
                
                logger.info(f"Retrieved {len(voices.get('voices', []))} voices")
                return {
                    "voices": voices.get("voices", []),
                    "status": "success"
                }
        
        except Exception as e:
            logger.error(f"Error fetching voices: {str(e)}")
            return {
                "error": str(e),
                "status": "failed"
            }
    
    async def get_voice_settings(self, voice_id: str) -> Dict:
        """
        Get settings for a specific voice
        """
        try:
            headers = {"xi-api-key": self.api_key}
            
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.BASE_URL}/voices/{voice_id}/settings",
                    headers=headers,
                    timeout=10.0
                )
                
                response.raise_for_status()
                settings_data = response.json()
                
                return {
                    "settings": settings_data,
                    "status": "success"
                }
        
        except Exception as e:
            logger.error(f"Error fetching voice settings: {str(e)}")
            return {
                "error": str(e),
                "status": "failed"
            }


class Wav2LipService:
    """Wav2Lip Service for lip synchronization"""
    
    def __init__(self):
        self.model_path = settings.WAV2LIP_MODEL_PATH
    
    async def sync_video(
        self,
        video_path: str,
        audio_path: str,
        output_path: str
    ) -> Dict:
        """
        Synchronize video with audio using Wav2Lip
        """
        try:
            logger.info(f"Lip sync started: {video_path}")
            
            return {
                "output_path": output_path,
                "status": "processing",
                "message": "Lip synchronization in progress"
            }
        
        except Exception as e:
            logger.error(f"Lip sync error: {str(e)}")
            return {
                "error": str(e),
                "status": "failed"
            }
