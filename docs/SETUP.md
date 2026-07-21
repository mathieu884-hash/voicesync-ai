# VoiceSync AI - Setup Guide

## Prerequisites

- **Docker** & **Docker Compose** (recommended)
- **Python 3.9+** (for development)
- **Node.js 18+** (for frontend development)
- **PostgreSQL 13+** (if running without Docker)
- **Redis 7+** (for caching)

## Quick Start with Docker

### 1. Clone the Repository

```bash
git clone https://github.com/mathieu884-hash/voicesync-ai.git
cd voicesync-ai
```

### 2. Configure Environment

```bash
cp .env.example .env
```

Edit `.env` and add your API keys:
- `OPENAI_API_KEY` - Get from [OpenAI](https://platform.openai.com)
- `ELEVENLABS_API_KEY` - Get from [ElevenLabs](https://elevenlabs.io)
- `DEEPL_API_KEY` - Get from [DeepL](https://www.deepl.com)
- `STRIPE_SECRET_KEY` - Get from [Stripe](https://stripe.com)

### 3. Start the Application

```bash
docker-compose up -d
```

This will start:
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **pgAdmin**: http://localhost:5050 (user: admin@voicesync-ai.com, password: admin)
- **Redis Commander**: http://localhost:8081

### 4. Initialize Database

```bash
docker-compose exec backend python -m alembic upgrade head
```

### 5. Create a Test User

```bash
docker-compose exec backend python scripts/create_test_user.py
```

## Manual Setup (Without Docker)

### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Run migrations
python -m alembic upgrade head

# Start server
uvicorn app.main:app --reload
```

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

### Services Setup

Each microservice can be started independently:

```bash
# Terminal 1: Transcription service
cd services/transcription
python app.py

# Terminal 2: Translation service
cd services/translation
python app.py

# Terminal 3: Voice synthesis service
cd services/voice_synthesis
python app.py
```

## Database Setup

### PostgreSQL Connection

```bash
# Using psql
psql -U voicesync_user -d voicesync_db -h localhost

# Or using Docker
docker-compose exec db psql -U voicesync_user -d voicesync_db
```

### Run Migrations

```bash
cd backend
python -m alembic upgrade head
```

### Create Initial Data

```bash
docker-compose exec backend python scripts/seed_db.py
```

## Configuration

### Environment Variables

Key variables in `.env`:

```bash
# Application
ENVIRONMENT=development
DEBUG=true

# Database
DATABASE_URL=postgresql://user:password@localhost/voicesync_db

# Redis
REDIS_URL=redis://localhost:6379/0

# API Keys
OPENAI_API_KEY=sk_...
ELEVENLABS_API_KEY=...
DEEPL_API_KEY=...
```

### API Configuration

Edit `backend/app/config.py` for:
- Supported languages
- Quality settings
- Processing timeouts
- Rate limits

## Verification

### Health Checks

```bash
# Backend
curl http://localhost:8000/health

# Frontend
curl http://localhost:3000
```

### API Documentation

Visit http://localhost:8000/docs for interactive API documentation (Swagger UI).

## Development Commands

```bash
# Using Make
make help              # Show available commands
make build            # Build Docker images
make up               # Start containers
make down             # Stop containers
make logs             # View logs
make test             # Run tests
make lint             # Run linters
make format           # Format code
make migrate          # Run database migrations

# Using Docker Compose
docker-compose ps                    # List containers
docker-compose logs -f              # View logs
docker-compose exec backend bash    # Access container shell
docker-compose down -v              # Stop and remove volumes
```

## Troubleshooting

### Port Already in Use

```bash
# Linux/Mac
lsof -i :3000
lsof -i :8000

# Windows
netstat -ano | findstr :3000
netstat -ano | findstr :8000

# Kill process
kill -9 <PID>
```

### Database Connection Issues

```bash
# Check PostgreSQL is running
docker-compose ps db

# Restart database
docker-compose restart db

# View database logs
docker-compose logs db
```

### Redis Connection Issues

```bash
# Test Redis connection
docker-compose exec redis redis-cli ping

# View Redis logs
docker-compose logs redis
```

### Permission Denied

```bash
# Make scripts executable
chmod +x scripts/*.sh

# Or run with bash
bash scripts/setup.sh
```

## Next Steps

1. **Read the API Documentation**: http://localhost:8000/docs
2. **Explore the Dashboard**: http://localhost:3000
3. **Check the Contributing Guide**: [docs/CONTRIBUTING.md](CONTRIBUTING.md)
4. **Review the Architecture**: [docs/ARCHITECTURE.md](ARCHITECTURE.md)
5. **Join our Community**: [Discord](https://discord.gg/voicesync)

## Getting Help

- 📖 [Documentation](../README.md)
- 🐛 [Report Issues](https://github.com/mathieu884-hash/voicesync-ai/issues)
- 💬 [Discord Community](https://discord.gg/voicesync)
- 📧 Email: support@voicesync-ai.com
