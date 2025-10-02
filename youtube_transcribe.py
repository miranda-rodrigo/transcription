#!/usr/bin/env python3
"""
YouTube Audio Transcription for Hammerspoon
Reads YouTube URL, downloads audio, splits if needed, transcribes in parallel with Whisper,
reviews with GPT, and outputs to stdout for clipboard.

Dependencies: openai, yt-dlp, pydub, python-dotenv
Requires: ffmpeg (brew install ffmpeg)
"""

import os
import sys
import tempfile
import shutil
import concurrent.futures
from pathlib import Path
from typing import List, Optional
import logging
from dotenv import load_dotenv
import openai
from pydub import AudioSegment
import yt_dlp

# Setup
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Configure logging to stderr so stdout is clean for clipboard
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s: %(message)s',
    stream=sys.stderr
)
logger = logging.getLogger(__name__)

# Constants
MAX_CHUNK_DURATION = 10 * 60 * 1000  # 10 minutes in ms (Whisper API limit ~25MB)
MAX_FILE_SIZE = 24 * 1024 * 1024  # 24 MB to be safe


def download_audio(url: str, output_dir: str) -> str:
    """Download audio from YouTube URL using yt-dlp."""
    logger.info("Downloading audio from YouTube...")
    output_path = os.path.join(output_dir, "audio.%(ext)s")
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': output_path,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '128',  # Lower quality to keep file size down
        }],
        'quiet': True,
        'no_warnings': True,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        # Find the downloaded file
        for file in os.listdir(output_dir):
            if file.startswith("audio."):
                downloaded_file = os.path.join(output_dir, file)
                logger.info(f"Download complete: {downloaded_file}")
                return downloaded_file
        
        raise FileNotFoundError("Downloaded audio file not found")
    except Exception as e:
        logger.error(f"Download failed: {str(e)}")
        raise


def split_audio(audio_path: str, output_dir: str) -> List[str]:
    """Split audio into chunks if longer than MAX_CHUNK_DURATION or larger than MAX_FILE_SIZE."""
    logger.info("Checking if audio needs splitting...")
    
    # Check file size
    file_size = os.path.getsize(audio_path)
    audio = AudioSegment.from_file(audio_path)
    audio_length = len(audio)
    
    # If small enough, return as is
    if file_size < MAX_FILE_SIZE and audio_length <= MAX_CHUNK_DURATION:
        logger.info("Audio is small enough, no splitting needed")
        return [audio_path]
    
    logger.info(f"Splitting audio into chunks (duration: {audio_length/1000:.1f}s, size: {file_size/(1024*1024):.1f}MB)...")
    
    chunks = []
    chunk_duration = min(MAX_CHUNK_DURATION, MAX_CHUNK_DURATION // 2)  # Use smaller chunks if file is large
    
    for i in range(0, audio_length, chunk_duration):
        chunk = audio[i:i + chunk_duration]
        chunk_path = os.path.join(output_dir, f"chunk_{len(chunks):03d}.mp3")
        chunk.export(chunk_path, format="mp3", bitrate="128k")
        chunks.append(chunk_path)
        logger.info(f"Created chunk {len(chunks)}/{(audio_length + chunk_duration - 1) // chunk_duration}")
    
    return chunks


def detect_language(audio_path: str) -> Optional[str]:
    """Detect language from audio using Whisper API (first 30 seconds)."""
    logger.info("Detecting language...")
    
    try:
        # Load first 30 seconds for language detection
        audio = AudioSegment.from_file(audio_path)
        sample = audio[:30000]  # First 30 seconds
        
        # Create temp file for sample
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as temp_file:
            sample.export(temp_file.name, format="mp3")
            temp_path = temp_file.name
        
        try:
            client = openai.OpenAI()
            with open(temp_path, "rb") as audio_file:
                # Use transcription without language parameter to get detection
                response = client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    response_format="verbose_json"
                )
                detected_lang = response.language
                logger.info(f"Detected language: {detected_lang}")
                return detected_lang
        finally:
            os.unlink(temp_path)
    except Exception as e:
        logger.warning(f"Language detection failed: {str(e)}, will use auto-detection")
        return None


