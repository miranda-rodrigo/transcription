# 🎥 Processador de Transcrição de Vídeo

Script Python completo para transcrever e refinar arquivos de vídeo longos com alta qualidade.

## 📋 Funcionalidades

1. **Melhoria da Qualidade do Áudio**
   - Remove ruído de fundo
   - Normalização dinâmica
   - Filtros de frequência
   - Compressão de áudio

2. **Divisão Inteligente em Chunks**
   - Detecta momentos de silêncio
   - Evita cortar palavras no meio
   - Chunks de duração configurável (padrão: 5 minutos)

3. **Transcrição com Whisper**
   - Modelo large-v2 para máxima qualidade
   - Suporte a GPU quando disponível
   - Transcrição em português

4. **Refinamento com IA**
   - Correção de erros de transcrição
   - Melhoria da pontuação
   - União de frases cortadas entre chunks
   - Formatação profissional

## 🚀 Instalação

### Pré-requisitos

1. **Python 3.8+**
2. **FFmpeg** (obrigatório)
   ```bash
   # Ubuntu/Debian
   sudo apt update && sudo apt install ffmpeg
   
   # macOS
   brew install ffmpeg
   
   # Windows: Baixar do site oficial
   ```

### Dependências Python

```bash
pip install -r video_transcription_requirements.txt
```

### Configuração da API OpenAI (opcional)

1. Crie um arquivo `.env`:
   ```bash
   OPENAI_API_KEY=sua_chave_api_aqui
   ```

2. Ou defina a variável de ambiente:
   ```bash
   export OPENAI_API_KEY="sua_chave_api_aqui"
   ```

## 📁 Uso

### Uso Básico

1. Coloque seu arquivo de vídeo como `Recording.mp4` no diretório do script
2. Execute o script:
   ```bash
   python video_transcription_processor.py
   ```

### Arquivos de Saída

O script cria um diretório `transcription_output/` com:

- `enhanced_audio.wav` - Áudio processado e melhorado
- `audio_chunks/` - Chunks individuais do áudio
- `transcricao-bruta.txt` - Transcrição inicial (automática)
- `transcricao-final.txt` - Transcrição refinada com IA
- `transcription_process.log` - Log detalhado do processamento

## ⚙️ Personalização

Você pode modificar os parâmetros no script:

```python
processor = VideoTranscriptionProcessor(
    input_video="Recording.mp4",           # Arquivo de entrada
    chunk_duration_minutes=5,              # Duração dos chunks
    whisper_model_size="large-v2"          # Tamanho do modelo Whisper
)
```

### Modelos Whisper Disponíveis

- `tiny` - Mais rápido, menor qualidade
- `base` - Balanceado
- `small` - Boa qualidade
- `medium` - Alta qualidade
- `large-v2` - Máxima qualidade (recomendado)

## 📊 Estatísticas de Processamento

O script fornece informações detalhadas:
- Tempo total de processamento
- Número de chunks criados
- Status de cada etapa
- Caminhos dos arquivos gerados

## 🔧 Solução de Problemas

### Erro: FFmpeg não encontrado
```bash
# Instale o FFmpeg conforme as instruções acima
```

### Erro: Memória insuficiente
- Use um modelo Whisper menor (`medium` ou `small`)
- Reduza a duração dos chunks para 3-4 minutos

### Erro: OpenAI API
- Verifique se a chave da API está configurada corretamente
- O refinamento com IA é opcional - o script continua sem ela

### Áudio de baixa qualidade
- Verifique se o arquivo de vídeo original tem boa qualidade de áudio
- Ajuste os filtros no método `extract_and_enhance_audio()`

## 📝 Logs

Todos os logs são salvos em `transcription_process.log` para debug e acompanhamento.

## 🎯 Exemplo de Uso Completo

```bash
# 1. Preparar ambiente
pip install -r video_transcription_requirements.txt

# 2. Configurar API (opcional)
echo "OPENAI_API_KEY=sua_chave" > .env

# 3. Colocar vídeo no diretório
# (certifique-se que Recording.mp4 está presente)

# 4. Executar processamento
python video_transcription_processor.py

# 5. Verificar resultados em transcription_output/
```

## ⚡ Performance

- **GPU**: Automaticamente detectada para acelerar a transcrição
- **CPU**: Otimizado para processamento multicore
- **Memória**: Processamento em chunks para arquivos grandes
- **Tempo**: ~1-2x o tempo real do vídeo (depende do hardware)

## 🛡️ Limitações

- Requer FFmpeg instalado no sistema
- Arquivos muito grandes podem precisar de mais RAM
- Refinamento com IA requer chave da OpenAI
- Melhor resultado com áudio limpo e claro

---

**Desenvolvido especialmente para processamento de Recording.mp4 com máxima qualidade de transcrição.**