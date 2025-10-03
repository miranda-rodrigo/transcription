#!/bin/zsh
# Script de instalação para o Mac
# Execute este script no diretório onde extrair o tar.gz

echo "🚀 INSTALAÇÃO DO SISTEMA DE TRANSCRIÇÃO"
echo "======================================="

# Definir diretório de destino
DEST_DIR="/Users/rodrigomiranda/useful-repos/long-audio"

echo "📁 Criando estrutura de diretórios..."
mkdir -p "$DEST_DIR"

echo "📦 Movendo arquivos para $DEST_DIR..."

# Mover todos os arquivos para o diretório correto
mv video_transcription_processor.py "$DEST_DIR/" 2>/dev/null && echo "✅ video_transcription_processor.py"
mv transcribe_audio.sh "$DEST_DIR/" 2>/dev/null && echo "✅ transcribe_audio.sh"
mv check_setup.py "$DEST_DIR/" 2>/dev/null && echo "✅ check_setup.py"
mv video_transcription_requirements.txt "$DEST_DIR/" 2>/dev/null && echo "✅ video_transcription_requirements.txt"
mv env.transcription.example "$DEST_DIR/" 2>/dev/null && echo "✅ env.transcription.example"
mv GUIA_RECORDING.md "$DEST_DIR/" 2>/dev/null && echo "✅ GUIA_RECORDING.md"
mv GUIA_RAPIDO.md "$DEST_DIR/" 2>/dev/null && echo "✅ GUIA_RAPIDO.md"
mv VIDEO_TRANSCRIPTION_README.md "$DEST_DIR/" 2>/dev/null && echo "✅ VIDEO_TRANSCRIPTION_README.md"

# Tornar scripts executáveis
chmod +x "$DEST_DIR/transcribe_audio.sh"

echo ""
echo "✅ INSTALAÇÃO CONCLUÍDA!"
echo "📁 Arquivos instalados em: $DEST_DIR"
echo ""
echo "🔧 PRÓXIMOS PASSOS:"
echo "1. cd $DEST_DIR"
echo "2. Configurar OpenAI (opcional): cp env.transcription.example .env"
echo "3. Editar .env com sua chave da OpenAI"
echo "4. Instalar dependências: /Users/rodrigomiranda/.pyenv/shims/pip install -r video_transcription_requirements.txt"
echo "5. Executar: ./transcribe_audio.sh"
echo ""
echo "📄 Consulte GUIA_RECORDING.md para instruções detalhadas"