def transcribe_chunk(chunk_path: str, language: Optional[str] = None) -> str:
    """Transcribe a single audio chunk using Whisper API."""
    try:
        client = openai.OpenAI()
        with open(chunk_path, "rb") as audio_file:
            kwargs = {
                "model": "whisper-1",
                "file": audio_file,
                "response_format": "text"
            }
            if language:
                kwargs["language"] = language
            
            response = client.audio.transcriptions.create(**kwargs)
        return response
    except Exception as e:
        logger.error(f"Transcription failed for {chunk_path}: {str(e)}")
        raise


def transcribe_parallel(chunks: List[str], language: Optional[str] = None) -> List[str]:
    """Transcribe multiple chunks in parallel."""
    logger.info(f"Transcribing {len(chunks)} chunk(s) in parallel...")
    
    transcripts = [None] * len(chunks)  # Preserve order
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=min(len(chunks), 5)) as executor:
        # Submit all tasks with their index
        future_to_index = {
            executor.submit(transcribe_chunk, chunk, language): i 
            for i, chunk in enumerate(chunks)
        }
        
        # Collect results in order
        for future in concurrent.futures.as_completed(future_to_index):
            index = future_to_index[future]
            try:
                transcripts[index] = future.result()
                logger.info(f"Chunk {index + 1}/{len(chunks)} transcribed")
            except Exception as e:
                logger.error(f"Failed to transcribe chunk {index}: {str(e)}")
                transcripts[index] = f"[Error transcribing chunk {index}]"
    
    return transcripts


def review_transcript(full_transcript: str, language: str) -> str:
    """Use GPT to review and improve the concatenated transcript."""
    logger.info("Reviewing transcript with GPT...")
    
    try:
        client = openai.OpenAI()
        
        system_prompt = (
            "You are a transcript editor. Fix any errors from audio transcription and chunking, "
            "ensure coherence across chunk boundaries, add proper punctuation, "
            "and format the text properly. Preserve the original language and meaning. "
            "Do not add content that wasn't spoken."
        )
        
        user_prompt = f"Review and improve this transcript (language: {language}):\n\n{full_transcript}"
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.3
        )
        
        reviewed = response.choices[0].message.content
        logger.info("Review complete")
        return reviewed
    except Exception as e:
        logger.warning(f"Review failed: {str(e)}, returning unreviewed transcript")
        return full_transcript


def main():
    if len(sys.argv) < 2:
        print("Usage: youtube_transcribe.py <youtube_url>", file=sys.stderr)
        sys.exit(1)
    
    youtube_url = sys.argv[1]
    
    # Validate API key
    if not openai.api_key:
        logger.error("OPENAI_API_KEY not found in environment")
        print("Error: OPENAI_API_KEY not configured", file=sys.stderr)
        sys.exit(1)
    
    # Create temp directory for processing
    temp_dir = tempfile.mkdtemp(prefix="youtube_transcribe_")
    logger.info(f"Working directory: {temp_dir}")
    
    try:
        # Download audio
        audio_path = download_audio(youtube_url, temp_dir)
        
        # Detect language
        language = detect_language(audio_path)
        
        # Split audio if needed
        chunks = split_audio(audio_path, temp_dir)
        
        # Transcribe chunks in parallel
        transcripts = transcribe_parallel(chunks, language)
        
        # Concatenate transcripts
        full_transcript = " ".join(transcripts)
        
        # Review with GPT
        if len(chunks) > 1 or len(full_transcript) > 500:
            final_transcript = review_transcript(full_transcript, language or "auto")
        else:
            final_transcript = full_transcript
        
        # Output to stdout (for clipboard)
        print(final_transcript)
        
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}")
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)
    finally:
        # Cleanup temp directory
        try:
            shutil.rmtree(temp_dir)
            logger.info("Cleanup complete")
        except Exception as e:
            logger.warning(f"Cleanup failed: {str(e)}")


if __name__ == "__main__":
    main()
