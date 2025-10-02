#!/usr/bin/env python3
"""
Transcribe YouTube audio from clipboard or URL on macOS.
- Downloads audio via yt-dlp + ffmpeg
- Splits into chunks if long
- Transcribes with faster-whisper (parallelizable)
- Optionally reviews with OpenAI GPT for coherence
- Copies final transcript back to clipboard (or prints to stdout)
- Cleans up temp files; does not save final transcript to disk

Dependencies:
  - Homebrew: ffmpeg, yt-dlp (brew install ffmpeg yt-dlp)
  - Python: faster-whisper, yt-dlp, pydub, python-dotenv, openai

Usage examples:
  python scripts/transcribe_youtube.py --url "https://youtu.be/..." --review auto --to-clipboard
  python scripts/transcribe_youtube.py --from-clipboard --to-clipboard
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
from typing import List, Optional, Tuple

from dotenv import load_dotenv
from pydub import AudioSegment
import yt_dlp

# Try to import faster-whisper; provide helpful error if missing
try:
    from faster_whisper import WhisperModel  # type: ignore
    HAS_FASTER = True
except Exception:  # pragma: no cover
    HAS_FASTER = False

# Optional OpenAI for review step
try:
    from openai import OpenAI  # type: ignore
    HAS_OPENAI = True
except Exception:  # pragma: no cover
    HAS_OPENAI = False

# -----------------------------------------------------------------------------
# Configuration
# -----------------------------------------------------------------------------

DEFAULT_MODEL_SIZE = os.environ.get("WHISPER_MODEL", "small")  # base|small|medium|large-v3
DEFAULT_DEVICE = os.environ.get("WHISPER_DEVICE", "auto")       # auto|cpu|cuda|metal
DEFAULT_COMPUTE = os.environ.get("WHISPER_COMPUTE", "int8")     # int8|int8_float16|float16|float32

# Split audio into chunks greater than this duration (in minutes)
DEFAULT_CHUNK_MIN = int(os.environ.get("CHUNK_MINUTES", "10"))

# Number of parallel chunk workers (each creates its own model instance). Keep small.
DEFAULT_CHUNK_WORKERS = int(os.environ.get("CHUNK_WORKERS", "2"))

# Number of internal workers inside faster-whisper for CPU tasks
DEFAULT_NUM_WORKERS = int(os.environ.get("WHISPER_NUM_WORKERS", "2"))

# -----------------------------------------------------------------------------
# Logging
# -----------------------------------------------------------------------------

logger = logging.getLogger("yt-transcribe")
handler = logging.StreamHandler(sys.stderr)
formatter = logging.Formatter("[%(levelname)s] %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

# -----------------------------------------------------------------------------
# Utilities
# -----------------------------------------------------------------------------

YOUTUBE_REGEX = re.compile(r"^(https?://)?(www\.)?(youtube\.com|youtu\.be)/")


def is_macos() -> bool:
    return platform.system() == "Darwin"


def read_clipboard_text() -> Optional[str]:
    if not is_macos():
        return None
    try:
        out = subprocess.run(["pbpaste"], check=True, stdout=subprocess.PIPE, text=True)
        return out.stdout.strip()
    except Exception:
        return None


def copy_to_clipboard(text: str) -> bool:
    if not is_macos():
        return False
    try:
        proc = subprocess.Popen(["pbcopy"], stdin=subprocess.PIPE, text=True)
        proc.communicate(text)
        return proc.returncode == 0
    except Exception as e:  # pragma: no cover
        logger.error(f"Failed to copy to clipboard: {e}")
        return False


def ensure_dependency_exists(cmd: str, args: list[str] = None) -> None:
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
# Core steps
# -----------------------------------------------------------------------------


def validate_youtube_url(url: str) -> None:
    if not url or not YOUTUBE_REGEX.search(url):
        raise ValueError("Clipboard or input does not contain a valid YouTube URL")


def download_audio_to_temp(url: str, temp_dir: Path) -> Path:
    """Download best audio and convert to WAV using yt-dlp + ffmpeg postprocessor."""
    output_tmpl = str(temp_dir / "downloaded.%(ext)s")
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": output_tmpl,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "wav",
                "preferredquality": "0",
            }
        ],
        "quiet": True,
        "noprogress": True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    # Locate WAV file
    for p in temp_dir.iterdir():
        if p.suffix.lower() in {".wav", ".m4a", ".mp3", ".webm"}:
            return p
    raise RuntimeError("Audio download failed or unexpected format.")


def split_audio_if_needed(audio_path: Path, chunk_minutes: int, temp_dir: Path) -> List[Tuple[int, Path]]:
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


def _transcribe_with_faster(model: WhisperModel, wav_path: Path, num_workers: int) -> Tuple[str, Optional[str]]:
    segments, info = model.transcribe(
        str(wav_path),
        language=None,  # autodetect
        vad_filter=True,
        beam_size=1,
        condition_on_previous_text=True,
        word_timestamps=False,
        num_workers=max(1, num_workers),
    )
    texts: List[str] = [seg.text for seg in segments]
    language = getattr(info, "language", None)
    return (" ".join(texts).strip(), language)


def transcribe_chunks_faster(
    chunks: List[Tuple[int, Path]],
    model_size: str,
    device: str,
    compute_type: str,
    chunk_workers: int,
    num_workers: int,
) -> Tuple[str, Optional[str]]:
    # If only one worker, reuse model to save memory
    if max(1, chunk_workers) == 1:
        model = WhisperModel(model_size, device=device, compute_type=compute_type)
        results: List[TranscriptionResult] = []
        for index, wav_path in chunks:
            text, lang = _transcribe_with_faster(model, wav_path, num_workers)
            results.append(TranscriptionResult(index=index, text=text, language=lang))
    else:
        # Parallel: each worker owns its model (more memory usage)
        def worker(args: Tuple[int, Path]) -> TranscriptionResult:
            index, wav_path = args
            worker_model = WhisperModel(model_size, device=device, compute_type=compute_type)
            text, lang = _transcribe_with_faster(worker_model, wav_path, num_workers)
            return TranscriptionResult(index=index, text=text, language=lang)

        results = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=chunk_workers) as executor:
            futures = [executor.submit(worker, item) for item in chunks]
            for fut in concurrent.futures.as_completed(futures):
                results.append(fut.result())

    # Sort and combine
    results.sort(key=lambda r: r.index)
    combined_text = "\n\n".join(r.text for r in results if r.text)

    # Choose language: first non-empty
    detected_language: Optional[str] = None
    for r in results:
        if r.language:
            detected_language = r.language
            break

    return combined_text.strip(), detected_language


def review_transcript_openai(text: str, language_hint: Optional[str]) -> str:
    if not HAS_OPENAI:
        logger.warning("openai package not available; skipping review.")
        return text
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        logger.info("OPENAI_API_KEY not set; skipping review.")
        return text

    try:
        client = OpenAI()
        system = (
            "Você é um assistente que revisa transcrições.\n"
            "- Preserve o idioma original.\n"
            "- Una e ajuste frases quebradas por chunking.\n"
            "- Corrija erros óbvios de reconhecimento sem alterar o sentido.\n"
            "- Não invente conteúdo.\n"
        )
        user = (
            f"Idioma detectado: {language_hint or 'desconhecido'}.\n\n"
            "Revise o texto abaixo para fluidez e correção mínima, mantendo o significado:\n\n"
            f"{text}"
        )
        resp = client.chat.completions.create(
            model=os.getenv("OPENAI_REVIEW_MODEL", "gpt-4o-mini"),
            temperature=0.2,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
        )
        revised = resp.choices[0].message.content or ""
        return revised.strip() or text
    except Exception as e:  # pragma: no cover
        logger.error(f"OpenAI review failed: {e}")
        return text


# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------


def main(argv: Optional[List[str]] = None) -> int:
    load_dotenv()

    parser = argparse.ArgumentParser(description="Transcribe YouTube audio and copy transcript to clipboard (macOS).")
    grp = parser.add_mutually_exclusive_group()
    grp.add_argument("--url", help="YouTube URL to transcribe")
    grp.add_argument("--from-clipboard", action="store_true", help="Read YouTube URL from clipboard")

    parser.add_argument("--review", choices=["auto", "openai", "none"], default="auto", help="Final review provider")
    parser.add_argument("--to-clipboard", action="store_true", help="Copy transcript to macOS clipboard")

    parser.add_argument("--model", default=DEFAULT_MODEL_SIZE, help="faster-whisper model size/path (default: small)")
    parser.add_argument("--device", default=DEFAULT_DEVICE, help="Device: auto|cpu|cuda|metal")
    parser.add_argument("--compute-type", default=DEFAULT_COMPUTE, help="Compute type: int8|int8_float16|float16|float32")
    parser.add_argument("--chunk-minutes", type=int, default=DEFAULT_CHUNK_MIN, help="Chunk size in minutes (default: 10)")
    parser.add_argument("--chunk-workers", type=int, default=DEFAULT_CHUNK_WORKERS, help="Parallel chunk workers (default: 2)")
    parser.add_argument("--num-workers", type=int, default=DEFAULT_NUM_WORKERS, help="Internal faster-whisper workers (default: 2)")

    parser.add_argument("--verbose", action="store_true", help="Verbose logging")

    args = parser.parse_args(argv)

    if args.verbose:
        logger.setLevel(logging.DEBUG)

    if not HAS_FASTER:
        logger.error("faster-whisper is not installed. pip install faster-whisper")
        return 2

    if not is_macos():
        logger.error("This script is intended for macOS.")
        return 2

    # Determine URL
    url: Optional[str] = args.url
    if args.from_clipboard or not url:
        url = read_clipboard_text()
    if not url:
        logger.error("No URL provided and clipboard is empty.")
        return 2

    try:
        validate_youtube_url(url)
    except Exception as e:
        logger.error(str(e))
        return 2

    # Ensure external deps
    try:
        ensure_dependency_exists("ffmpeg", ["-version"])  # required by pydub/yt-dlp
        ensure_dependency_exists("yt-dlp", ["--version"])  # helpful check
    except RuntimeError as e:
        logger.error(str(e))
        return 2

    temp_dir = Path(tempfile.mkdtemp(prefix="yt_transcribe_"))
    try:
        logger.info("Downloading audio with yt-dlp...")
        audio_path = download_audio_to_temp(url, temp_dir)
        logger.info(f"Downloaded: {audio_path.name}")

        logger.info("Preparing chunks...")
        chunks = split_audio_if_needed(audio_path, args.chunk_minutes, temp_dir)
        logger.info(f"Chunks: {len(chunks)}")

        logger.info("Transcribing with faster-whisper...")
        transcript_text, detected_language = transcribe_chunks_faster(
            chunks=chunks,
            model_size=args.model,
            device=args.device,
            compute_type=args.compute_type,
            chunk_workers=max(1, args.chunk_workers),
            num_workers=max(1, args.num_workers),
        )

        logger.info(f"Language detected: {detected_language or 'unknown'}")

        # Final review
        do_review = (
            (args.review == "openai") or
            (args.review == "auto" and os.getenv("OPENAI_API_KEY") is not None)
        )
        final_text = transcript_text
        if do_review:
            logger.info("Reviewing transcript with OpenAI...")
            final_text = review_transcript_openai(transcript_text, detected_language)

        # Output
        if args.to_clipboard:
            ok = copy_to_clipboard(final_text)
            if ok:
                logger.info("Transcript copied to clipboard.")
            else:
                logger.error("Failed to copy transcript to clipboard.")
                # Still print to stdout as fallback
                print(final_text)
        else:
            print(final_text)

        return 0
    finally:
        # Cleanup temp directory
        try:
            shutil.rmtree(temp_dir, ignore_errors=True)
        except Exception:  # pragma: no cover
            pass


if __name__ == "__main__":
    raise SystemExit(main())
