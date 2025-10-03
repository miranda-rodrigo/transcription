#!/bin/bash
# Optimized shell script for macOS Shortcuts 
# Input: Clipboard | Pass Input: as arguments

set -euo pipefail

# Add Homebrew bin to PATH (fixes ffmpeg not found in Shortcuts app)
export PATH="/opt/homebrew/bin:/opt/homebrew/sbin:$PATH"

# Function to extract YouTube URL from HTML file
extract_youtube_url() {
    local file="$1"
    if [ -f "$file" ] && [[ "$file" == *.html ]]; then
        # Extract canonical URL from HTML
        url=$(grep -oE '<link rel="canonical" href="https://www\.youtube\.com/watch\?v=[^"]+"' "$file" | sed -E 's/.*href="([^"]+)".*/\1/')
        if [ -n "$url" ]; then
            echo "$url"
            return 0
        fi
    fi
    return 1
}

# Check if we have an argument (from clipboard or share sheet)
if [ $# -gt 0 ] && [ -n "$1" ]; then
    input="$1"
    
    # If it's an HTML file, extract URL
    extracted_url=$(extract_youtube_url "$input")
    if [ $? -eq 0 ]; then
        echo "URL extraída do HTML: $extracted_url"
        ./bin/transcribe-shortcut "$extracted_url"
    else
        # Use input as is (URL or file path)
        ./bin/transcribe-shortcut "$input"
    fi
else
    # Fallback to clipboard workflow
    ./bin/transcribe-shortcut --from-clipboard --to-clipboard
fi