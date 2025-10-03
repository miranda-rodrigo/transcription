#!/usr/bin/env python3
"""
Generic Audio/Video Transcription Script

Supports:
- Local audio/video files (any format supported by ffmpeg)
- YouTube and other URLs supported by yt-dlp  
- Clipboard input/output (macOS only)
- Multiple languages with auto-detection
- AI review with OpenAI (optional)
- Parallel processing for long files

Dependencies:
  - System: ffmpeg, yt-dlp (brew install ffmpeg yt-dlp)
  - Python: faster-whisper, yt-dlp, pydub, python-dotenv, openai

Usage:
  python scripts/transcribe_generic.py audio.mp4
  python scripts/transcribe_generic.py https://youtu.be/...
  python scripts/transcribe_generic.py --from-clipboard --to-clipboard
"""

from __future__ import annotations

import argparse
import concurrent.futures
import logging
import os
import platform
import re
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Tuple, Union

from dotenv import load_dotenv
from pydub import AudioSegment
import yt_dlp

# Try to import faster-whisper
try:
    from faster_whisper import WhisperModel
    HAS_FASTER = True
except Exception:
    HAS_FASTER = False

# Optional OpenAI for review
try:
    from openai import OpenAI
    HAS_OPENAI = True
except Exception:
    HAS_OPENAI = False

# -----------------------------------------------------------------------------
# Configuration
# -----------------------------------------------------------------------------

DEFAULT_MODEL_SIZE = os.environ.get("WHISPER_MODEL", "small")
DEFAULT_DEVICE = os.environ.get("WHISPER_DEVICE", "auto") 
DEFAULT_COMPUTE = os.environ.get("WHISPER_COMPUTE", "int8")
DEFAULT_CHUNK_MIN = int(os.environ.get("CHUNK_MINUTES", "10"))
DEFAULT_CHUNK_WORKERS = int(os.environ.get("CHUNK_WORKERS", "2"))
DEFAULT_NUM_WORKERS = int(os.environ.get("WHISPER_NUM_WORKERS", "2"))

# -----------------------------------------------------------------------------
# Logging
# -----------------------------------------------------------------------------

logger = logging.getLogger("transcribe")
handler = logging.StreamHandler(sys.stderr)
formatter = logging.Formatter("[%(levelname)s] %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

# -----------------------------------------------------------------------------
# Utilities
# -----------------------------------------------------------------------------

URL_REGEX = re.compile(r"^https?://")
YOUTUBE_REGEX = re.compile(r"^(https?://)?(www\.)?(youtube\.com|youtu\.be)/")

def is_macos() -> bool:
    return platform.system() == "Darwin"

def is_url(text: str) -> bool:
    return bool(URL_REGEX.match(text.strip()))

def is_youtube_url(text: str) -> bool:
    return bool(YOUTUBE_REGEX.search(text.strip()))

def read_clipboard_text() -> Optional[str]:
    """Read text from clipboard (macOS only)."""
    if not is_macos():
        logger.warning("Clipboard read only supported on macOS")
        return None
    try:
        out = subprocess.run(["pbpaste"], check=True, stdout=subprocess.PIPE, text=True)
        return out.stdout.strip()
    except Exception as e:
        logger.error(f"Failed to read clipboard: {e}")
        return None

def copy_to_clipboard(text: str) -> bool:
    """Copy text to clipboard (macOS only)."""
    if not is_macos():
        logger.warning("Clipboard copy only supported on macOS")
        return False
    try:
        proc = subprocess.Popen(["pbcopy"], stdin=subprocess.PIPE, text=True)
        proc.communicate(text)
        return proc.returncode == 0
    except Exception as e:
        logger.error(f"Failed to copy to clipboard: {e}")
        return False

def ensure_dependency_exists(cmd: str, args: list[str] = None) -> None:
    """Check if external dependency exists."""
    args = args or ["--version"]
    try:
        subprocess.run([cmd] + args, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    except Exception:
        raise RuntimeError(f"Dependency '{cmd}' not found. Please install it.")

@dataclass
class TranscriptionResult:
    index: int
    text: str
    language: Optional[str]

# -----------------------------------------------------------------------------
# Core Functions
# -----------------------------------------------------------------------------

def download_audio_to_temp(url: str, temp_dir: Path) -> Path:
    """Download audio from URL using yt-dlp."""
    output_tmpl = str(temp_dir / "downloaded.%(ext)s")
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": output_tmpl,
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "wav",
            "preferredquality": "0",
        }],
        "quiet": True,
        "noprogress": True,
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    # Find downloaded file
    for p in temp_dir.iterdir():
        if p.suffix.lower() in {".wav", ".m4a", ".mp3", ".webm", ".ogg", ".flac"}:
            return p
    raise RuntimeError("Audio download failed or unexpected format.")

