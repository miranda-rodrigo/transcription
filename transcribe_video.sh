#!/bin/bash
# Script executável para processar transcrição de vídeo
# Uso: ./transcribe_video.sh

set -e  # Parar se houver erro

echo "🎥 PROCESSADOR DE TRANSCRIÇÃO DE VÍDEO 🎥"
echo "=========================================="

# Verificar se Python está disponível
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 não encontrado. Por favor, instale Python 3.8+"
    exit 1
fi

# Verificar se o arquivo existe
if [[ ! -f "Recording.mp4" ]]; then
    echo "❌ Arquivo 'Recording.mp4' não encontrado!"
    echo "Por favor, coloque seu arquivo de vídeo como 'Recording.mp4' neste diretório."
    exit 1
fi

echo "📋 Verificando configuração..."

# Executar verificações
python3 check_setup.py

# Se chegou até aqui, está tudo OK
echo ""
echo "🚀 Iniciando processamento..."
echo ""

# Executar o processamento principal
python3 video_transcription_processor.py

echo ""
echo "✅ Processamento concluído!"
echo "📁 Verifique a pasta 'transcription_output/' para os resultados."