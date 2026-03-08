# AGENTS.md

## Cursor Cloud specific instructions

This is a Python CLI tool for audio/video transcription (YouTube URLs, local files). No web server or database — it's a local pipeline.

### Architecture
- Entry points: `bin/transcribe-shortcut` (generic) and `bin/transcribe-youtube-clipboard` (macOS-only YouTube clipboard workflow)
- Core scripts: `scripts/transcribe_generic.py` (works on Linux), `scripts/transcribe_youtube.py` (macOS-only)
- Setup: `make setup` (creates `.venv`, installs `requirements.txt`)
- Config: `.env` (copy from `.env.example`); `OPENAI_API_KEY` is optional

### Running on Linux (Cloud Agent)
- `bin/transcribe-youtube-clipboard` and `scripts/transcribe_youtube.py` require macOS (`pbcopy`/`pbpaste`). Use `scripts/transcribe_generic.py` or `bin/transcribe-shortcut` for testing on Linux.
- System dependency: `ffmpeg` (pre-installed). `yt-dlp` is installed as a Python package.
- Example test command:
  ```
  .venv/bin/python3 scripts/transcribe_generic.py --no-review --model tiny --device cpu --compute-type int8 <audio_file>
  ```

### Gotchas
- The `tiny` model is fastest for testing; `small` is the default for production quality.
- Use `--device cpu --compute-type int8` on machines without GPU.
- `--no-review` skips the OpenAI API call (useful when `OPENAI_API_KEY` is not set).
- The root-level `transcribe.py` is an older script that uses OpenAI's cloud Whisper API, not `faster-whisper`. The main scripts are in `scripts/`.
- There are no automated tests (no test framework configured). Validation is done by running the transcription pipeline with sample audio files.
- `README.md` currently has merge conflict markers — this is a pre-existing issue in the repo.
