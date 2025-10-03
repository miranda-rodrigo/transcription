# 🎥 GUIA RÁPIDO DE USO - Processador de Transcrição de Vídeo

## ⚡ Uso Simples (3 passos)

### 1. Preparar o ambiente
```bash
# Instalar dependências
pip install -r video_transcription_requirements.txt

# Configurar OpenAI (opcional, para refinamento)
cp env.transcription.example .env
# Editar .env e adicionar sua chave da OpenAI
```

### 2. Colocar seu vídeo
- Renomeie seu arquivo de vídeo para `Recording.mp4`
- Coloque-o no mesmo diretório dos scripts

### 3. Executar processamento
```bash
# Opção 1: Script automatizado (recomendado)
./transcribe_video.sh

# Opção 2: Python direto
python3 video_transcription_processor.py

# Opção 3: Verificação antes de executar
python3 check_setup.py
```

## 📋 Pré-requisitos Obrigatórios

- **Python 3.8+**
- **FFmpeg** instalado no sistema
- **Pelo menos 4GB RAM** disponível
- **Espaço em disco**: ~3x o tamanho do vídeo original

## 📁 Arquivos Criados

Após o processamento, você terá:

```
transcription_output/
├── transcricao-bruta.txt      ← Transcrição automática inicial
├── transcricao-final.txt      ← Transcrição refinada (RESULTADO FINAL)
├── enhanced_audio.wav         ← Áudio processado
├── audio_chunks/              ← Chunks individuais
└── transcription_process.log  ← Log detalhado
```

## ⚙️ O que o script faz automaticamente:

1. **Melhora a qualidade do áudio**:
   - Remove ruído de fundo
   - Normaliza volume
   - Aplica filtros de frequência

2. **Divide em chunks inteligentes**:
   - Chunks de ~5 minutos
   - Quebra em momentos de silêncio
   - Evita cortar palavras

3. **Transcreve com Whisper**:
   - Modelo large-v2 (máxima qualidade)
   - Usa GPU se disponível
   - Otimizado para português

4. **Refina com IA** (se configurado):
   - Corrige erros de transcrição
   - Melhora pontuação
   - Une frases cortadas
   - Formatação profissional

## 🚨 Resolução de Problemas

### Erro: "FFmpeg not found"
```bash
# Ubuntu/Debian
sudo apt update && sudo apt install ffmpeg

# macOS
brew install ffmpeg
```

### Erro: "Recording.mp4 not found"
- Certifique-se que seu arquivo se chama exatamente `Recording.mp4`
- Deve estar no mesmo diretório dos scripts

### Processamento muito lento
- Use um modelo Whisper menor: edite o script e mude `large-v2` para `medium`
- Reduza o tamanho dos chunks para 3 minutos

### Refinamento com IA não funciona
- Configure a chave da OpenAI no arquivo `.env`
- O script funciona sem IA, mas a qualidade será menor

## 📊 Tempo Estimado

- **Vídeo de 1 hora**: ~30-60 minutos de processamento
- **GPU disponível**: 2-3x mais rápido
- **Primeiro uso**: +10-15 min (download do modelo Whisper)

## 🎯 Resultado Final

O arquivo `transcricao-final.txt` conterá:
- Texto limpo e bem formatado
- Parágrafos organizados
- Pontuação correta
- Indicação de trechos com áudio ruim
- Cabeçalho com informações do processamento

---

**💡 Dica**: Execute `python3 check_setup.py` primeiro para verificar se tudo está configurado corretamente!