#!/bin/bash
# Setup script for YouTube Transcription Hammerspoon Module
# For macOS

set -e

echo "🔧 YouTube Transcription Setup for Hammerspoon"
echo "=============================================="
echo ""

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Check if Hammerspoon is installed
if [ ! -d "$HOME/.hammerspoon" ]; then
    echo "⚠️  Hammerspoon config directory not found!"
    echo "Please install Hammerspoon first: https://www.hammerspoon.org/"
    exit 1
fi

# Check for Homebrew
if ! command -v brew &> /dev/null; then
    echo "⚠️  Homebrew not found!"
    echo "Please install Homebrew first: https://brew.sh/"
    exit 1
fi

# Check/install ffmpeg
echo "📦 Checking for ffmpeg..."
if ! command -v ffmpeg &> /dev/null; then
    echo "Installing ffmpeg via Homebrew..."
    brew install ffmpeg
else
    echo "✅ ffmpeg already installed"
fi

# Check for Python 3
if ! command -v python3 &> /dev/null; then
    echo "⚠️  Python 3 not found!"
    echo "Please install Python 3: brew install python3"
    exit 1
fi

echo ""
echo "🐍 Setting up Python virtual environment..."
python3 -m venv venv

echo "📦 Installing Python dependencies..."
./venv/bin/pip install --upgrade pip
./venv/bin/pip install -r requirements.txt

echo ""
echo "🔑 Checking for API key..."
if [ ! -f .env ]; then
    if [ -f env.example ]; then
        cp env.example .env
        echo "⚠️  Created .env file from template"
        echo "Please edit .env and add your OPENAI_API_KEY"
        echo ""
        read -p "Do you want to add your API key now? (y/n) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            read -p "Enter your OpenAI API key: " api_key
            echo "OPENAI_API_KEY=$api_key" > .env
            echo "✅ API key saved to .env"
        fi
    else
        echo "⚠️  No .env file found. Creating one..."
        echo "OPENAI_API_KEY=your_key_here" > .env
        echo "Please edit .env and add your OPENAI_API_KEY"
    fi
else
    echo "✅ .env file already exists"
fi

echo ""
echo "📁 Creating Hammerspoon module directory..."
MODULE_DIR="$HOME/.hammerspoon/youtube-transcribe"
mkdir -p "$MODULE_DIR"

echo "📋 Copying files to Hammerspoon directory..."
cp youtube_transcribe.py "$MODULE_DIR/"
cp .env "$MODULE_DIR/" 2>/dev/null || echo "⚠️  .env not copied (configure it later)"
cp requirements.txt "$MODULE_DIR/"

# Copy or link venv
if [ -d "venv" ]; then
    echo "🔗 Linking virtual environment..."
    ln -sf "$SCRIPT_DIR/venv" "$MODULE_DIR/venv"
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "📝 Next steps:"
echo "1. Make sure your OpenAI API key is set in $MODULE_DIR/.env"
echo "2. Add this to your ~/.hammerspoon/init.lua:"
echo ""
echo "   -- YouTube Transcription"
echo "   local ytTranscribe = require('init')"
echo "   hs.hotkey.bind({'cmd', 'shift'}, 'T', function()"
echo "       ytTranscribe.transcribeYouTubeFromClipboard()"
echo "   end)"
echo ""
echo "   Or use this minimal integration:"
echo "   hs.hotkey.bind({'cmd', 'shift'}, 'T', function()"
echo "       dofile(hs.configdir .. '/init.lua').transcribeYouTubeFromClipboard()"
echo "   end)"
echo ""
echo "3. Reload Hammerspoon config"
echo "4. Copy a YouTube URL to clipboard and press Cmd+Shift+T"
echo ""
