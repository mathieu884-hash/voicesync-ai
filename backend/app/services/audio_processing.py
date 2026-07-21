"""Audio Processing Service"""
import logging
from typing import Dict, Optional
import subprocess
import os

logger = logging.getLogger(__name__)


class AudioProcessingService:
    """Service for audio extraction and processing"""
    
    @staticmethod
    def extract_audio_from_video(
        video_path: str,
        output_audio_path: str,
        format: str = "wav"
    ) -> Dict:
        """
        Extract audio from video file using ffmpeg
        """
        try:
            os.makedirs(os.path.dirname(output_audio_path), exist_ok=True)
            
            cmd = [
                "ffmpeg",
                "-i", video_path,
                "-q:a", "9",
                "-n",
                output_audio_path
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300
            )
            
            if result.returncode == 0:
                logger.info(f"Audio extracted successfully: {output_audio_path}")
                return {
                    "audio_path": output_audio_path,
                    "status": "success"
                }
            else:
                logger.error(f"FFmpeg error: {result.stderr}")
                return {
                    "error": result.stderr,
                    "status": "failed"
                }
        
        except subprocess.TimeoutExpired:
            logger.error("Audio extraction timeout")
            return {
                "error": "Audio extraction timeout",
                "status": "failed"
            }
        except Exception as e:
            logger.error(f"Audio extraction error: {str(e)}")
            return {
                "error": str(e),
                "status": "failed"
            }
    
    @staticmethod
    def get_video_duration(video_path: str) -> Optional[float]:
        """
        Get video duration in seconds using ffprobe
        """
        try:
            cmd = [
                "ffprobe",
                "-v", "error",
                "-show_entries", "format=duration",
                "-of", "default=noprint_wrappers=1:nokey=1:nounits=1",
                video_path
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                duration = float(result.stdout.strip())
                logger.info(f"Video duration: {duration} seconds")
                return duration
            else:
                logger.error(f"FFprobe error: {result.stderr}")
                return None
        
        except Exception as e:
            logger.error(f"Error getting video duration: {str(e)}")
            return None
    
    @staticmethod
    def merge_audio_with_video(
        video_path: str,
        audio_path: str,
        output_path: str
    ) -> Dict:
        """
        Merge dubbed audio with original video using ffmpeg
        """
        try:
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            cmd = [
                "ffmpeg",
                "-i", video_path,
                "-i", audio_path,
                "-c:v", "copy",
                "-c:a", "aac",
                "-map", "0:v:0",
                "-map", "1:a:0",
                "-shortest",
                "-n",
                output_path
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=600
            )
            
            if result.returncode == 0:
                logger.info(f"Audio merged with video: {output_path}")
                return {
                    "output_path": output_path,
                    "status": "success"
                }
            else:
                logger.error(f"FFmpeg error: {result.stderr}")
                return {
                    "error": result.stderr,
                    "status": "failed"
                }
        
        except subprocess.TimeoutExpired:
            logger.error("Video merge timeout")
            return {
                "error": "Video merge timeout",
                "status": "failed"
            }
        except Exception as e:
            logger.error(f"Video merge error: {str(e)}")
            return {
                "error": str(e),
                "status": "failed"
            }
    
    @staticmethod
    def convert_audio_format(
        input_path: str,
        output_path: str,
        format: str = "wav"
    ) -> Dict:
        """
        Convert audio to different format
        """
        try:
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            codec_map = {
                "wav": "pcm_s16le",
                "mp3": "libmp3lame",
                "aac": "aac"
            }
            
            codec = codec_map.get(format, "pcm_s16le")
            
            cmd = [
                "ffmpeg",
                "-i", input_path,
                "-c:a", codec,
                "-n",
                output_path
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300
            )
            
            if result.returncode == 0:
                logger.info(f"Audio converted to {format}: {output_path}")
                return {
                    "output_path": output_path,
                    "format": format,
                    "status": "success"
                }
            else:
                logger.error(f"FFmpeg error: {result.stderr}")
                return {
                    "error": result.stderr,
                    "status": "failed"
                }
        
        except Exception as e:
            logger.error(f"Audio conversion error: {str(e)}")
            return {
                "error": str(e),
                "status": "failed"
            }
