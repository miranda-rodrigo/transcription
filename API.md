# API Documentation

Documentação técnica dos componentes do YouTube Transcriber.

## 📦 Módulo Lua (init.lua)

### `transcribeYouTubeFromClipboard()`

Função principal que executa todo o workflow de transcrição.

**Retorno:** `void` (função assíncrona)

**Comportamento:**
1. Lê conteúdo do clipboard
2. Valida se é URL do YouTube
3. Mostra notificação de início
4. Executa script Python em background
5. Atualiza clipboard com resultado ou mostra erro

**Exemplo de uso:**
```lua
local ytTranscribe = dofile(hs.configdir .. "/youtube-transcribe/init.lua")
ytTranscribe.transcribeYouTubeFromClipboard()
```

**Notificações emitidas:**
- "Clipboard is empty!" - Se clipboard vazio
- "No YouTube URL found in clipboard!" - Se não for URL do YouTube
- "Starting transcription..." - Ao iniciar processamento
- "✅ Transcription completed!" - Ao concluir com sucesso
- "❌ Error: {mensagem}" - Se ocorrer erro

---

## 🐍 Script Python (youtube_transcribe.py)

### Uso via CLI

```bash
python3 youtube_transcribe.py <youtube_url>
```

**Argumentos:**
- `youtube_url` (string, obrigatório): URL completa do YouTube

**Variáveis de ambiente:**
- `OPENAI_API_KEY` (obrigatória): Chave da API OpenAI

**Saída:**
- **stdout**: Texto da transcrição (clean, para clipboard)
- **stderr**: Logs e mensagens de progresso
- **exit code**: 0 = sucesso, 1 = erro

**Exemplo:**
```bash
export OPENAI_API_KEY="sk-..."
python3 youtube_transcribe.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
```

### Funções Internas

#### `download_audio(url: str, output_dir: str) -> str`

Baixa áudio do YouTube usando yt-dlp.

**Parâmetros:**
- `url`: URL do YouTube
- `output_dir`: Diretório para salvar arquivo temporário

**Retorno:** Caminho do arquivo de áudio baixado

**Exceções:**
- `FileNotFoundError`: Se download falhar
- `Exception`: Erros de rede ou URL inválida

---

#### `split_audio(audio_path: str, output_dir: str) -> List[str]`

Divide áudio em chunks se necessário.

**Parâmetros:**
- `audio_path`: Caminho do arquivo de áudio
- `output_dir`: Diretório para salvar chunks

**Retorno:** Lista de caminhos dos chunks (ou arquivo original se pequeno)

**Limites:**
- `MAX_CHUNK_DURATION`: 10 minutos (600.000 ms)
- `MAX_FILE_SIZE`: 24 MB

**Comportamento:**
- Se áudio < 10 min E < 24 MB → retorna arquivo original
- Caso contrário → divide em chunks de 10 minutos

---

#### `detect_language(audio_path: str) -> Optional[str]`

Detecta idioma do áudio usando Whisper.

**Parâmetros:**
- `audio_path`: Caminho do arquivo de áudio

**Retorno:** Código do idioma (ex: "pt", "en", "es") ou `None` se falhar

**Comportamento:**
- Usa primeiros 30 segundos do áudio
- Chama Whisper API com `response_format="verbose_json"`
- Extrai campo `language` da resposta

---

#### `transcribe_chunk(chunk_path: str, language: Optional[str]) -> str`

Transcreve um único chunk de áudio.

**Parâmetros:**
- `chunk_path`: Caminho do chunk
- `language`: Código do idioma (opcional, para auto-detect use `None`)

**Retorno:** Texto transcrito do chunk

**API usada:** OpenAI Whisper-1

**Exceções:**
- `Exception`: Se transcrição falhar (arquivo corrompido, limite de API, etc.)

---

#### `transcribe_parallel(chunks: List[str], language: Optional[str]) -> List[str]`

Transcreve múltiplos chunks em paralelo.

**Parâmetros:**
- `chunks`: Lista de caminhos dos chunks
- `language`: Código do idioma (opcional)

**Retorno:** Lista de transcrições na mesma ordem dos chunks

**Comportamento:**
- Usa `ThreadPoolExecutor` com até 5 workers
- Preserva ordem original dos chunks
- Continua mesmo se um chunk falhar (retorna mensagem de erro)

---

#### `review_transcript(full_transcript: str, language: str) -> str`

Revisa transcrição com GPT para melhorar coerência.

**Parâmetros:**
- `full_transcript`: Texto completo concatenado
- `language`: Código do idioma

**Retorno:** Texto revisado e melhorado

**API usada:** GPT-4o-mini

**Comportamento:**
- Corrige erros de transcrição
- Melhora coerência entre chunks
- Adiciona pontuação adequada
- Preserva significado original
- Temperature: 0.3 (mais determinístico)

---

## 🔧 Configuração

### Variáveis de Ambiente

Arquivo `.env`:

```bash
# Obrigatória
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxx

# Opcionais (futuro)
# MAX_CHUNK_DURATION=600000  # 10 minutos em ms
# WHISPER_MODEL=whisper-1
# GPT_MODEL=gpt-4o-mini
```

### Constantes Configuráveis

Em `youtube_transcribe.py`:

```python
# Duração máxima de cada chunk (10 minutos)
MAX_CHUNK_DURATION = 10 * 60 * 1000  

# Tamanho máximo de arquivo (24 MB)
MAX_FILE_SIZE = 24 * 1024 * 1024
```

