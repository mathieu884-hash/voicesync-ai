# 🎬 VoiceSync AI

**AI-powered video dubbing and lip-sync platform** - Translate and dub movies and series with high-quality voices in 50+ languages.

![Status](https://img.shields.io/badge/status-active-success?style=flat-square)
![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=flat-square)
![Node.js](https://img.shields.io/badge/Node.js-18%2B-green?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)

## 📋 Table of Contents
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Getting Started](#getting-started)
- [Project Structure](#project-structure)
- [API Documentation](#api-documentation)
- [Pricing Plans](#pricing-plans)
- [Contributing](#contributing)
- [License](#license)

## ✨ Features

✅ **Automatic Dubbing** - AI-powered voice generation in 50+ languages
✅ **Lip Synchronization** - Advanced Wav2Lip technology for perfect mouth movements
✅ **Emotion Preservation** - Maintain original voice tonality and emotions
✅ **Multiple Voice Options** - Professional voice profiles (male, female, custom)
✅ **Real-time Processing** - WebSocket streaming for live progress tracking
✅ **Multi-format Support** - MP4, MKV, AVI, MOV, and more
✅ **Premium Quality** - Support for 720p, 1080p, and 4K output
✅ **API Access** - RESTful API for third-party integrations
✅ **Content Protection** - DRM, watermarking, and copyright verification

## 🛠️ Tech Stack

### Frontend
- **React.js / Next.js** - Modern UI framework
- **WebGL** - Audio visualization
- **WebSocket** - Real-time streaming
- **TailwindCSS** - Styling
- **Redux** - State management

### Backend
- **Python 3.9+** - Core dubbing engine
- **FastAPI** - High-performance API
- **Node.js** - Microservices
- **Redis** - Caching layer
- **PostgreSQL** - User data & job storage

### AI/ML Services
- **OpenAI Whisper** - Transcription with timestamps
- **ElevenLabs / Coqui TTS** - Voice synthesis
- **Wav2Lip** - Lip synchronization
- **DeepL / GPT-4** - Contextual translation
- **Hugging Face** - Alternative open-source models

### Infrastructure
- **Docker & Docker Compose** - Containerization
- **Kubernetes** - Orchestration
- **AWS/GCP** - GPU instances for processing
- **GitHub Actions** - CI/CD pipeline
- **CDN** - Content distribution

## 🚀 Getting Started

### Prerequisites
- Docker & Docker Compose (recommended)
- Python 3.9+
- Node.js 18+
- PostgreSQL 13+
- Redis 7+

### Installation

#### Option 1: Docker Compose (Recommended)

```bash
# Clone the repository
git clone https://github.com/mathieu884-hash/voicesync-ai.git
cd voicesync-ai

# Create environment file
cp .env.example .env

# Start all services
docker-compose up -d

# Apply database migrations
docker-compose exec backend python -m alembic upgrade head

# Access the application
# Frontend: http://localhost:3000
# API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

#### Option 2: Manual Setup

**Backend Setup:**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
python -m alembic upgrade head
uvicorn app.main:app --reload
```

**Frontend Setup:**
```bash
cd frontend
npm install
npm run dev
```

## 📁 Project Structure

```
voicesync-ai/
├── backend/                    # Python FastAPI backend
│   ├── app/
│   │   ├── main.py            # FastAPI app entry point
│   │   ├── config.py          # Configuration management
│   │   ├── models/            # Database models
│   │   ├── schemas/           # Pydantic schemas
│   │   ├── routes/            # API endpoints
│   │   ├── services/          # Business logic
│   │   ├── middleware/        # Custom middleware
│   │   └── utils/             # Utility functions
│   ├── dubbing_pipeline/      # Core dubbing engine
│   │   ├── extractor.py       # Audio extraction
│   │   ├── transcriber.py     # Speech-to-text
│   │   ├── translator.py      # Contextual translation
│   │   ├── voice_generator.py # TTS engine
│   │   └── lip_sync.py        # Lip synchronization
│   ├── tests/                 # Unit & integration tests
│   ├── requirements.txt       # Python dependencies
│   ├── Dockerfile            # Docker image
│   └── .env.example          # Environment template
│
├── frontend/                   # React/Next.js frontend
│   ├── app/
│   │   ├── page.tsx          # Home page
│   │   ├── layout.tsx        # Root layout
│   │   ├── dashboard/        # User dashboard
│   │   ├── pricing/          # Pricing page
│   │   └── api/              # API routes
│   ├── components/           # React components
│   │   ├── Upload/           # Video upload
│   │   ├── LanguageSelector/ # Language selection
│   │   ├── VoiceCustomizer/  # Voice settings
│   │   └── Preview/          # Video preview
│   ├── styles/               # TailwindCSS styles
│   ├── utils/                # Helper functions
│   ├── hooks/                # React hooks
│   ├── package.json          # Node dependencies
│   ├── tsconfig.json         # TypeScript config
│   ├── Dockerfile            # Docker image
│   └── .env.example          # Environment template
│
├── services/                   # Microservices
│   ├── transcription/         # Whisper service
│   ├── translation/           # DeepL service
│   └── voice_synthesis/       # TTS service
│
├── ml_models/                 # ML model configs
│   ├── whisper/
│   ├── wav2lip/
│   └── voice_cloning/
│
├── .github/
│   ├── workflows/
│   │   ├── ci.yml            # CI pipeline
│   │   ├── deploy.yml        # Deployment pipeline
│   │   └── tests.yml         # Automated tests
│   └── ISSUE_TEMPLATE/       # Issue templates
│
├── docs/                       # Documentation
│   ├── API.md                # API documentation
│   ├── ARCHITECTURE.md       # System architecture
│   ├── SETUP.md              # Setup guide
│   └── CONTRIBUTING.md       # Contributing guide
│
├── docker-compose.yml        # Multi-container setup
├── .env.example              # Environment variables
├── LICENSE                   # MIT License
└── README.md                 # This file
```

## 🔌 API Documentation

### Base URL
```
http://localhost:8000/api/v1
```

### Authentication
All requests require a Bearer token in the Authorization header:
```
Authorization: Bearer YOUR_API_KEY
```

### Endpoints

#### Create Dubbing Job
```http
POST /dub
Content-Type: application/json

{
  "source_language": "en",
  "target_language": "fr",
  "preserve_voice": true,
  "sync_lips": true,
  "quality": "1080p"
}
```

#### Get Job Status
```http
GET /jobs/{job_id}
```

#### List Available Voices
```http
GET /voices
```

#### Get User Plans
```http
GET /user/plan
```

For complete API documentation, visit: `http://localhost:8000/docs`

## 💰 Pricing Plans

| Plan | Price | Minutes/Month | Languages | Quality | Features |
|------|-------|---------------|-----------|---------|----------|
| **Basic** | €9.99 | 30 | 10 | 720p | Standard dubbing, Subtitles |
| **Pro** | €29.99 | 150 | 30 | 1080p | Premium dubbing, Lip sync, API |
| **Studio** | €99.99 | 600 | 50 | 4K | Custom voices, Batch processing, Support |
| **Enterprise** | Custom | Unlimited | 50+ | 4K+ | On-premise, SLA, Dedicated support |

### Additional Revenue Streams
- **Pay-per-use**: €2.99 per minute
- **Voice Cloning**: €49.99
- **API Access**: Custom pricing
- **White Label**: For dubbing studios

## 🧪 Testing

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test

# End-to-end tests
npm run e2e
```

## 📊 Monitoring & Logs

```bash
# View backend logs
docker-compose logs -f backend

# View frontend logs
docker-compose logs -f frontend

# View all services
docker-compose logs -f
```

## 🤝 Contributing

We welcome contributions! Please read our [CONTRIBUTING.md](docs/CONTRIBUTING.md) guide.

### Development Workflow
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Coding Standards
- Python: PEP 8, type hints required
- JavaScript: ESLint + Prettier
- Commit messages: Conventional commits
- Pull requests: Require 2 approvals before merge

## 📝 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

## 🙋 Support

- 📧 Email: support@voicesync-ai.com
- 💬 Discord: [Join our community](https://discord.gg/voicesync)
- 🐛 Issues: [GitHub Issues](https://github.com/mathieu884-hash/voicesync-ai/issues)
- 📚 Docs: [Full documentation](docs/)

## 🗺️ Roadmap

- [ ] MVP with 5 languages (Q3 2026)
- [ ] Extended language support (50+) (Q4 2026)
- [ ] Mobile app (iOS/Android) (Q1 2027)
- [ ] Real-time streaming support (Q2 2027)
- [ ] Voice marketplace (Q3 2027)
- [ ] Enterprise features (Q4 2027)

## 👥 Team

- **Lead Developer**: Mathieu884
- **Contributors**: [See contributors page](https://github.com/mathieu884-hash/voicesync-ai/graphs/contributors)

---

**Made with ❤️ by the VoiceSync AI Team**
