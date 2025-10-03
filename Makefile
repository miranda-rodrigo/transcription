SHELL := /bin/bash
PY := $(shell command -v python3)
VENV := .venv
PIP := $(VENV)/bin/pip
PYTHON := $(VENV)/bin/python3

.DEFAULT_GOAL := help

help:
	@echo 'Targets:'
	@echo '  setup         Create venv and install deps'
	@echo '  run           Transcribe YouTube URL from clipboard (macOS)'
	@echo '  transcribe    Generic transcription shortcut (files/URLs/clipboard)'
	@echo '  shortcut-help Show macOS Shortcuts app integration instructions'
	@echo '  clean         Remove venv and temp files'
	@echo ''
	@echo 'Transcription shortcuts:'
	@echo '  make transcribe FILE=audio.mp4     # Transcribe local file'
	@echo '  make transcribe URL="https://..."  # Transcribe from URL' 
	@echo '  make transcribe-clipboard          # Use clipboard workflow'
	@echo ''
	@echo 'macOS Shortcuts integration:'
	@echo '  make shortcut-help                 # Show setup instructions'
	@echo '  make shortcut-test                 # Test shortcut integration'

setup:
	@[ -n "$(PY)" ] || (echo 'python3 not found' && exit 1)
	@$(PY) -m venv $(VENV)
	@$(PIP) install --upgrade pip wheel
	@$(PIP) install -r requirements.txt
	@echo 'Done. Remember to: brew install ffmpeg yt-dlp'

run:
	@bin/transcribe-youtube-clipboard

transcribe:
ifdef FILE
	@bin/transcribe-shortcut "$(FILE)"
else ifdef URL  
	@bin/transcribe-shortcut "$(URL)"
else
	@bin/transcribe-shortcut --help
endif

transcribe-clipboard:
	@bin/transcribe-shortcut --from-clipboard --to-clipboard

clean:
	rm -rf $(VENV) tmp __pycache__ **/__pycache__ *.log

shortcut-help:
	@echo "=== macOS Shortcuts Integration ==="
	@echo ""
	@cat shortcuts/SETUP_INSTRUCTIONS.md
	@echo ""
	@echo "Files created:"
	@echo "  shortcuts/simple_shortcut.sh      - Simple shell script for Shortcuts app"
	@echo "  shortcuts/Audio_Transcription.applescript  - AppleScript version"
	@echo "  shortcuts/SETUP_INSTRUCTIONS.md   - Quick setup guide"  
	@echo "  shortcuts/README.md               - Detailed documentation"

shortcut-test:
	@echo "Testing shortcut integration..."
	@echo "Make sure you have a YouTube URL in your clipboard, then:"
	@shortcuts/simple_shortcut.sh
	@echo "If this works, your macOS Shortcuts integration is ready!"