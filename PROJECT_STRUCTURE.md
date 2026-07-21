# VoiceSync AI

## Project Structure

```
voicesync-ai/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── dependencies.py
│   │   ├── models/
│   │   │   ├── user.py
│   │   │   ├── job.py
│   │   │   └── __init__.py
│   │   ├── schemas/
│   │   │   ├── user.py
│   │   │   ├── job.py
│   │   │   └── __init__.py
│   │   ├── services/
│   │   │   ├── auth.py
│   │   │   ├── job.py
│   │   │   ├── external_apis.py
│   │   │   ├── audio_processing.py
│   │   │   ├── dubbing_pipeline.py
│   │   │   └── __init__.py
│   │   ├── routes/
│   │   │   ├── auth.py
│   │   │   ├── dubbing.py
│   │   │   ├── jobs.py
│   │   │   ├── voices.py
│   │   │   ├── health.py
│   │   │   └── __init__.py
│   │   ├── tasks/
│   │   │   ├── celery_tasks.py
│   │   │   └── __init__.py
│   │   ├── utils/
│   │   │   ├── database.py
│   │   │   ├── security.py
│   │   │   ├── logging_config.py
│   │   │   └── __init__.py
│   ├── tests/
│   │   ├── test_auth.py
│   │   ├── test_jobs.py
│   │   ├── test_voices.py
│   │   ├── test_integration.py
│   │   ├── test_performance.py
│   │   ├── test_api_integration.py
│   │   └── conftest.py
│   ├── migrations/
│   ├── requirements.txt
│   ├── requirements-dev.txt
│   └── pytest.ini
├── frontend/
│   ├── src/
│   ├── public/
│   └── package.json
├── docs/
│   ├── README.md
│   ├── API.md
│   ├── DEPLOYMENT.md
│   └── ARCHITECTURE.md
├── deploy/
│   └── deploy.sh
├── docker-compose.yml
├── Dockerfile
├── .env.example
├── .dockerignore
├── .gitignore
├── README.md
└── LICENSE
```

## Getting Started

### Development

```bash
# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Configure environment
cp .env.example .env

# Initialize database
alembic upgrade head

# Run development server
uvicorn app.main:app --reload

# Run tests
pytest

# Run with Docker
docker-compose up
```

## API Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

MIT License - see LICENSE file for details

## Support

- 📧 Email: support@voicesync-ai.com
- 💬 Discord: https://discord.gg/voicesync
- 🐛 Issues: https://github.com/yourusername/voicesync-ai/issues
