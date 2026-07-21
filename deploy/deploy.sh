#!/bin/bash
# Deployment script for AWS

set -e

echo "🚀 VoiceSync AI Deployment Script"
echo "==================================="

# Configuration
REPO_URL="https://github.com/yourusername/voicesync-ai.git"
BRANCH="main"
APP_DIR="/home/ubuntu/voicesync-ai"
VENV_DIR="$APP_DIR/venv"

echo "
📥 Cloning repository..."
if [ -d "$APP_DIR" ]; then
    cd "$APP_DIR"
    git pull origin "$BRANCH"
else
    git clone -b "$BRANCH" "$REPO_URL" "$APP_DIR"
    cd "$APP_DIR"
fi

echo "
🐍 Setting up Python environment..."
if [ ! -d "$VENV_DIR" ]; then
    python3.11 -m venv "$VENV_DIR"
fi
source "$VENV_DIR/bin/activate"

echo "
📦 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "
🔧 Configuring environment..."
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "⚠️  Please configure .env file"
    exit 1
fi

echo "
🗄️  Migrating database..."
alembic upgrade head

echo "
🔄 Restarting services..."
sudo systemctl restart voicesync-api
sudo systemctl restart voicesync-worker

echo "
✅ Deployment completed successfully!"
echo "API URL: http://localhost:8000"
echo "Docs: http://localhost:8000/docs"
