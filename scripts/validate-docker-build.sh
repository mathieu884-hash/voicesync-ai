#!/bin/bash
# Docker Build Validation Script
# Validates dependencies and Docker configuration before deployment

set -e

echo "🔍 VoiceSync AI - Docker Build Validation"
echo "=========================================="
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check Docker
echo "📦 Checking Docker installation..."
if ! command -v docker &> /dev/null; then
    echo -e "${RED}✗ Docker not found${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Docker found${NC}"

# Check Python
echo "📦 Checking Python..."
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}✗ Python 3 not found${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Python 3 found${NC}"

# Validate backend requirements
echo "📋 Validating backend requirements..."
if [ ! -f "backend/requirements-prod.txt" ]; then
    echo -e "${RED}✗ requirements-prod.txt not found${NC}"
    exit 1
fi
echo -e "${GREEN}✓ requirements-prod.txt found${NC}"

# Validate frontend package.json
echo "📋 Validating frontend package.json..."
if [ ! -f "frontend/package.json" ]; then
    echo -e "${RED}✗ frontend/package.json not found${NC}"
    exit 1
fi

if ! grep -q '"next"' frontend/package.json; then
    echo -e "${RED}✗ Next.js not in frontend dependencies${NC}"
    exit 1
fi
echo -e "${GREEN}✓ frontend/package.json valid${NC}"

# Validate frontend package-lock.json
echo "📋 Validating frontend package-lock.json..."
if [ ! -f "frontend/package-lock.json" ]; then
    echo -e "${RED}✗ package-lock.json not found${NC}"
    exit 1
fi
echo -e "${GREEN}✓ package-lock.json found${NC}"

# Build backend
echo ""
echo "🏗️  Building backend image..."
if docker build -t voicesync-backend:test -f backend/Dockerfile backend --target production > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Backend image built successfully${NC}"
else
    echo -e "${RED}✗ Backend image build failed${NC}"
    exit 1
fi

# Build frontend
echo "🏗️  Building frontend image..."
if docker build -t voicesync-frontend:test -f frontend/Dockerfile frontend > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Frontend image built successfully${NC}"
else
    echo -e "${RED}✗ Frontend image build failed${NC}"
    exit 1
fi

# Check image sizes
echo ""
echo "📊 Image sizes:"
echo -n "Backend: "
docker images voicesync-backend:test --format "{{.Size}}"
echo -n "Frontend: "
docker images voicesync-frontend:test --format "{{.Size}}"

# Cleanup
echo ""
echo "🧹 Cleaning up test images..."
docker rmi voicesync-backend:test voicesync-frontend:test > /dev/null 2>&1
echo -e "${GREEN}✓ Cleanup complete${NC}"

echo ""
echo -e "${GREEN}✅ All validations passed!${NC}"
echo "Ready for deployment."