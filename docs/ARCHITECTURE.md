# VoiceSync AI - System Architecture

## Overview

VoiceSync AI is a distributed, microservices-based platform for AI-powered video dubbing and lip-synchronization. The system is designed for scalability, reliability, and high performance.

## Architecture Diagram

```
Frontend (React/Next.js) at :3000
           |
           v
    API Gateway/LB
           |
    +------+------+------+------+
    |      |      |      |      |
    v      v      v      v      v
Backend  Redis  Database  S3   Other
:8000   :6379   :5432    Storage Services
    |
    +------+------+------+------+
           |      |      |      |
           v      v      v      v
      Transcribe Translate Voice Lip-Sync
      Service   Service   Synth  Service
      :8001    :8002     :8003
           |
           v
    Celery Task Queue
           |
    +------+------+------+
    |      |      |      |
    v      v      v      v
  Workers Pool (Distributed)
```

## Core Components

### 1. Frontend Layer
- **Technology**: React 18 + Next.js 14
- **Styling**: TailwindCSS
- **State Management**: Zustand
- **API Client**: Axios + React Query
- **Real-time**: WebSocket for live progress
- **Hosted on**: Vercel / Docker

### 2. API Gateway
- **Technology**: FastAPI
- **Language**: Python 3.11
- **Server**: Uvicorn / Gunicorn
- **Port**: 8000
- **Features**:
  - RESTful API design
  - JWT authentication
  - Rate limiting
  - CORS handling
  - Error handling & logging

### 3. Database Layer
- **Primary**: PostgreSQL 15
  - User management
  - Job tracking
  - Pricing & subscriptions
  - Voice profiles
- **Cache**: Redis 7
  - Session management
  - Job queue
  - Rate limiting
  - Temporary data storage

### 4. Microservices

#### Transcription Service (:8001)
- **AI Model**: OpenAI Whisper
- **Input**: Audio file
- **Output**: Text with timestamps
- **Languages**: 99+ languages
- **Accuracy**: 99.5%+

#### Translation Service (:8002)
- **AI Model**: DeepL API
- **Features**:
  - Context-aware translation
  - Sentiment preservation
  - Formality levels
- **Languages**: 50+ languages

#### Voice Synthesis Service (:8003)
- **AI Model**: ElevenLabs / Coqui TTS
- **Features**:
  - 500+ voice actors
  - Emotion preservation
  - Voice cloning capability
  - Multiple accents
- **Output**: High-quality audio (MP3/WAV)

#### Lip Sync Service
- **AI Model**: Wav2Lip
- **Features**:
  - Perfect mouth synchronization
  - Emotion preservation
  - Face detection
  - Video quality up to 4K

### 5. Task Queue & Workers
- **Queue System**: Celery + Redis
- **Worker Pool**: Distributed workers
- **Features**:
  - Asynchronous processing
  - Automatic retries
  - Priority queues
  - Job monitoring
  - Timeout handling

## Data Flow

### Video Dubbing Pipeline

```
1. User Upload
   -> Validate file format & size
   -> Store in S3 uploads
   -> Create job record
   -> Queue processing job

2. Audio Extraction
   -> Extract audio from video
   -> Store temporary audio

3. Transcription
   -> Send to Whisper API
   -> Get transcript with timestamps
   -> Store transcript

4. Translation
   -> Send transcript to DeepL
   -> Get translated text
   -> Maintain timestamps

5. Voice Synthesis
   -> Convert text to speech
   -> Use target language voice
   -> Maintain emotion & tone
   -> Output high-quality audio

6. Lip Synchronization
   -> Use Wav2Lip model
   -> Sync audio with video
   -> Maintain facial expressions
   -> Output synced video

7. Final Processing
   -> Encode to target quality
   -> Add subtitles (optional)
   -> Store in S3 outputs
   -> Update job status
   -> Generate download link

8. User Download
   -> Serve from CDN
   -> Track usage
   -> Update user quota
```

## Performance Targets

| Metric | Target |
|--------|--------|
| API Response Time | < 500ms |
| Video Upload | 50 MB/s |
| Transcription | 10x real-time |
| Translation | Near instant |
| Voice Synthesis | 2x real-time |
| Lip Sync | 5x real-time |
| Overall Processing | < 10 minutes for 1hr video |
| Uptime | 99.9% |
| Error Rate | < 0.1% |

## Technology Stack Summary

| Layer | Technology |
|-------|------------|
| **Frontend** | React 18, Next.js 14, TailwindCSS |
| **Backend** | FastAPI, Python 3.11 |
| **Database** | PostgreSQL 15, Redis 7 |
| **AI/ML** | Whisper, DeepL, ElevenLabs, Wav2Lip |
| **Task Queue** | Celery, Redis |
| **Containerization** | Docker, Docker Compose |
| **Orchestration** | Kubernetes |
| **CI/CD** | GitHub Actions |
| **Cloud** | AWS / Google Cloud |

---

For more details, see the [API Documentation](API.md) and [Setup Guide](SETUP.md).