def convert_to_wav(input_path: Path, temp_dir: Path) -> Path:
    """Convert any audio/video file to WAV using ffmpeg."""
    if input_path.suffix.lower() == ".wav":
        return input_path
    
    output_path = temp_dir / "converted.wav"
    cmd = [
        "ffmpeg", "-i", str(input_path), 
        "-acodec", "pcm_s16le", "-ar", "16000", "-ac", "1",
        "-y", str(output_path)
    ]
    
    try:
        subprocess.run(cmd, check=True, capture_output=True, text=True)
        return output_path
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"FFmpeg conversion failed: {e.stderr}")

def split_audio_if_needed(audio_path: Path, chunk_minutes: int, temp_dir: Path) -> List[Tuple[int, Path]]:
    """Split audio into chunks if longer than chunk_minutes."""
    audio = AudioSegment.from_file(audio_path)
    chunk_ms = max(1, chunk_minutes) * 60 * 1000
    
    if len(audio) <= chunk_ms:
        return [(0, audio_path)]

    chunks: List[Tuple[int, Path]] = []
    for start_ms in range(0, len(audio), chunk_ms):
        end_ms = min(start_ms + chunk_ms, len(audio))
        chunk = audio[start_ms:end_ms]
        index = start_ms // chunk_ms
        out_path = temp_dir / f"chunk_{index:04d}.wav"
        chunk.export(out_path, format="wav")
        chunks.append((index, out_path))
    
    return chunks

def _transcribe_with_faster(model: WhisperModel, wav_path: Path, language: Optional[str]) -> Tuple[str, Optional[str]]:
    """Transcribe single audio file with faster-whisper."""
    segments, info = model.transcribe(
        str(wav_path),
        language=language,  # None for autodetect
        vad_filter=True,
        beam_size=1,
        condition_on_previous_text=True,
        word_timestamps=False,
    )
    
    texts: List[str] = [seg.text for seg in segments]
    detected_language = getattr(info, "language", None)
    return (" ".join(texts).strip(), detected_language)

def transcribe_chunks_faster(
    chunks: List[Tuple[int, Path]],
    model_size: str,
    device: str,
    compute_type: str,
    chunk_workers: int,
    language: Optional[str] = None,
) -> Tuple[str, Optional[str]]:
    """Transcribe audio chunks in parallel using faster-whisper."""
    
    if max(1, chunk_workers) == 1:
        # Single worker: reuse model
        model = WhisperModel(model_size, device=device, compute_type=compute_type)
        results: List[TranscriptionResult] = []
        
        for index, wav_path in chunks:
            text, lang = _transcribe_with_faster(model, wav_path, language)
            results.append(TranscriptionResult(index=index, text=text, language=lang))
    else:
        # Parallel workers: each owns model
        def worker(args: Tuple[int, Path]) -> TranscriptionResult:
            index, wav_path = args
            worker_model = WhisperModel(model_size, device=device, compute_type=compute_type)
            text, lang = _transcribe_with_faster(worker_model, wav_path, language)
            return TranscriptionResult(index=index, text=text, language=lang)

        results = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=chunk_workers) as executor:
            futures = [executor.submit(worker, item) for item in chunks]
            for fut in concurrent.futures.as_completed(futures):
                results.append(fut.result())

    # Sort by index and combine
    results.sort(key=lambda r: r.index)
    combined_text = "\n\n".join(r.text for r in results if r.text)

    # Get detected language from first result
    detected_language: Optional[str] = None
    for r in results:
        if r.language:
            detected_language = r.language
            break

    return combined_text.strip(), detected_language

def review_transcript_openai(text: str, language_hint: Optional[str]) -> str:
    """Review transcript with OpenAI for coherence and corrections."""
    if not HAS_OPENAI:
        logger.warning("OpenAI package not available; skipping review.")
        return text
    
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        logger.info("OPENAI_API_KEY not set; skipping review.")
        return text

    try:
        client = OpenAI()
        system = (
            "You are a transcript reviewer assistant.\n"
            "- Preserve the original language.\n" 
            "- Fix sentences broken by audio chunking.\n"
            "- Correct obvious recognition errors without changing meaning.\n"
            "- Do not invent content.\n"
            "- Output clean, readable text."
        )
        
        user_prompt = f"Detected language: {language_hint or 'unknown'}.\n\n"
        user_prompt += "Please review this transcript for fluency and minimal corrections while preserving meaning:\n\n"
        user_prompt += text
        
        response = client.chat.completions.create(
            model=os.getenv("OPENAI_REVIEW_MODEL", "gpt-4o-mini"),
            temperature=0.2,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user_prompt},
            ],
        )
        
        revised = response.choices[0].message.content or ""
        return revised.strip() or text
        
    except Exception as e:
        logger.error(f"OpenAI review failed: {e}")
        return text

# -----------------------------------------------------------------------------
# Main Function
# -----------------------------------------------------------------------------

