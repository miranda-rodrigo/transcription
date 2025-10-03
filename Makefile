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
	@echo '  clean         Remove venv and temp files'
	@echo ''
	@echo 'Transcription shortcuts:'
	@echo '  make transcribe FILE=audio.mp4     # Transcribe local file'
	@echo '  make transcribe URL="https://..."  # Transcribe from URL' 
	@echo '  make transcribe-clipboard          # Use clipboard workflow'

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
	rm -rf $(VENV) tmp __pycache__ **/__pycache** *.log




