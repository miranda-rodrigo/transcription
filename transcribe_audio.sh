#!/bin/zsh
# Script para transcrever o áudio Recording.m4a
# Adaptado para ambiente macOS com pyenv e Homebrew

# Configurar PATH para pyenv e Homebrew
export PATH="/opt/homebrew/bin:/Users/rodrigomiranda/.pyenv/shims:$PATH"

# Carregar variáveis de ambiente do .env
if [ -f .env ]; then
    export $(grep -v '^#' .env | xargs)
fi

echo "🎵 PROCESSADOR DE TRANSCRIÇÃO DE ÁUDIO 🎵"
echo "=========================================="
echo "Arquivo: /Users/rodrigomiranda/useful-repos/audio_transcription/long-audio/Recording.m4a"
echo ""

# Verificar se Python está disponível via pyenv
if ! command -v /Users/rodrigomiranda/.pyenv/shims/python3 &> /dev/null; then
    echo "❌ Python3 via pyenv não encontrado. Verifique a instalação do pyenv."
    exit 1
fi

# Verificar se FFmpeg está disponível
if ! command -v /opt/homebrew/bin/ffmpeg &> /dev/null; then
    echo "❌ FFmpeg não encontrado. Instale com: brew install ffmpeg"
    exit 1
fi

# Verificar se o arquivo de áudio existe
AUDIO_FILE="/Users/rodrigomiranda/useful-repos/audio_transcription/long-audio/Recording.m4a"
if [[ ! -f "$AUDIO_FILE" ]]; then
    echo "❌ Arquivo não encontrado: $AUDIO_FILE"
    exit 1
fi

echo "✅ Arquivo encontrado: Recording.m4a"
echo "📋 Verificando configuração..."

# Executar verificações (opcional)
/Users/rodrigomiranda/.pyenv/shims/python3 check_setup.py

echo ""
echo "🚀 Iniciando processamento de transcrição..."
echo "⏱️  Este processo pode levar algum tempo dependendo do tamanho do áudio..."
echo ""

# Executar o processamento principal
/Users/rodrigomiranda/.pyenv/shims/python3 video_transcription_processor.py

echo ""
echo "✅ Processamento concluído!"
echo "📁 Verifique a pasta 'transcription_output/' para os resultados."
echo "📄 Arquivo final: transcription_output/transcricao-final.txt"