def main(argv: Optional[List[str]] = None) -> int:
    load_dotenv()

    parser = argparse.ArgumentParser(
        description="Generic audio/video transcription with Whisper",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s audio.mp4                       # Transcribe local file
  %(prog)s https://youtu.be/abc123         # Transcribe YouTube video  
  %(prog)s --from-clipboard --to-clipboard # Use clipboard workflow
  %(prog)s --language en video.mov         # Force English language
        """.strip()
    )

    # Input sources
    input_group = parser.add_mutually_exclusive_group()
    input_group.add_argument("input", nargs="?", help="Local file path or URL to transcribe")
    input_group.add_argument("--from-clipboard", action="store_true", help="Read input from clipboard (macOS)")

    # Output options
    parser.add_argument("--to-clipboard", action="store_true", help="Copy result to clipboard (macOS)")
    parser.add_argument("--output", "-o", help="Save transcript to file")

    # Transcription options
    parser.add_argument("--language", "-l", help="Force language code (e.g., pt, en, es)")
    parser.add_argument("--model", default=DEFAULT_MODEL_SIZE, 
                       help="Whisper model size (tiny/base/small/medium/large)")
    parser.add_argument("--device", default=DEFAULT_DEVICE, help="Device: auto|cpu|cuda|metal")
    parser.add_argument("--compute-type", default=DEFAULT_COMPUTE, 
                       help="Compute type: int8|int8_float16|float16|float32")

    # Processing options
    parser.add_argument("--chunk-minutes", type=int, default=DEFAULT_CHUNK_MIN,
                       help="Chunk size in minutes for long files")
    parser.add_argument("--chunk-workers", type=int, default=DEFAULT_CHUNK_WORKERS,
                       help="Number of parallel workers for chunks")

    # Review options
    review_group = parser.add_mutually_exclusive_group()
    review_group.add_argument("--review", action="store_true", help="Review transcript with AI")
    review_group.add_argument("--no-review", action="store_true", help="Skip AI review")

    # Other options
    parser.add_argument("--verbose", action="store_true", help="Enable verbose logging")

    args = parser.parse_args(argv)

    if args.verbose:
        logger.setLevel(logging.DEBUG)

    # Validate dependencies
    if not HAS_FASTER:
        logger.error("faster-whisper is not installed. Run: pip install faster-whisper")
        return 2

    try:
        ensure_dependency_exists("ffmpeg", ["-version"])
    except RuntimeError as e:
        logger.error(str(e))
        return 2

    # Determine input source
    input_source: Optional[str] = args.input
    if args.from_clipboard:
        input_source = read_clipboard_text()
        if not input_source:
            logger.error("Clipboard is empty")
            return 2

    if not input_source:
        logger.error("No input provided. Use a file path, URL, or --from-clipboard")
        return 2

    # Determine if we should do AI review
    do_review = False
    if args.review:
        do_review = True
    elif not args.no_review:
        # Auto-detect based on API key availability
        do_review = bool(os.getenv("OPENAI_API_KEY"))

    # Create temporary directory
    temp_dir = Path(tempfile.mkdtemp(prefix="transcribe_"))
    
    try:
        # Process input
        if is_url(input_source):
            logger.info(f"Downloading from URL: {input_source}")
            audio_path = download_audio_to_temp(input_source, temp_dir)
        else:
            # Local file
            input_path = Path(input_source)
            if not input_path.exists():
                logger.error(f"File not found: {input_path}")
                return 2
            
            logger.info(f"Processing local file: {input_path}")
            # Convert to WAV if needed
            audio_path = convert_to_wav(input_path, temp_dir)

        logger.info(f"Audio prepared: {audio_path.name}")

        # Split into chunks if needed
        logger.info("Preparing chunks...")
        chunks = split_audio_if_needed(audio_path, args.chunk_minutes, temp_dir)
        logger.info(f"Audio split into {len(chunks)} chunk(s)")

        # Transcribe
        logger.info("Transcribing with Whisper...")
        transcript_text, detected_language = transcribe_chunks_faster(
            chunks=chunks,
            model_size=args.model,
            device=args.device,
            compute_type=args.compute_type,
            chunk_workers=max(1, args.chunk_workers),
            language=args.language,
        )

        logger.info(f"Language detected: {detected_language or 'unknown'}")

        # Review if requested
        final_text = transcript_text
        if do_review and transcript_text:
            logger.info("Reviewing transcript with AI...")
            final_text = review_transcript_openai(transcript_text, detected_language)

        # Output results
        if args.to_clipboard:
            if copy_to_clipboard(final_text):
                logger.info("Transcript copied to clipboard")
            else:
                logger.error("Failed to copy to clipboard, printing to stdout")
                print(final_text)
        
        if args.output:
            output_path = Path(args.output)
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(final_text)
            logger.info(f"Transcript saved to: {output_path}")

        # Always print to stdout unless only using clipboard
        if not args.to_clipboard or args.output:
            print(final_text)

        return 0

    except Exception as e:
        logger.error(f"Transcription failed: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1

    finally:
        # Cleanup
        try:
            shutil.rmtree(temp_dir, ignore_errors=True)
        except Exception:
            pass

if __name__ == "__main__":
    raise SystemExit(main())

