# 🎵 GUIA RÁPIDO - Transcrição do Recording.m4a

## ⚡ Como usar (ambiente macOS com pyenv)

### 1. Executar o processamento
```bash
# Opção 1: Script otimizado (recomendado)
./transcribe_audio.sh

# Opção 2: Python direto
/Users/rodrigomiranda/.pyenv/shims/python3 video_transcription_processor.py
```

### 2. Verificar se tudo está OK (opcional)
```bash
/Users/rodrigomiranda/.pyenv/shims/python3 check_setup.py
```

## 📁 Arquivo processado
**Localização**: `/Users/rodrigomiranda/useful-repos/audio_transcription/long-audio/Recording.m4a`

## 📋 Pré-requisitos (já configurados no seu ambiente)
✅ **Python via pyenv**: `/Users/rodrigomiranda/.pyenv/shims/python3`  
✅ **FFmpeg via Homebrew**: `/opt/homebrew/bin/ffmpeg`  
✅ **Chave OpenAI**: Carregada do arquivo `.env`  

## 🎯 O que o script faz

1. **Processa o áudio M4A**:
   - Remove ruído de fundo
   - Normaliza volume
   - Converte para formato otimizado

2. **Divide em chunks de 5 minutos**:
   - Quebra em momentos de silêncio
   - Evita cortar palavras

3. **Transcreve com Whisper large-v2**:
   - Máxima qualidade de transcrição
   - Usa GPU se disponível
   - Otimizado para português

4. **Refina com OpenAI GPT-4**:
   - Corrige erros de transcrição
   - Melhora pontuação e formatação
   - Une frases cortadas entre chunks

## 📂 Arquivos gerados

```
transcription_output/
├── transcricao-bruta.txt      ← Transcrição automática inicial
├── transcricao-final.txt      ← RESULTADO FINAL ✅
├── enhanced_audio.wav         ← Áudio processado
├── audio_chunks/              ← Chunks individuais
└── transcription_process.log  ← Log detalhado
```

## ⏱️ Tempo estimado

- **Para áudio de 1 hora**: ~30-60 minutos de processamento
- **Primeiro uso**: +10-15 minutos (download do modelo Whisper)
- **Com GPU**: 2-3x mais rápido

## 🎯 Resultado final

O arquivo `transcricao-final.txt` conterá:
- Texto limpo e bem formatado
- Parágrafos organizados logicamente
- Pontuação e gramática corrigidas
- Indicação de trechos com áudio ruim
- Cabeçalho com informações do processamento

---

**💡 Dica**: O script está configurado especificamente para seu ambiente macOS. Apenas execute `./transcribe_audio.sh` e aguarde o processamento!