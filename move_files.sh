#!/bin/bash
# Script para mover arquivos de transcrição para o diretório correto

# Diretório de destino
DEST_DIR="/Users/rodrigomiranda/useful-repos/long-audio"

echo "🚀 MOVENDO ARQUIVOS DE TRANSCRIÇÃO"
echo "=================================="
echo "Destino: $DEST_DIR"
echo ""

# Verificar se o diretório de destino existe
if [ ! -d "$DEST_DIR" ]; then
    echo "📁 Criando diretório: $DEST_DIR"
    mkdir -p "$DEST_DIR"
fi

# Lista de arquivos para mover
FILES_TO_MOVE=(
    "video_transcription_processor.py"
    "transcribe_audio.sh"
    "check_setup.py"
    "video_transcription_requirements.txt"
    "env.transcription.example"
    "GUIA_RECORDING.md"
    "GUIA_RAPIDO.md"
    "VIDEO_TRANSCRIPTION_README.md"
)

echo "📦 Movendo arquivos..."

for file in "${FILES_TO_MOVE[@]}"; do
    if [ -f "$file" ]; then
        echo "✅ Movendo: $file"
        mv "$file" "$DEST_DIR/"
    else
        echo "⚠️  Arquivo não encontrado: $file"
    fi
done

echo ""
echo "✅ ARQUIVOS MOVIDOS COM SUCESSO!"
echo "📁 Localização: $DEST_DIR"
echo ""
echo "🎯 Para executar a transcrição:"
echo "cd $DEST_DIR"
echo "./transcribe_audio.sh"
echo ""
echo "📋 Arquivos movidos:"
cd "$DEST_DIR" && ls -la *.py *.sh *.txt *.md 2>/dev/null || echo "Navegue para o diretório para ver os arquivos"