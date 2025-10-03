#!/bin/bash
# Clean script for macOS Shortcuts - paste this in "Run Shell Script" action

cd "/Users/rodrigomiranda/useful-repos/audio_transcription"

# Add Homebrew to PATH
export PATH="/opt/homebrew/bin:/usr/local/bin:$PATH"

# Run transcription
if [ $# -gt 0 ] && [ -n "$1" ]; then
  ./bin/transcribe-shortcut "$1"
else
  ./bin/transcribe-shortcut --from-clipboard --to-clipboard
fi

