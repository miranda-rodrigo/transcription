### Módulo Hammerspoon: YouTube Transcribe

- **Função**: `youtube_transcribe.transcribeFromClipboard()` lê um URL do YouTube da área de transferência, chama o script Python e copia o transcript final para a área de transferência.
- **Hotkey opcional**: `youtube_transcribe.bindHotkey({'cmd','alt'}, 't')`.

### Instalação
- Requer macOS, Hammerspoon, Python 3, e Homebrew.
- Instale dependências de sistema:
  - `brew install ffmpeg yt-dlp`
- Instale dependências Python no repositório:
  - `make setup`

### Uso
- Copie um URL do YouTube para a área de transferência.
- No Console do Hammerspoon: `require('youtube_transcribe').transcribeFromClipboard()`
- Opcionalmente, adicione ao `~/.hammerspoon/init.lua`:
```lua
local yt = dofile('/caminho/para/este/repo/hammerspoon/youtube_transcribe.lua')
yt.bindHotkey({'cmd','alt'}, 't')
```

### Notas
- O script Python autodetecta idioma com `faster-whisper` e, se houver `OPENAI_API_KEY`, roda uma revisão final com `OpenAI` e copia para a área de transferência.
- Nada é salvo permanentemente; apenas arquivos temporários durante o processamento.





