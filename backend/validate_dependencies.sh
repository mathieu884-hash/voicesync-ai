#!/bin/bash

set -euo pipefail

REQ_FILE="${1:-requirements-prod.txt}"

echo "🔍 Validating dependency installation with ${REQ_FILE}"
python -m pip install --upgrade pip setuptools wheel
pip install --no-cache-dir requests
pip install --no-cache-dir --no-build-isolation -r "${REQ_FILE}"
pip check

echo "✅ Dependency validation completed successfully"
