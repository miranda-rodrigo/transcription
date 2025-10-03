### YouTube Audio → Transcript (macOS, Hammerspoon + Python)

- **Objetivo**: Ao executar um único comando ou hotkey no Hammerspoon, ler um URL do YouTube da área de transferência, baixar o áudio (yt-dlp + ffmpeg), dividir em chunks se necessário, transcrever em paralelo com `faster-whisper`, revisar com OpenAI (opcional) e copiar o transcript final de volta para a área de transferência. Sem salvar arquivos finais.

### Dependências
- **macOS** com clipboard (`pbcopy/pbpaste`)
- **Homebrew**: `brew install ffmpeg yt-dlp`
- **Python 3** (recomendado via `pyenv` ou sistema)

### Setup
```bash
make setup
```

Defina sua `OPENAI_API_KEY` no ambiente (opcional para revisão):
```bash
export OPENAI_API_KEY=...  # adicione ao seu shell rc
```

### Uso (CLI)
- Copie um URL do YouTube para a área de transferência.
- Rode:
```bash
make run
```
Ou diretamente:
```bash
bin/transcribe-youtube-clipboard
```

O script Python cuida de baixar, transcrever, revisar (se possível) e copiar o texto para a área de transferência.

### Uso (Hammerspoon)
- Veja `hammerspoon/README.md` e `hammerspoon/youtube_transcribe.lua`.

### Implementação
- `scripts/transcribe_youtube.py`: pipeline Python com `yt-dlp`, `ffmpeg`, chunking (`pydub`), transcrição (`faster-whisper`), revisão opcional (`OpenAI`), clipboard, e limpeza de temporários.
- `bin/transcribe-youtube-clipboard`: wrapper CLI macOS que lê o URL da área de transferência e chama o Python.
- `Makefile`: `setup` e `run`.

<<<<<<< Current (Your changes)
- O arquivo `.env` está incluído no `.gitignore` para proteger suas chaves de API
- Nunca commite chaves de API diretamente no código
- Use sempre o arquivo `.env` para variáveis sensíveis
=======
### Observações
- Autodetecção de idioma pelo Whisper; revisão preserva idioma.
- Erros comuns (faltam deps, URL inválido) retornam mensagens claras.
- Nada é salvo além de temporários; transcript final fica no clipboard e também é impresso no stdout como fallback.
>>>>>>> Incoming (Background Agent changes)
