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
	@echo '  clean         Remove venv and temp files'

setup:
	@[ -n "$(PY)" ] || (echo 'python3 not found' && exit 1)
	@$(PY) -m venv $(VENV)
	@$(PIP) install --upgrade pip wheel
	@$(PIP) install -r requirements.txt
	@echo 'Done. Remember to: brew install ffmpeg yt-dlp'

run:
	@bin/transcribe-youtube-clipboard

clean:
	rm -rf $(VENV) tmp __pycache__ **/__pycache__ *.log




