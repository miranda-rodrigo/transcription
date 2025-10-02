# ⚡ Quick Start - 5 Minutos

Comece a usar o YouTube Transcriber em 5 minutos.

## 🎯 O Que Você Vai Fazer

Configurar um atalho no macOS que:
1. Lê URL do YouTube da área de transferência
2. Baixa e transcreve o áudio automaticamente
3. Copia a transcrição de volta para a área de transferência

## 📋 Pré-requisitos Rápidos

- [ ] macOS (10.15+)
- [ ] Chave da API OpenAI ([obter aqui](https://platform.openai.com/api-keys))
- [ ] 10 minutos de tempo

## 🚀 Instalação em 3 Passos

### Passo 1: Execute o Setup (2 min)

```bash
# Clone ou baixe este repositório
cd /caminho/para/youtube-transcribe

# Execute o script de setup
./setup.sh
```

O script irá:
- ✅ Instalar ffmpeg (se necessário)
- ✅ Criar ambiente Python
- ✅ Instalar bibliotecas
- ✅ Pedir sua API key da OpenAI

**⚠️ Quando pedir a API key, cole ela com cuidado!**

---

### Passo 2: Configure o Hammerspoon (2 min)

#### 2.1. Instale o Hammerspoon

Se ainda não tem:

```bash
# Via Homebrew
brew install --cask hammerspoon

# Ou baixe: https://www.hammerspoon.org/
```

#### 2.2. Abra o Hammerspoon uma vez

- Abra Hammerspoon.app
- Conceda permissões quando solicitado
- Aparecerá um ícone na barra de menu

#### 2.3. Edite a configuração

```bash
# Abra o arquivo de configuração
open -e ~/.hammerspoon/init.lua
```

**Cole estas 5 linhas no final do arquivo:**

```lua
-- YouTube Transcriber
local yt = dofile(hs.configdir .. "/youtube-transcribe/init.lua")
hs.hotkey.bind({"cmd", "shift"}, "T", function()
    yt.transcribeYouTubeFromClipboard()
end)
```

**Salve o arquivo** (Cmd+S)

---

### Passo 3: Reload e Teste (1 min)

#### 3.1. Reload Hammerspoon

No menu bar do Hammerspoon:
- Clique no ícone 🔨
- Selecione "Reload Config"
- Deve aparecer notificação de sucesso

#### 3.2. Teste!

1. **Copie este URL de teste:**
   ```
   https://www.youtube.com/watch?v=jNQXAC9IVRw
   ```

2. **Pressione:** `Cmd + Shift + T`

3. **Aguarde:** Notificação "Starting transcription..."

4. **Após 30-60 segundos:** Notificação "✅ Transcription completed!"

5. **Cole em qualquer lugar** para ver a transcrição

---

## ✅ Pronto! Você Configurou

Agora você pode:

1. Copiar qualquer URL do YouTube
2. Pressionar `Cmd+Shift+T`
3. Aguardar a transcrição
4. Colar o resultado

---

## 🎨 Personalize (Opcional)

### Mudar o Atalho

Não gosta de `Cmd+Shift+T`? Mude no `init.lua`:

```lua
-- Exemplo: Ctrl+Alt+Y
hs.hotkey.bind({"ctrl", "alt"}, "Y", function()
    yt.transcribeYouTubeFromClipboard()
end)
```

**Teclas disponíveis:**
- Modificadores: `cmd`, `shift`, `alt` (ou `option`), `ctrl`
- Letras: `"A"` até `"Z"`
- Números: `"1"` até `"0"`
- Especiais: `"space"`, `"return"`, `"escape"`, etc.

---

## 🐛 Problemas?

### "Clipboard is empty!"
→ Certifique-se de ter copiado a URL primeiro (Cmd+C)

### "No YouTube URL found"
→ Só funciona com youtube.com ou youtu.be

### "Error: OPENAI_API_KEY not configured"
→ Execute novamente: `./setup.sh` e configure a API key

### Nada acontece quando pressiono o atalho
→ Abra o Console do Hammerspoon (ícone na barra → Console) e veja os erros

### Quer testar sem o Hammerspoon?
```bash
./test_local.sh "https://www.youtube.com/watch?v=jNQXAC9IVRw"
```

---

## 📊 Custos de Uso

Cada transcrição custa aproximadamente:

| Duração do Vídeo | Custo (USD) |
|------------------|-------------|
| 5 minutos        | ~$0.03      |
| 15 minutos       | ~$0.09      |
| 30 minutos       | ~$0.18      |
| 1 hora           | ~$0.36      |

*Baseado nos preços atuais da OpenAI (Whisper: $0.006/min)*

---

## 💡 Dicas de Uso

✅ **Funciona bem com:**
- Vídeos de palestras e apresentações
- Podcasts no YouTube
- Aulas e tutoriais
- Entrevistas

⚠️ **Menos efetivo com:**
- Vídeos com muito ruído de fundo
- Música sem fala
- Múltiplos idiomas no mesmo vídeo

---

## 📚 Próximos Passos

Quer aprender mais?

- [README.md](README.md) - Documentação completa
- [INTEGRATION.md](INTEGRATION.md) - Integrações avançadas
- [example_config.lua](example_config.lua) - Mais exemplos de configuração

---

## 🎉 Aproveite!

Você agora tem um transcriber de YouTube profissional integrado ao seu macOS.

**Compartilhe com amigos que também vão achar útil!**

---

**Tempo total gasto:** ~5 minutos
**Tempo economizado:** Incontável! 🚀
