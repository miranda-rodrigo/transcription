# Guia de Instalação Detalhado

## 🎯 Instalação Automática (Recomendada)

```bash
cd /caminho/para/youtube-transcribe
./setup.sh
```

Siga as instruções na tela.

## 🔧 Instalação Manual Passo-a-Passo

### 1. Pré-requisitos

#### Instalar Homebrew (se não tiver)
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

#### Instalar Hammerspoon
Baixe em: https://www.hammerspoon.org/
Ou via Homebrew:
```bash
brew install --cask hammerspoon
```

Abra o Hammerspoon e dê as permissões necessárias em Preferências do Sistema.

### 2. Instalar Dependências do Sistema

```bash
# ffmpeg para processamento de áudio
brew install ffmpeg

# Python 3 (geralmente já vem no macOS)
brew install python3
```

### 3. Configurar o Projeto

#### Clone ou baixe o repositório
```bash
git clone <repository_url>
cd youtube-transcribe
```

#### Criar ambiente virtual Python
```bash
python3 -m venv venv
source venv/bin/activate
```

#### Instalar dependências Python
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### Configurar chave da API
```bash
cp env.example .env
nano .env  # ou use seu editor preferido
```

Adicione sua chave OpenAI:
```
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### 4. Integrar com Hammerspoon

#### Opção A: Copiar para diretório do Hammerspoon
```bash
mkdir -p ~/.hammerspoon/youtube-transcribe
cp youtube_transcribe.py ~/.hammerspoon/youtube-transcribe/
cp init.lua ~/.hammerspoon/youtube-transcribe/
cp .env ~/.hammerspoon/youtube-transcribe/
cp -r venv ~/.hammerspoon/youtube-transcribe/
```

#### Opção B: Usar symlink (mais fácil para desenvolvimento)
```bash
ln -s "$(pwd)" ~/.hammerspoon/youtube-transcribe
```

### 5. Configurar Hammerspoon

Edite `~/.hammerspoon/init.lua`:

```lua
-- No topo do arquivo
local ytTranscribe = dofile(hs.configdir .. "/youtube-transcribe/init.lua")

-- Adicionar atalho (exemplo: Cmd+Shift+T)
hs.hotkey.bind({"cmd", "shift"}, "T", function()
    ytTranscribe.transcribeYouTubeFromClipboard()
end)
```

### 6. Recarregar Hammerspoon

- Clique no ícone do Hammerspoon na barra de menu
- Selecione "Reload Config"
- Ou pressione o atalho configurado (geralmente Cmd+Alt+R)

### 7. Testar

1. Copie um URL do YouTube curto para teste:
   ```
   https://www.youtube.com/watch?v=jNQXAC9IVRw
   ```

2. Pressione `Cmd+Shift+T` (ou seu atalho configurado)

3. Aguarde a notificação de conclusão

4. Cole em qualquer editor de texto para ver a transcrição

## 🧪 Teste sem Hammerspoon

Para testar o script Python diretamente:

```bash
# Ativar ambiente virtual
source venv/bin/activate

# Executar diretamente
python3 youtube_transcribe.py "https://www.youtube.com/watch?v=jNQXAC9IVRw"

# Ou usar o script de teste
./test_local.sh "https://www.youtube.com/watch?v=jNQXAC9IVRw"
```

## 📝 Verificar Instalação

Execute este checklist:

```bash
# ✅ Verificar ffmpeg
ffmpeg -version

# ✅ Verificar Python
python3 --version

# ✅ Verificar pip packages
source venv/bin/activate
pip list | grep -E "openai|yt-dlp|pydub|python-dotenv"

# ✅ Verificar arquivo .env
cat .env | grep OPENAI_API_KEY

# ✅ Verificar estrutura do Hammerspoon
ls -la ~/.hammerspoon/youtube-transcribe/
```

Todos devem retornar resultados válidos.

## 🆘 Problemas Comuns

### "Command not found: ffmpeg"
```bash
brew install ffmpeg
```

### "No module named 'openai'"
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### "Permission denied" ao executar scripts
```bash
chmod +x setup.sh test_local.sh
```

### Hammerspoon não encontra o módulo
Verifique o caminho em `~/.hammerspoon/init.lua`:
```lua
-- Deve apontar para onde você instalou
local ytTranscribe = dofile(hs.configdir .. "/youtube-transcribe/init.lua")
```

### API key inválida
- Verifique em: https://platform.openai.com/api-keys
- Certifique-se de que tem créditos na conta
- Confirme que a chave tem acesso ao Whisper API

## 🔄 Atualizar o Projeto

```bash
cd youtube-transcribe
git pull origin main
source venv/bin/activate
pip install -r requirements.txt --upgrade
# Recopiar arquivos para Hammerspoon se necessário
cp youtube_transcribe.py ~/.hammerspoon/youtube-transcribe/
```

## 🗑️ Desinstalar

```bash
# Remover do Hammerspoon
rm -rf ~/.hammerspoon/youtube-transcribe

# Remover binding do init.lua (editar manualmente)
nano ~/.hammerspoon/init.lua

# Remover projeto local
cd ..
rm -rf youtube-transcribe
```

---

**Precisa de ajuda?** Abra uma issue ou consulte o README.md para mais informações.