---

## 📊 Fluxo de Dados

```
┌─────────────┐
│  Clipboard  │ (YouTube URL)
└──────┬──────┘
       │
       ▼
┌─────────────────┐
│ Hammerspoon Lua │ (Validação e orquestração)
└────────┬────────┘
         │
         ▼
┌──────────────────────┐
│  Python Script       │
│  ─────────────────   │
│  1. download_audio   │
│  2. detect_language  │
│  3. split_audio      │
│  4. transcribe_*     │ (Parallel)
│  5. review_transcript│
└──────────┬───────────┘
           │
           ▼
┌──────────────────┐
│  OpenAI APIs     │
│  ─────────────   │
│  • Whisper       │ (Transcrição)
│  • GPT-4o-mini   │ (Revisão)
└──────────┬───────┘
           │
           ▼
┌─────────────┐
│  stdout     │ (Texto limpo)
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Clipboard  │ (Transcrição final)
└─────────────┘
```

---

## 🔌 Integração com Outras Ferramentas

### Via Shell

```bash
# Direto
python3 youtube_transcribe.py "URL" > transcript.txt

# Com pipe
echo "URL" | xargs python3 youtube_transcribe.py | pbcopy
```

### Via AppleScript

```applescript
set youtubeURL to the clipboard
do shell script "python3 youtube_transcribe.py " & quoted form of youtubeURL
set the clipboard to result
```

### Via JavaScript (JXA)

```javascript
const url = Application('System Events').clipboard()
const app = Application.currentApplication()
app.includeStandardAdditions = true
const result = app.doShellScript(`python3 youtube_transcribe.py "${url}"`)
app.setTheClipboardTo(result)
```

### Via Alfred Workflow

```bash
# Alfred Script Filter
query="{query}"
python3 youtube_transcribe.py "$query"
```

---

## 🚨 Códigos de Erro

| Exit Code | Significado                          |
|-----------|--------------------------------------|
| 0         | Sucesso                              |
| 1         | Erro genérico                        |

**Mensagens de erro comuns (stderr):**

- `OPENAI_API_KEY not found in environment` - API key não configurada
- `Download failed: {razão}` - Erro ao baixar vídeo
- `Transcription failed for {chunk}: {razão}` - Erro na transcrição
- `Review failed: {razão}` - Erro na revisão (retorna texto sem revisão)

---

## 📈 Performance

### Estimativas de Tempo

| Duração do Vídeo | Chunks | Tempo Aprox. | API Calls |
|------------------|--------|--------------|-----------|
| 5 minutos        | 1      | 30-60s       | 2-3       |
| 15 minutos       | 2      | 60-90s       | 3-4       |
| 30 minutos       | 3      | 90-120s      | 4-5       |
| 1 hora           | 6      | 2-3 min      | 7-8       |

**Fatores:**
- Download: 10-30s (depende da conexão)
- Transcrição: ~0.5-1x duração do áudio (em paralelo)
- Revisão: 5-15s

### Custos Estimados (USD)

| Duração | Whisper | GPT | Total  |
|---------|---------|-----|--------|
| 10 min  | $0.06   | ~$0 | $0.06  |
| 30 min  | $0.18   | ~$0 | $0.18  |
| 1 hora  | $0.36   | ~$0 | $0.36  |

*Preços referência (podem variar): Whisper $0.006/min, GPT-4o-mini ~$0.0001/request*

---

## 🧪 Testing

### Testes Manuais

```bash
# Teste básico
./test_local.sh "https://www.youtube.com/watch?v=jNQXAC9IVRw"

# Teste com vídeo curto (< 10 min)
python3 youtube_transcribe.py "URL_CURTA" 2>error.log

# Teste com vídeo longo (> 30 min)
python3 youtube_transcribe.py "URL_LONGA" 2>error.log

# Teste de detecção de idioma
python3 youtube_transcribe.py "URL_ESPANHOL" 2>error.log
```

### Validação

Checklist de testes:

- [ ] Vídeo curto (< 10 min) - sem chunks
- [ ] Vídeo médio (10-30 min) - 2-3 chunks
- [ ] Vídeo longo (> 30 min) - múltiplos chunks
- [ ] Diferentes idiomas (PT, EN, ES, FR)
- [ ] URLs em formatos diferentes (youtube.com, youtu.be)
- [ ] Vídeos com música/ruído de fundo
- [ ] Vídeos com múltiplos speakers

---

## 🔍 Debug

### Ativar Logs Detalhados

```python
# Em youtube_transcribe.py
logging.basicConfig(level=logging.DEBUG)  # Em vez de INFO
```

### Verificar Chamadas à API

```python
# Adicionar antes das chamadas da API
print(f"DEBUG: Calling Whisper API with {len(audio_file.read())} bytes")
print(f"DEBUG: Language: {language}")
```

### Console do Hammerspoon

```lua
-- Abrir console
hs.openConsole()

-- Testar módulo
dofile(hs.configdir .. "/youtube-transcribe/init.lua").transcribeYouTubeFromClipboard()
```

---

**Para mais informações, veja:**
- [README.md](README.md) - Guia de uso geral
- [INSTALL.md](INSTALL.md) - Instalação detalhada
- [INTEGRATION.md](INTEGRATION.md) - Exemplos de integração
