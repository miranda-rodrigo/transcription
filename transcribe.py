#!/usr/bin/env python3
"""
Simplified Audio/Video Transcription Script

Handles local files or URLs (YouTube, etc.), splits long audio, transcribes in parallel using Whisper,
concatenates, and reviews with GPT for coherence.

Dependencies (install manually):
pip install openai yt-dlp pydub python-dotenv requests

Set OPENAI_API_KEY in .env file.
"""

import os
import sys
import time
import argparse
import subprocess
import concurrent.futures
from pathlib import Path
from typing import List, Optional
import logging
from dotenv import load_dotenv
import openai
from pydub import AudioSegment
import yt_dlp
import requests

# Setup
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

MAX_CHUNK_DURATION = 10 * 60 * 1000  # 10 minutes in ms

def download_audio(url: str, output_dir: str) -> str:
    """Download audio from URL using yt-dlp."""
    output_path = os.path.join(output_dir, "downloaded_audio.%(ext)s")
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': output_path,
        'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3'}],
        'quiet': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    # Find the downloaded file
    for file in os.listdir(output_dir):
        if file.startswith("downloaded_audio."):
            return os.path.join(output_dir, file)
    raise ValueError("Download failed")

def split_audio(audio_path: str, output_dir: str) -> List[str]:
    """Split audio into chunks if longer than MAX_CHUNK_DURATION."""
    audio = AudioSegment.from_file(audio_path)
    chunks = []
    if len(audio) <= MAX_CHUNK_DURATION:
        return [audio_path]
    
    for i in range(0, len(audio), MAX_CHUNK_DURATION):
        chunk = audio[i:i + MAX_CHUNK_DURATION]
        chunk_path = os.path.join(output_dir, f"chunk_{i//MAX_CHUNK_DURATION}.mp3")
        chunk.export(chunk_path, format="mp3")
        chunks.append(chunk_path)
    return chunks

def transcribe_chunk(chunk_path: str, language: str = "pt") -> str:
    """Transcribe a single audio chunk using Whisper."""
    client = openai.OpenAI()
    with open(chunk_path, "rb") as audio_file:
        response = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
            language=language,
            response_format="text"
        )
    return response

def review_transcript(full_transcript: str, language: str) -> str:
    """Use GPT to review and correct the concatenated transcript for coherence."""
    client = openai.OpenAI()
    prompt = f"Revise this transcript for coherence, fixing any issues from chunking. Original language: {language}\n\n{full_transcript}"
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

def main():
    parser = argparse.ArgumentParser(description="Transcribe audio from file or URL.")
    parser.add_argument("input", help="Local file path or URL")
    parser.add_argument("--language", "-l", default="pt", help="Language code (default: pt)")
    parser.add_argument("--output-dir", "-o", default=".", help="Output directory")
    args = parser.parse_args()

    output_dir = args.output_dir
    os.makedirs(output_dir, exist_ok=True)
    
    # Download if URL
    if args.input.startswith("http"):
        logger.info("Downloading audio from URL...")
        audio_path = download_audio(args.input, output_dir)
    else:
        audio_path = args.input
    
    # Split
    chunks = split_audio(audio_path, output_dir)
    
    # Parallel transcribe
    transcripts = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(transcribe_chunk, chunk, args.language) for chunk in chunks]
        for future in concurrent.futures.as_completed(futures):
            transcripts.append(future.result())
    
    # Concatenate
    full_transcript = " ".join(transcripts)
    
    # Review
    reviewed = review_transcript(full_transcript, args.language)
    
    # Save
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    output_path = os.path.join(output_dir, f"transcript_{timestamp}.txt")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(reviewed)
    
    logger.info(f"Transcript saved to: {output_path}")
    print(reviewed)

if __name__ == "__main__":
    main()

