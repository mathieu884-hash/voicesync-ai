#!/bin/bash
# Create Pull Request for Docker Build Fix

set -e

PR_TITLE="Fix: Complete Docker build system robustness and dependency management"
PR_BODY_FILE=".github/pulls/docker-build-fix.md"
BASE="main"
HEAD="fix/docker-build-robust-solution"

echo "🔄 Creating Pull Request..."
echo "Title: $PR_TITLE"
echo "From: $HEAD → To: $BASE"
echo ""

# Check if PR body file exists
if [ ! -f "$PR_BODY_FILE" ]; then
    echo "❌ PR body file not found: $PR_BODY_FILE"
    exit 1
fi

# Create PR using GitHub CLI
if command -v gh &> /dev/null; then
    gh pr create \
      --title "$PR_TITLE" \
      --body-file "$PR_BODY_FILE" \
      --base "$BASE" \
      --head "$HEAD" \
      --repo "mathieu884-hash/voicesync-ai"
    
    if [ $? -eq 0 ]; then
        echo ""
        echo "✅ Pull Request created successfully!"
        echo "View at: https://github.com/mathieu884-hash/voicesync-ai/pulls"
    else
        echo "❌ Failed to create Pull Request"
        exit 1
    fi
else
    echo "⚠️  GitHub CLI not found. Please install it to use this script."
    echo "Or create PR manually at:"
    echo "https://github.com/mathieu884-hash/voicesync-ai/pull/new/fix/docker-build-robust-solution"
    exit 1
fi
