# Multi-stage build
FROM python:3.11-slim as base

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies - organized by category
RUN apt-get update && apt-get install -y --no-install-recommends \
    # Build tools
    build-essential \
    gcc \
    g++ \
    git \
    curl \
    pkg-config \
    cmake \
    # Database
    libpq-dev \
    # Audio/Video
    ffmpeg \
    libsndfile1 \
    # Image processing
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgl1 \
    libglib2.0-0 \
    # Scientific computing (fallback support)
    libgomp1 \
    gfortran \
    libblas-dev \
    liblapack-dev \
    # OpenSSL (for cryptography)
    libssl-dev \
    # Clean up
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Development stage
FROM base as development

# Install Python build tools first (required by many packages)
RUN pip install --upgrade pip setuptools wheel

# Install build dependencies separately
RUN pip install requests

# Copy and install requirements
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

# Production stage
FROM base as production

# Install Python build tools first (required by many packages)
RUN pip install --upgrade pip setuptools wheel

# Install build dependencies separately  
RUN pip install requests

# Copy and install production requirements
COPY requirements-prod.txt .
RUN pip install -r requirements-prod.txt

# Install gunicorn for production
RUN pip install gunicorn==21.2.0

# Copy application
COPY . .

# Create non-root user
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app

USER appuser

EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

CMD ["gunicorn", "app.main:app", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000", "--timeout", "120"]