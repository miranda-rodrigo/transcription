#!/bin/bash
# Simple shell script for macOS Shortcuts integration
# This script is designed to work with the Shortcuts app "Run Shell Script" action

set -euo pipefail

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
TRANSCRIBE_SCRIPT="$REPO_ROOT/bin/transcribe-shortcut"

# Default to clipboard workflow if no arguments
if [[ $# -eq 0 ]]; then
    exec "$TRANSCRIBE_SCRIPT" --from-clipboard --to-clipboard
fi

# Otherwise pass all arguments to the transcription script
exec "$TRANSCRIBE_SCRIPT" "$@"



