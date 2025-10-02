# YouTube Audio Transcription for Hammerspoon

🎥 → 🎙️ → 📝

Módulo Hammerspoon que transcreve vídeos do YouTube diretamente da área de transferência usando Whisper AI.

> **⚡ Começar rápido?** Veja [QUICKSTART.md](QUICKSTART.md) para configuração em 5 minutos!

## ✨ Funcionalidades

- 📋 **Clipboard-first**: Cole um URL do YouTube, pressione um atalho, receba a transcrição
- 🎯 **Detecção automática de idioma**: Whisper detecta o idioma automaticamente
- ✂️ **Divisão inteligente**: Divide áudios longos em chunks e transcreve em paralelo
- 🔄 **Revisão com GPT**: Melhora a coerência do texto transcrito
- 🚀 **Processamento assíncrono**: Não trava o Hammerspoon durante a transcrição
- 🧹 **Sem arquivos salvos**: Tudo via clipboard, arquivos temporários são limpos automaticamente

## 📋 Requisitos

- **macOS** (10.15+)
- **Hammerspoon** ([download](https://www.hammerspoon.org/))
- **Homebrew** ([install](https://brew.sh/))
- **Python 3.8+**
- **OpenAI API Key** com acesso ao Whisper API

## 🚀 Instalação Rápida

```bash
# Clone ou baixe este repositório
git clone <repo-url>
cd youtube-transcribe

# Execute o script de setup (instala dependências e configura)
./setup.sh
```

O script de setup irá:
1. Verificar/instalar `ffmpeg` via Homebrew
2. Criar ambiente virtual Python
3. Instalar dependências Python
4. Configurar arquivo `.env` com sua chave OpenAI
5. Copiar arquivos para `~/.hammerspoon/youtube-transcribe/`

## ⚙️ Configuração do Hammerspoon

Adicione ao seu `~/.hammerspoon/init.lua`:

### Opção 1: Como módulo standalone (recomendado para testar)

```lua
-- YouTube Transcription
local ytTranscribe = dofile(hs.configdir .. "/youtube-transcribe/init.lua")

-- Bind to Cmd+Shift+T
hs.hotkey.bind({"cmd", "shift"}, "T", function()
    ytTranscribe.transcribeYouTubeFromClipboard()
end)
```

### Opção 2: Integração no seu init.lua existente

Copie o conteúdo de `init.lua` para o seu arquivo principal e ajuste conforme necessário.

### Opção 3: Como função simples

```lua
hs.hotkey.bind({"cmd", "shift"}, "T", function()
    local url = hs.pasteboard.getContents()
    if url and (string.match(url, "youtube%.com") or string.match(url, "youtu%.be")) then
        hs.notify.new({title="YouTube Transcribe", informativeText="Starting..."}):send()
        local scriptPath = hs.configdir .. "/youtube-transcribe"
        local cmd = string.format('%s/venv/bin/python3 %s/youtube_transcribe.py "%s"', scriptPath, scriptPath, url)
        hs.task.new("/bin/bash", function(exit, stdout, stderr)
            if exit == 0 then
                hs.pasteboard.setContents(stdout)
                hs.notify.new({title="YouTube Transcribe", informativeText="✅ Done!"}):send()
            else
                hs.notify.new({title="YouTube Transcribe", informativeText="❌ Error: " .. stderr}):send()
            end
        end, {"-c", cmd}):start()
    end
end)
```

## 📚 Documentação

- **[QUICKSTART.md](QUICKSTART.md)** - Comece em 5 minutos ⚡
- **[INSTALL.md](INSTALL.md)** - Guia de instalação detalhado
- **[INTEGRATION.md](INTEGRATION.md)** - Integrações avançadas
- **[API.md](API.md)** - Documentação técnica completa
- **[example_config.lua](example_config.lua)** - Exemplos de configuração

## 📖 Como Usar

1. **Copie um URL do YouTube** para a área de transferência:
   ```
   https://www.youtube.com/watch?v=dQw4w9WgXcQ
   ```

2. **Pressione o atalho configurado** (ex: `Cmd+Shift+T`)

3. **Aguarde a notificação** - O processo pode levar alguns minutos dependendo do tamanho do vídeo

4. **Cole o resultado** - A transcrição estará na área de transferência

## 🔧 Configuração Manual

Se preferir não usar o `setup.sh`:

### 1. Instalar dependências do sistema

```bash
brew install ffmpeg python3
```

### 2. Criar ambiente virtual e instalar pacotes Python

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Configurar chave da API

Crie um arquivo `.env`:

```bash
cp env.example .env
# Edite .env e adicione sua chave:
# OPENAI_API_KEY=sk-...
```

### 4. Copiar para Hammerspoon

```bash
mkdir -p ~/.hammerspoon/youtube-transcribe
cp youtube_transcribe.py ~/.hammerspoon/youtube-transcribe/
cp .env ~/.hammerspoon/youtube-transcribe/
cp -r venv ~/.hammerspoon/youtube-transcribe/
```

## 🏗️ Estrutura do Projeto

```
youtube-transcribe/
├── init.lua                 # Módulo Hammerspoon (interface Lua)
├── youtube_transcribe.py    # Script Python (lógica principal)
├── requirements.txt         # Dependências Python
├── setup.sh                # Script de instalação automatizada
├── env.example             # Template para variáveis de ambiente
├── .env                    # Chave da API (não commitado)
├── .gitignore             # Arquivos ignorados
└── README.md              # Esta documentação
```

## 🔍 Como Funciona

1. **Hammerspoon (Lua)**: Lê clipboard, valida URL, chama Python, atualiza clipboard com resultado
2. **Python Script**:
   - Baixa áudio do YouTube com `yt-dlp`
   - Detecta idioma automaticamente com Whisper
   - Divide em chunks de 10 minutos (se necessário)
   - Transcreve chunks em paralelo com Whisper API
   - Concatena transcrições
   - Revisa texto com GPT-4 para melhorar coerência
   - Retorna texto via stdout
3. **Cleanup**: Remove arquivos temporários automaticamente

## 🎛️ Personalização

### Alterar duração dos chunks

Edite `youtube_transcribe.py`:

```python
MAX_CHUNK_DURATION = 5 * 60 * 1000  # 5 minutos em vez de 10
```

### Desabilitar revisão com GPT

Comente a seção de revisão em `youtube_transcribe.py`:

```python
# Review with GPT
# final_transcript = review_transcript(full_transcript, language or "auto")
final_transcript = full_transcript  # Use sem revisão
```

### Mudar modelo de revisão

Em `youtube_transcribe.py`, função `review_transcript()`:

```python
model="gpt-4o",  # Use GPT-4 em vez de gpt-4o-mini
```

### Configurar outro atalho

No `init.lua` ou seu `~/.hammerspoon/init.lua`:

```lua
-- Exemplo: Ctrl+Alt+Y
hs.hotkey.bind({"ctrl", "alt"}, "Y", function()
    ytTranscribe.transcribeYouTubeFromClipboard()
end)
```

## 🐛 Troubleshooting

### "Clipboard is empty!"
- Certifique-se de ter copiado um URL válido

### "No YouTube URL found in clipboard!"
- O script só aceita URLs do youtube.com ou youtu.be

### "OPENAI_API_KEY not configured"
- Verifique se o arquivo `.env` existe em `~/.hammerspoon/youtube-transcribe/.env`
- Certifique-se de que a chave está correta

### "Download failed"
- Verifique sua conexão com a internet
- Alguns vídeos podem ter restrições de download
- Verifique se `yt-dlp` está atualizado: `pip install -U yt-dlp`

### "ffmpeg not found"
- Instale via Homebrew: `brew install ffmpeg`

### Script não encontrado pelo Hammerspoon
- Verifique o caminho em `init.lua`
- Certifique-se de que os arquivos estão em `~/.hammerspoon/youtube-transcribe/`

### Notificação de erro genérico
- Abra o Console do Hammerspoon (menu bar icon → Console)
- Execute manualmente: `~/.hammerspoon/youtube-transcribe/venv/bin/python3 ~/.hammerspoon/youtube-transcribe/youtube_transcribe.py "URL_AQUI"`

## 💡 Dicas de Uso

- **Vídeos curtos** (< 10 min): Transcrição rápida, sem chunks
- **Vídeos médios** (10-30 min): Dividido em 2-3 chunks, processamento paralelo
- **Vídeos longos** (30+ min): Mais chunks, pode demorar alguns minutos
- **Podcasts**: Funciona perfeitamente para episódios completos
- **Idiomas**: Detecta automaticamente português, inglês, espanhol, etc.

## 💰 Custos

Usar a API OpenAI tem custos. Referência (preços podem mudar):

- **Whisper API**: ~$0.006 por minuto de áudio
- **GPT-4o-mini**: ~$0.0001-0.0003 por revisão

Exemplo: Vídeo de 1 hora = ~$0.36 + revisão

## 🔐 Segurança

- **Nunca** commite o arquivo `.env` com sua chave
- Mantenha `.env` apenas local
- O `.gitignore` já está configurado para proteger `.env`

## 🚀 Próximos Passos

Ideias para expandir o projeto:

- [ ] Suporte a outros sites de vídeo (Vimeo, etc.)
- [ ] Detecção de múltiplos idiomas no mesmo vídeo
- [ ] Formatação markdown automática (títulos, listas)
- [ ] Resumo automático do conteúdo
- [ ] Export para Notion/Obsidian
- [ ] Interface gráfica com Hammerspoon chooser

## 📝 Licença

Este projeto é um exemplo/template. Use e modifique como quiser.

## 🤝 Contribuindo

Sinta-se à vontade para fazer fork, modificar e adaptar para suas necessidades!

---

**Feito com ❤️ para a comunidade Hammerspoon**
