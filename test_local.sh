#!/bin/bash
# Script para testar localmente (sem Hammerspoon)
# Útil para debug e desenvolvimento

set -e

# Check for URL argument
if [ -z "$1" ]; then
    echo "Usage: ./test_local.sh <youtube_url>"
    echo "Example: ./test_local.sh 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'"
    exit 1
fi

YOUTUBE_URL="$1"
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Load environment
if [ -f "$SCRIPT_DIR/.env" ]; then
    export $(grep -v '^#' "$SCRIPT_DIR/.env" | xargs)
fi

# Check for venv
if [ -d "$SCRIPT_DIR/venv" ]; then
    PYTHON="$SCRIPT_DIR/venv/bin/python3"
else
    PYTHON="python3"
fi

echo "🎬 Testing YouTube transcription..."
echo "URL: $YOUTUBE_URL"
echo ""

# Run the script
"$PYTHON" "$SCRIPT_DIR/youtube_transcribe.py" "$YOUTUBE_URL"

echo ""
echo "✅ Test complete!"
