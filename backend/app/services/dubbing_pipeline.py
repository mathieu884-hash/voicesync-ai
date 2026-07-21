"""Dubbing Pipeline Service"""
from sqlalchemy.orm import Session
from app.models.user import User
from app.models.job import Job, JobStatus
from app.services.external_apis import WhisperService, DeepLService, ElevenLabsService, Wav2LipService
from app.services.audio_processing import AudioProcessingService
import logging
import os
from datetime import datetime

logger = logging.getLogger(__name__)


class DubbingPipelineService:
    """Orchestrates the complete dubbing pipeline"""
    
    def __init__(self):
        self.whisper = WhisperService()
        self.deepl = DeepLService()
        self.elevenlabs = ElevenLabsService()
        self.wav2lip = Wav2LipService()
        self.audio_processor = AudioProcessingService()
    
    async def process_dubbing_job(
        self,
        db: Session,
        job: Job,
        user: User
    ) -> dict:
        """
        Execute complete dubbing pipeline for a job
        """
        try:
            logger.info(f"Step 1/6: Extracting audio from job {job.id}")
            from app.services.job import JobService
            JobService.update_job_status(db, job, JobStatus.PROCESSING, progress=10)
            
            audio_path = os.path.join("temp", f"job_{job.id}", "original_audio.wav")
            extract_result = self.audio_processor.extract_audio_from_video(
                job.input_video_path,
                audio_path
            )
            
            if extract_result["status"] != "success":
                raise Exception(f"Audio extraction failed: {extract_result.get('error')}")
            
            logger.info(f"Step 2/6: Transcribing audio for job {job.id}")
            JobService.update_job_status(db, job, JobStatus.PROCESSING, progress=20)
            
            transcription_result = await self.whisper.transcribe_audio(
                audio_path,
                language=job.source_language
            )
            
            if transcription_result["status"] != "success":
                raise Exception(f"Transcription failed: {transcription_result.get('error')}")
            
            original_text = transcription_result.get("text")
            
            logger.info(f"Step 3/6: Translating text for job {job.id}")
            JobService.update_job_status(db, job, JobStatus.PROCESSING, progress=30)
            
            translation_result = await self.deepl.translate_text(
                original_text,
                job.source_language,
                job.target_language
            )
            
            if translation_result["status"] != "success":
                raise Exception(f"Translation failed: {translation_result.get('error')}")
            
            translated_text = translation_result.get("translated_text")
            
            logger.info(f"Step 4/6: Synthesizing speech for job {job.id}")
            JobService.update_job_status(db, job, JobStatus.PROCESSING, progress=40)
            
            voice_id = job.voice_id or "default_voice"
            
            synthesis_result = await self.elevenlabs.synthesize_speech(
                translated_text,
                voice_id
            )
            
            if synthesis_result["status"] != "success":
                raise Exception(f"Speech synthesis failed: {synthesis_result.get('error')}")
            
            dubbed_audio_path = os.path.join("temp", f"job_{job.id}", "dubbed_audio.wav")
            os.makedirs(os.path.dirname(dubbed_audio_path), exist_ok=True)
            
            with open(dubbed_audio_path, "wb") as f:
                f.write(synthesis_result.get("audio_data"))
            
            if job.sync_lips:
                logger.info(f"Step 5/6: Synchronizing lips for job {job.id}")
                JobService.update_job_status(db, job, JobStatus.PROCESSING, progress=60)
                
                synced_video_path = os.path.join("temp", f"job_{job.id}", "synced_video.mp4")
                
                sync_result = await self.wav2lip.sync_video(
                    job.input_video_path,
                    dubbed_audio_path,
                    synced_video_path
                )
                
                if sync_result["status"] != "success":
                    logger.warning(f"Lip sync failed, using dubbed audio only")
                    video_with_audio = job.input_video_path
                else:
                    video_with_audio = synced_video_path
            else:
                video_with_audio = job.input_video_path
            
            logger.info(f"Step 6/6: Merging audio with video for job {job.id}")
            JobService.update_job_status(db, job, JobStatus.PROCESSING, progress=80)
            
            output_path = os.path.join("outputs", f"job_{job.id}", f"{job.title}_dubbed.mp4")
            
            merge_result = self.audio_processor.merge_audio_with_video(
                video_with_audio,
                dubbed_audio_path,
                output_path
            )
            
            if merge_result["status"] != "success":
                raise Exception(f"Video merge failed: {merge_result.get('error')}")
            
            job.output_video_path = output_path
            
            logger.info(f"Dubbing pipeline completed successfully for job {job.id}")
            JobService.update_job_status(db, job, JobStatus.COMPLETED, progress=100)
            
            return {
                "job_id": job.id,
                "output_path": output_path,
                "status": "success",
                "message": "Dubbing completed successfully"
            }
        
        except Exception as e:
            logger.error(f"Dubbing pipeline error for job {job.id}: {str(e)}")
            from app.services.job import JobService
            JobService.update_job_status(
                db,
                job,
                JobStatus.FAILED,
                error_message=str(e)
            )
            
            return {
                "job_id": job.id,
                "error": str(e),
                "status": "failed",
                "message": "Dubbing pipeline failed"
            }
