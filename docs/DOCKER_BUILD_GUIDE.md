# Docker Build and Deployment Guide

## Overview

This guide covers the Docker build system, dependencies, and troubleshooting for VoiceSync AI.

## Build Architecture

### Backend

**Image**: Multi-stage production Docker build
**Base**: `python:3.11-slim`
**Key Features**:
- Separate development and production stages
- Comprehensive system packages for ML/AI
- Optimized build order for dependency resolution
- Non-root user for security
- Health checks included

**Build Dependencies**:
- `build-essential`: C/C++ compilers for Python packages
- `libpq-dev`: PostgreSQL client library
- `ffmpeg`: Audio/video processing
- `libsndfile1`: Audio processing support
- `libgl1`, `libglib2.0-0`: OpenCV runtime

**Python Packages**: See `backend/requirements-prod.txt`

### Frontend

**Image**: Multi-stage Node.js build
**Base**: `node:20-alpine`
**Key Features**:
- Separate build and production stages
- Dev dependencies only in build stage
- Optimized production image
- Health checks included

**Requirements**:
- Next.js 14+
- React 18+
- TypeScript support
- Tailwind CSS

## Building Locally

### Prerequisites

```bash
docker --version  # Should be 20.10+
npm --version     # Should be 8+
python3 --version # Should be 3.11+
```

### Backend Build

**Development**:
```bash
cd backend
docker build -t voicesync-backend:dev -f Dockerfile --target development .
docker run -p 8000:8000 voicesync-backend:dev
```

**Production**:
```bash
cd backend
docker build -t voicesync-backend:latest -f Dockerfile --target production .
```

### Frontend Build

```bash
cd frontend
docker build -t voicesync-frontend:latest -f Dockerfile .
docker run -p 3000:3000 voicesync-frontend:latest
```

## Validation Script

Before deployment, run the validation script:

```bash
chmod +x scripts/validate-docker-build.sh
./scripts/validate-docker-build.sh
```

This validates:
- Docker installation
- Python installation
- Required configuration files
- Builds both images for testing
- Checks image sizes

## Troubleshooting

### Build Issues

#### "ModuleNotFoundError: No module named 'requests'"

**Cause**: Build tool dependencies installed after `requirements.txt`

**Solution**:
- Ensure `pip install setuptools wheel` runs before `pip install -r requirements.txt`
- This is now handled in the Dockerfile

#### "No such file or directory: 'package-lock.json'"

**Cause**: Frontend package-lock.json missing

**Solution**:
- Run `npm install` locally to generate `package-lock.json`
- Commit to repository

#### "docker: Error response from daemon: OCI runtime create failed"

**Cause**: System resource limits or kernel issues

**Solution**:
```bash
# Increase Docker memory limit
docker run --memory=4g voicesync-backend:latest

# Or configure in Docker Desktop settings
# Preferences > Resources > Memory: 8GB+
```

### Dependency Issues

#### torch/numpy/scipy compilation errors

**Cause**: Missing system packages for compilation

**Solution**:
- Ensure all system packages are installed (see Dockerfile)
- Use prebuilt wheels: these are installed by default
- Check Python version compatibility

#### cryptography/OpenSSL errors

**Cause**: Missing OpenSSL development headers

**Solution**:
- Already included in Dockerfile
- Ensure `libssl-dev` is installed in system

### Image Size Issues

#### Docker image too large

**Optimization**:
```dockerfile
# Use --no-cache-dir with pip
RUN pip install --no-cache-dir -r requirements.txt

# Use slim base images
FROM python:3.11-slim

# Multi-stage builds
FROM base as build
...
FROM base as production
COPY --from=build /app/dist .
```

## CI/CD Deployment

### GitHub Actions Workflow

The workflow in `.github/workflows/deploy.yml`:

1. **Checkout code**
2. **Setup Docker Buildx**
3. **Login to GHCR**
4. **Build and push backend** to `ghcr.io/.../backend:latest`
5. **Build and push frontend** to `ghcr.io/.../frontend:latest`
6. **Deploy to Kubernetes** (if configured)
7. **Notify Slack** with status

### Image Naming Convention

```
Repository: ghcr.io/mathieu884-hash/voicesync-ai

Backend:
  - ghcr.io/mathieu884-hash/voicesync-ai/backend:latest
  - ghcr.io/mathieu884-hash/voicesync-ai/backend:<commit-sha>

Frontend:
  - ghcr.io/mathieu884-hash/voicesync-ai/frontend:latest
  - ghcr.io/mathieu884-hash/voicesync-ai/frontend:<commit-sha>
```

## Performance Optimization

### Docker Build Cache

```dockerfile
# Good: Frequent changes at end
RUN apt-get install ...
RUN pip install setuptools wheel
RUN pip install requests
COPY . .  # Changes frequently, after stable layers

# Bad: Frequent changes early
COPY . .  # Changes frequently
RUN apt-get install ...  # Won't be cached
```

### Caching Strategy

- GitHub Actions GHA cache: 5GB per repo
- Use `type=gha` in docker/build-push-action
- Cache Docker layers for faster rebuilds

### Build Time Optimization

**Current times**:
- Backend: ~10-15 minutes (first run), ~2-3 minutes (cached)
- Frontend: ~5-8 minutes (first run), ~1-2 minutes (cached)

## Environment Variables

### Backend (production.env)

```
ENVIRONMENT=production
DEBUG=false
DATABASE_URL=postgresql://user:pass@host:5432/db
REDIS_URL=redis://cache-server:6379
GUNICORN_WORKERS=4
GUNICORN_TIMEOUT=120
```

### Frontend (.env.production)

```
NEXT_PUBLIC_API_URL=https://api.voicesync.ai
NEXT_PUBLIC_APP_NAME=VoiceSync AI
```

## Security Considerations

1. **Non-root user**: Backend runs as `appuser:appuser` (UID 1000)
2. **Health checks**: Both images include health checks
3. **Minimal base images**: Using `slim` and `alpine` variants
4. **Secret management**: Use GitHub Secrets for sensitive data
5. **Read-only filesystem**: Consider `--read-only` flag in production

## Monitoring

### Health Endpoints

**Backend**:
- `GET /health` - Basic health check
- `GET /health/db` - Database connectivity
- `GET /health/redis` - Redis connectivity

**Frontend**:
- `GET /` - Server availability

### Container Logging

```bash
# View logs
docker logs <container-id>

# Follow logs
docker logs -f <container-id>

# Limit output
docker logs --tail 100 <container-id>
```

## Related Documentation

- [GitHub Actions CI/CD](./GITHUB_ACTIONS.md)
- [Kubernetes Deployment](./KUBERNETES.md)
- [Development Setup](./DEVELOPMENT.md)