#!/bin/bash
# Test script to run all tests

set -e

echo "🧪 Running VoiceSync AI Tests"
echo "============================="

# Install dependencies
echo "
📦 Installing dependencies..."
pip install -r requirements-dev.txt

# Run unit tests
echo "
🔧 Running unit tests..."
pytest tests/test_auth.py -v --tb=short
pytest tests/test_jobs.py -v --tb=short
pytest tests/test_voices.py -v --tb=short

# Run integration tests
echo "
🔗 Running integration tests..."
pytest tests/test_integration.py -v --tb=short -m integration

# Run performance tests
echo "
⚡ Running performance tests..."
pytest tests/test_performance.py -v --tb=short -m performance

# Run coverage report
echo "
📊 Generating coverage report..."
pytest --cov=app --cov-report=html --cov-report=term

echo "
✅ All tests completed!"
