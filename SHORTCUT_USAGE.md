# Shortcut de Transcrição Universal

Este projeto agora inclui um **shortcut genérico de transcrição** que funciona com arquivos locais, URLs e clipboard, sem necessidade do Hammerspoon.

## 🎯 Funcionalidades

- ✅ **Arquivos locais**: MP4, MP3, WAV, M4A, WebM, OGG, FLAC, etc.
- ✅ **URLs**: YouTube, Vimeo, SoundCloud e outros suportados pelo yt-dlp
- ✅ **Clipboard**: Lê da área de transferência e copia resultado de volta (macOS)
- ✅ **Multi-idiomas**: Auto-detecção ou força idioma específico
- ✅ **IA Review**: Revisão opcional com OpenAI para melhorar a qualidade
- ✅ **Processamento paralelo**: Para arquivos longos (chunks automáticos)
- ✅ **Múltiplos formatos**: Conversão automática com ffmpeg

## 🚀 Instalação e Setup

```bash
# 1. Instalar dependências do sistema (macOS)
brew install ffmpeg yt-dlp

# 2. Configurar ambiente Python
make setup

# 3. [Opcional] Configurar OpenAI para revisão de texto
cp env.example .env
# Editar .env e adicionar: OPENAI_API_KEY=sua_chave_aqui
```

## 📋 Uso Básico

### Via Makefile (Recomendado)

```bash
# Transcrever arquivo local
make transcribe FILE=meu-video.mp4

# Transcrever URL do YouTube
make transcribe URL="https://youtu.be/abc123"

# Workflow com clipboard (macOS)
make transcribe-clipboard
```

### Via Script Direto

```bash
# Transcrever arquivo local
bin/transcribe-shortcut audio.wav

# Transcrever URL
bin/transcribe-shortcut "https://youtube.com/watch?v=..."

# Usar clipboard para entrada e saída
bin/transcribe-shortcut --from-clipboard --to-clipboard

# Forçar idioma específico
bin/transcribe-shortcut --language en video.mp4

# Salvar em arquivo
bin/transcribe-shortcut --output transcript.txt audio.mp3

# Ver todas as opções
bin/transcribe-shortcut --help
```

## 🔧 Opções Avançadas

### Modelos do Whisper
```bash
# Usar modelo maior (mais preciso, mais lento)
bin/transcribe-shortcut --model large video.mp4

# Usar modelo menor (mais rápido, menos preciso)  
bin/transcribe-shortcut --model tiny audio.wav
```

### Revisão com IA
```bash
# Forçar revisão (requer OPENAI_API_KEY)
bin/transcribe-shortcut --review audio.mp4

# Pular revisão mesmo com API key configurada
bin/transcribe-shortcut --no-review audio.mp4
```

### Performance
```bash
# Ajustar tamanho dos chunks (para arquivos longos)
bin/transcribe-shortcut --chunk-minutes 5 long-podcast.mp3

# Usar mais workers paralelos (mais RAM, mais rápido)
bin/transcribe-shortcut --chunk-workers 4 video.mp4
```

## 🌍 Criando Alias Global

Para usar de qualquer lugar no sistema:

```bash
# Adicionar ao seu ~/.bashrc ou ~/.zshrc
echo 'alias transcribe="'$(pwd)'/bin/transcribe-shortcut"' >> ~/.bashrc
source ~/.bashrc

# Agora pode usar de qualquer pasta:
transcribe ~/Downloads/video.mp4
transcribe --from-clipboard --to-clipboard
```

## 📱 Workflows Úteis

### 1. Transcrição Rápida de YouTube
```bash
# 1. Copie URL do YouTube
# 2. Execute:
make transcribe-clipboard
# 3. Transcrição estará no clipboard
```

### 2. Processar Vários Arquivos
```bash
# Bash loop para múltiplos arquivos
for file in *.mp4; do
  echo "Transcrevendo: $file"
  bin/transcribe-shortcut --output "${file%.mp4}.txt" "$file"
done
```

### 3. Transcrição com Configurações Personalizadas
```bash
# Criar script personalizado
cat > transcribe-pt << 'EOF'
#!/bin/bash
bin/transcribe-shortcut \
  --language pt \
  --model small \
  --review \
  --to-clipboard \
  "$@"
EOF
chmod +x transcribe-pt

# Usar:
./transcribe-pt video.mp4
```

## ⚙️ Variáveis de Ambiente

Você pode personalizar comportamento via `.env` ou variáveis de ambiente:

```bash
# Modelo Whisper padrão
WHISPER_MODEL=small

# Dispositivo (auto, cpu, cuda, metal)  
WHISPER_DEVICE=auto

# Tamanho dos chunks em minutos
CHUNK_MINUTES=10

# Workers paralelos
CHUNK_WORKERS=2

# Chave da OpenAI para revisão
OPENAI_API_KEY=sk-...

# Modelo da OpenAI para revisão
OPENAI_REVIEW_MODEL=gpt-4o-mini
```

## 🔍 Solução de Problemas

### Erro: "faster-whisper not found"
```bash
# Reinstalar dependências
make setup
```

### Erro: "ffmpeg not found"
```bash
# macOS
brew install ffmpeg

# Ubuntu/Debian
sudo apt install ffmpeg

# CentOS/RHEL
sudo yum install ffmpeg
```

### Erro: "pbpaste/pbcopy not found"
- Clipboard só funciona no macOS
- No Linux, o texto será impresso no terminal

### Arquivo muito grande/lento
```bash
# Usar modelo menor
bin/transcribe-shortcut --model tiny arquivo.mp4

# Diminuir chunks  
bin/transcribe-shortcut --chunk-minutes 5 arquivo.mp4

# Mais workers (se tiver RAM)
bin/transcribe-shortcut --chunk-workers 4 arquivo.mp4
```

## 🆚 Comparação com Versão YouTube

| Funcionalidade | transcribe-shortcut | transcribe-youtube-clipboard |
|---|---|---|
| Arquivos locais | ✅ | ❌ |
| URLs genéricas | ✅ | ❌ |
| YouTube | ✅ | ✅ |
| Clipboard | ✅ | ✅ |
| Multi-plataforma | ✅ (Linux/macOS) | macOS apenas |
| Hammerspoon | Não requer | Integração disponível |

## 📚 Exemplos Práticos

```bash
# Transcrever reunião gravada
bin/transcribe-shortcut --language pt --review meeting.m4a

# Transcrever podcast em inglês
bin/transcribe-shortcut --language en --model medium podcast.mp3

# Backup de transcrição do YouTube  
bin/transcribe-shortcut --output backup.txt "https://youtu.be/abc123"

# Workflow rápido para anotações
bin/transcribe-shortcut --from-clipboard --to-clipboard --review
```

---

💡 **Dica**: Use `make transcribe-clipboard` para o workflow mais rápido no dia a dia!