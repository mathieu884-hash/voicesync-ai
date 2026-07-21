# VoiceSync AI - Documentation Complète

## 📖 Table des Matières

1. [Introduction](#introduction)
2. [Architecture](#architecture)
3. [Installation](#installation)
4. [Configuration](#configuration)
5. [API Reference](#api-reference)
6. [Utilisation](#utilisation)
7. [Deployment](#deployment)
8. [Troubleshooting](#troubleshooting)

---

## Introduction

**VoiceSync AI** est une plateforme de dubbing vidéo alimentée par l'IA qui combine:
- 🎤 Transcription audio (OpenAI Whisper)
- 🌐 Traduction multilingue (DeepL)
- 🎵 Synthèse vocale (ElevenLabs)
- 👄 Synchronisation lèvres (Wav2Lip)

### Caractéristiques Principales

✅ Support 50+ langues  
✅ 500+ voix disponibles  
✅ Synchronisation lèvres automatique  
✅ Qualité jusqu'à 4K  
✅ API REST complète  
✅ Traitement asynchrone  
✅ Dashboard utilisateur  

---

## Architecture

### Stack Technologique

```
┌─────────────────────────────────────┐
│         Frontend (React/Vue)        │
└────────────────┬────────────────────┘
                 │
┌────────────────▼────────────────────┐
│      FastAPI Backend (Python)       │
│  ├─ Authentication & Authorization  │
│  ├─ Job Management                  │
│  ├─ Voice Management                │
│  └─ Dubbing Pipeline Orchestration  │
└────────────────┬────────────────────┘
                 │
    ┌────────────┼────────────┐
    │            │            │
┌───▼──┐  ┌─────▼────┐  ┌───▼────┐
│ Celery│  │PostgreSQL│  │ Redis  │
│ Queue │  │ Database │  │ Cache  │
└───┬──┘  └──────────┘  └────────┘
    │
    └─► External APIs
        ├─ OpenAI Whisper
        ├─ DeepL
        ├─ ElevenLabs
        └─ Wav2Lip
```

### Architecture du Pipeline

```
1. Extract Audio (FFmpeg)
   ↓
2. Transcribe (Whisper API)
   ↓
3. Translate (DeepL API)
   ↓
4. Synthesize (ElevenLabs API)
   ↓
5. Sync Lips (Wav2Lip Model)
   ↓
6. Merge Video (FFmpeg)
   ↓
Final Output
```

---

## Installation

### Prérequis

- Python 3.11+
- PostgreSQL 15+
- Redis 7+
- FFmpeg & FFprobe
- Docker & Docker Compose (optionnel)

### Installation Locale

```bash
# 1. Cloner le repository
git clone https://github.com/yourusername/voicesync-ai.git
cd voicesync-ai

# 2. Créer un environnement virtuel
python -m venv venv
source venv/bin/activate  # Sur Windows: venv\Scripts\activate

# 3. Installer les dépendances
pip install -r requirements.txt
pip install -r requirements-dev.txt

# 4. Configurer les variables d'environnement
cp .env.example .env
# Éditer .env avec vos clés API

# 5. Initialiser la base de données
alembic upgrade head

# 6. Lancer le serveur de développement
uvicorn app.main:app --reload
```

### Installation avec Docker

```bash
# 1. Build les images
docker-compose build

# 2. Lancer les services
docker-compose up -d

# 3. Initialiser la base de données
docker-compose exec web alembic upgrade head

# 4. Créer un superuser (optionnel)
docker-compose exec web python -m app.scripts.create_superuser
```

---

## Configuration

### Variables d'Environnement

Créer un fichier `.env` à la racine:

```env
# Application
APP_NAME=VoiceSync AI
ENVIRONMENT=development
DEBUG=True
SECRET_KEY=your-secret-key-here

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/voicesync

# Redis
REDIS_URL=redis://localhost:6379/0
CELERY_BROKER_URL=redis://localhost:6379/1
CELERY_RESULT_BACKEND=redis://localhost:6379/2

# JWT
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# External APIs
OPENAI_API_KEY=sk_test_xxxxx
DEEPL_API_KEY=xxxxx
DEEPL_PRO=False
ELEVENLABS_API_KEY=xxxxx
WAV2LIP_MODEL_PATH=/path/to/wav2lip.pth

# CORS
CORS_ORIGINS=http://localhost:3000,http://localhost:8000

# File Upload
MAX_UPLOAD_SIZE=2147483648  # 2GB
UPLOAD_DIR=uploads
```

---

## API Reference

### Authentication Endpoints

#### Register User
```http
POST /api/v1/auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "username": "username",
  "full_name": "Full Name",
  "password": "SecurePassword123"
}

Response: 201 Created
{
  "id": 1,
  "email": "user@example.com",
  "username": "username",
  "full_name": "Full Name"
}
```

#### Login
```http
POST /api/v1/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "SecurePassword123"
}

Response: 200 OK
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer"
}
```

#### Get Profile
```http
GET /api/v1/auth/me
Authorization: Bearer {access_token}

Response: 200 OK
{
  "id": 1,
  "email": "user@example.com",
  "username": "username",
  "full_name": "Full Name",
  "is_active": true,
  "created_at": "2024-01-01T00:00:00Z"
}
```

### Dubbing Endpoints

#### Create Dubbing Job
```http
POST /api/v1/dubbing/create
Authorization: Bearer {access_token}
Content-Type: multipart/form-data

FormData:
- title: "My Video"
- description: "Video description"
- source_language: "en"
- target_language: "fr"
- video_quality: "1080p"
- preserve_voice: true
- sync_lips: true
- voice_id: "voice_123" (optional)
- video: <file>

Response: 201 Created
{
  "job_id": 123,
  "status": "queued",
  "created_at": "2024-01-01T00:00:00Z",
  "estimated_duration": 300,
  "message": "Dubbing job created successfully"
}
```

#### Get Job Details
```http
GET /api/v1/jobs/{job_id}
Authorization: Bearer {access_token}

Response: 200 OK
{
  "id": 123,
  "title": "My Video",
  "status": "processing",
  "progress": 50,
  "source_language": "en",
  "target_language": "fr",
  "created_at": "2024-01-01T00:00:00Z",
  "estimated_duration": 300,
  "segments": [...]
}
```

#### List Jobs
```http
GET /api/v1/jobs?skip=0&limit=10&status=processing
Authorization: Bearer {access_token}

Response: 200 OK
[
  {
    "id": 123,
    "title": "My Video",
    "status": "processing",
    "progress": 50,
    "created_at": "2024-01-01T00:00:00Z"
  },
  ...
]
```

#### Cancel Job
```http
POST /api/v1/dubbing/cancel/{job_id}
Authorization: Bearer {access_token}

Response: 200 OK
{
  "job_id": 123,
  "status": "cancelled",
  "message": "Job 123 cancelled successfully"
}
```

### Voices Endpoints

#### List Available Voices
```http
GET /api/v1/voices?language=en&gender=female&skip=0&limit=50

Response: 200 OK
[
  {
    "id": "voice_123",
    "name": "Sarah",
    "language": "en",
    "gender": "female",
    "quality": "premium",
    "cost_per_minute": 0.50,
    "preview_audio_url": "https://..."
  },
  ...
]
```

#### Clone Voice
```http
POST /api/v1/voices/clone
Authorization: Bearer {access_token}
Content-Type: multipart/form-data

FormData:
- name: "My Voice"
- gender: "male"
- accent: "British"
- description: "My voice clone"
- audio: <file>

Response: 201 Created
{
  "id": 1,
  "name": "My Voice",
  "status": "processing",
  "created_at": "2024-01-01T00:00:00Z"
}
```

---

## Utilisation

### Workflow Complet

1. **Authentification**
```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "password"}'
```

2. **Créer un Job de Dubbing**
```bash
curl -X POST http://localhost:8000/api/v1/dubbing/create \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "title=My Video" \
  -F "source_language=en" \
  -F "target_language=fr" \
  -F "sync_lips=true" \
  -F "video=@movie.mp4"
```

3. **Suivi de la Progression**
```bash
curl -X GET http://localhost:8000/api/v1/jobs/1 \
  -H "Authorization: Bearer YOUR_TOKEN"
```

4. **Télécharger le Résultat**
```bash
curl -X GET http://localhost:8000/api/v1/jobs/1/download \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -o dubbed_video.mp4
```

---

## Deployment

### Deployment sur AWS

#### 1. Créer les ressources AWS

```bash
# Créer une instance EC2
aws ec2 run-instances \
  --image-id ami-0c55b159cbfafe1f0 \
  --instance-type t3.medium \
  --key-name your-key-pair \
  --security-groups default

# Créer une RDS PostgreSQL
aws rds create-db-instance \
  --db-instance-identifier voicesync-db \
  --db-instance-class db.t3.micro \
  --engine postgres \
  --master-username admin \
  --allocated-storage 100

# Créer un ElastiCache Redis
aws elasticache create-cache-cluster \
  --cache-cluster-id voicesync-redis \
  --cache-node-type cache.t3.micro \
  --engine redis
```

#### 2. Configurer l'Instance EC2

```bash
# Se connecter à l'instance
ssh -i your-key-pair.pem ubuntu@your-instance-ip

# Installer les dépendances
sudo apt-get update
sudo apt-get install -y python3.11 python3.11-venv postgresql-client redis-tools
sudo apt-get install -y ffmpeg

# Cloner le repository
git clone https://github.com/yourusername/voicesync-ai.git
cd voicesync-ai

# Configurer l'environnement
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Configurer les variables d'environnement
nano .env
```

#### 3. Configurer Nginx

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static/ {
        alias /home/ubuntu/voicesync-ai/static/;
    }
}
```

#### 4. Configurer Systemd Services

**FastAPI Service** (`/etc/systemd/system/voicesync-api.service`):
```ini
[Unit]
Description=VoiceSync AI API
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/voicesync-ai
ExecStart=/home/ubuntu/voicesync-ai/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000
Restart=always
Environment="PATH=/home/ubuntu/voicesync-ai/venv/bin"

[Install]
WantedBy=multi-user.target
```

**Celery Worker** (`/etc/systemd/system/voicesync-worker.service`):
```ini
[Unit]
Description=VoiceSync AI Celery Worker
After=network.target redis-server.service

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/voicesync-ai
ExecStart=/home/ubuntu/voicesync-ai/venv/bin/celery -A app.tasks worker -l info
Restart=always
Environment="PATH=/home/ubuntu/voicesync-ai/venv/bin"

[Install]
WantedBy=multi-user.target
```

```bash
# Activer les services
sudo systemctl enable voicesync-api
sudo systemctl enable voicesync-worker
sudo systemctl start voicesync-api
sudo systemctl start voicesync-worker
```

### Deployment avec Docker

```bash
# Build l'image
docker build -t voicesync-ai:latest .

# Push vers ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com
docker tag voicesync-ai:latest YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/voicesync-ai:latest
docker push YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/voicesync-ai:latest

# Deploy avec ECS
aws ecs create-service \
  --cluster voicesync-cluster \
  --service-name voicesync-api \
  --task-definition voicesync-task:1 \
  --desired-count 2
```

---

## Troubleshooting

### Erreurs Courantes

#### 1. Erreur de connexion à la base de données
```
ERROR: could not translate host name "localhost" to address: Name or service not known
```
**Solution:**
- Vérifier que PostgreSQL est en cours d'exécution
- Vérifier la variable `DATABASE_URL` dans `.env`
- Tester la connexion: `psql -U user -d voicesync -h localhost`

#### 2. Erreur API OpenAI
```
AuthenticationError: Incorrect API key provided
```
**Solution:**
- Vérifier la clé API dans `.env`
- Vérifier les limites de quota
- Tester avec: `curl -H "Authorization: Bearer $OPENAI_API_KEY" https://api.openai.com/v1/models`

#### 3. Timeout du traitement
```
TimeoutError: Task took too long to execute
```
**Solution:**
- Augmenter les timeouts Celery
- Vérifier les ressources serveur (CPU, RAM)
- Scaler les workers Celery

#### 4. Erreur d'extraction audio
```
FFmpeg error: cannot find ffmpeg
```
**Solution:**
- Installer FFmpeg: `sudo apt-get install ffmpeg`
- Vérifier le chemin: `which ffmpeg`
- Tester: `ffmpeg -version`

---

## Support

- 📧 Email: support@voicesync-ai.com
- 💬 Discord: https://discord.gg/voicesync
- 🐛 Issues: https://github.com/yourusername/voicesync-ai/issues
- 📚 Docs: https://docs.voicesync-ai.com

---

**Dernière mise à jour:** 2024-01-01  
**Version:** 1.0.0
