# Estrutura do Projeto

## 📁 Arquivos Principais

```
youtube-transcribe/
│
├── 🎯 CORE - Arquivos Essenciais
│   ├── init.lua                    # Módulo Hammerspoon (interface Lua)
│   ├── youtube_transcribe.py       # Script Python principal (lógica de transcrição)
│   ├── requirements.txt            # Dependências Python
│   └── .env                        # Configuração (API keys) - NÃO COMMITADO
│
├── 🔧 SETUP - Instalação e Configuração
│   ├── setup.sh                    # Script de instalação automatizada
│   ├── env.example                 # Template para .env
│   ├── diagnose.sh                 # Script de diagnóstico do sistema
│   └── test_local.sh               # Script para testes locais
│
├── 📚 DOCUMENTAÇÃO
│   ├── README.md                   # Guia principal de uso
│   ├── INSTALL.md                  # Instalação detalhada passo-a-passo
│   ├── INTEGRATION.md              # Exemplos de integração avançada
│   ├── API.md                      # Documentação técnica da API
│   ├── CHANGELOG.md                # Histórico de versões
│   ├── PROJECT_STRUCTURE.md        # Este arquivo
│   └── example_config.lua          # Exemplo de configuração completa
│
├── 🗑️ ARQUIVOS LEGADOS (da estrutura anterior)
│   ├── transcribe.py               # Script antigo (mantido para referência)
│   └── transcribe.sh               # Script shell antigo
│
└── 🔒 SEGURANÇA
    └── .gitignore                  # Arquivos ignorados pelo Git
```

## 📄 Descrição Detalhada

### CORE - Arquivos Essenciais

#### `init.lua`
- **Propósito**: Interface Lua para Hammerspoon
- **Função**: Orquestra o workflow (clipboard → Python → clipboard)
- **Integrável**: Pode ser carregado com `dofile()` ou `require()`
- **Exporta**: Módulo com função `transcribeYouTubeFromClipboard()`

#### `youtube_transcribe.py`
- **Propósito**: Lógica principal de transcrição
- **Responsabilidades**:
  - Download de áudio (yt-dlp)
  - Detecção de idioma (Whisper)
  - Divisão em chunks
  - Transcrição paralela
  - Revisão com GPT
- **I/O**: Recebe URL via CLI, retorna texto via stdout
- **Logs**: stderr para não poluir stdout

#### `requirements.txt`
- **Propósito**: Lista de dependências Python
- **Conteúdo**:
  - openai (Whisper + GPT)
  - yt-dlp (download)
  - pydub (processamento de áudio)
  - python-dotenv (variáveis de ambiente)

#### `.env`
- **Propósito**: Armazenar credenciais sensíveis
- **Conteúdo**: `OPENAI_API_KEY=sk-...`
- **Segurança**: NUNCA commitar! Incluído no .gitignore

---

### SETUP - Instalação e Configuração

#### `setup.sh`
- **Propósito**: Instalação automatizada de tudo
- **Ações**:
  1. Verifica Homebrew e ffmpeg
  2. Cria virtualenv Python
  3. Instala dependências
  4. Configura .env
  5. Copia arquivos para ~/.hammerspoon/
- **Uso**: `./setup.sh` (executar uma vez)

#### `env.example`
- **Propósito**: Template para configuração
- **Uso**: `cp env.example .env` e editar

#### `diagnose.sh`
- **Propósito**: Verificar se tudo está configurado corretamente
- **Saída**: Lista de checks com ✓, ⚠, ou ✗
- **Uso**: `./diagnose.sh` (quando tiver problemas)

#### `test_local.sh`
- **Propósito**: Testar script Python sem Hammerspoon
- **Uso**: `./test_local.sh "URL_YOUTUBE"`
- **Debug**: Útil para desenvolvimento e troubleshooting

---

### DOCUMENTAÇÃO

#### `README.md` ⭐
- **Propósito**: Documento principal - LEIA PRIMEIRO
- **Conteúdo**:
  - Visão geral do projeto
  - Instalação rápida
  - Como usar
  - Troubleshooting básico
- **Público**: Usuários iniciantes e intermediários

#### `INSTALL.md`
- **Propósito**: Guia detalhado de instalação
- **Conteúdo**:
  - Instalação automática
  - Instalação manual passo-a-passo
  - Verificação da instalação
  - Problemas comuns
- **Público**: Usuários que querem entender cada passo

#### `INTEGRATION.md`
- **Propósito**: Exemplos avançados de integração
- **Conteúdo**:
  - Diferentes cenários de uso
  - Menu bar, chooser, clipboard watcher
  - Integração com Alfred/Raycast
  - Customizações avançadas
- **Público**: Usuários avançados do Hammerspoon

#### `API.md`
- **Propósito**: Documentação técnica completa
- **Conteúdo**:
  - API do módulo Lua
  - Funções internas do Python
  - Fluxo de dados
  - Códigos de erro
  - Performance e custos
- **Público**: Desenvolvedores que querem modificar o código

#### `CHANGELOG.md`
- **Propósito**: Histórico de versões
- **Formato**: Keep a Changelog
- **Conteúdo**: Versão atual (1.0.0) e roadmap futuro

#### `example_config.lua`
- **Propósito**: Exemplo completo de configuração
- **Conteúdo**:
  - Setup básico
  - Menu bar integration
  - Histórico de transcrições
  - Atalhos úteis
- **Uso**: Copiar trechos para seu `~/.hammerspoon/init.lua`

---

### ARQUIVOS LEGADOS

#### `transcribe.py`
- **Status**: Mantido para referência
- **Nota**: Este era o script anterior, diferente do novo `youtube_transcribe.py`
- **Pode ser deletado**: Se não precisar

#### `transcribe.sh`
- **Status**: Script shell antigo
- **Pode ser deletado**: Se não precisar

---

## 🗂️ Estrutura de Instalação

Após executar `./setup.sh`, a estrutura será:

```
~/
├── .hammerspoon/
│   ├── init.lua                        # Seu arquivo de config (editar)
│   └── youtube-transcribe/             # Módulo instalado
│       ├── init.lua                    # (link ou cópia)
│       ├── youtube_transcribe.py       # (cópia)
│       ├── .env                        # (cópia)
│       ├── requirements.txt            # (cópia)
│       └── venv/                       # (link ou cópia)
│           └── bin/python3
│
└── <este-repo>/                        # Repositório original
    └── (todos os arquivos)
```

## 🔄 Workflow de Uso

```
1. Usuário copia URL → Clipboard
2. Pressiona Cmd+Shift+T → Hammerspoon
3. init.lua valida URL → Python script
4. youtube_transcribe.py:
   - Download (yt-dlp)
   - Divide em chunks (pydub)
   - Transcreve (Whisper API)
   - Revisa (GPT API)
5. Retorna texto → stdout
6. init.lua copia para → Clipboard
7. Notificação → Usuário
```

## 📦 Dependências

### Sistema
- macOS 10.15+
- Homebrew
- ffmpeg
- Python 3.8+

### Python (requirements.txt)
- openai >= 1.12.0
- yt-dlp >= 2024.3.10
- pydub >= 0.25.1
- python-dotenv >= 1.0.0

### Aplicativos
- Hammerspoon (https://www.hammerspoon.org/)

### API
- OpenAI API Key (Whisper + GPT access)

## 🚀 Quick Start

```bash
# 1. Clone e entre no diretório
cd youtube-transcribe

# 2. Execute setup
./setup.sh

# 3. Configure API key quando solicitado

# 4. Adicione ao ~/.hammerspoon/init.lua:
#    local yt = dofile(hs.configdir .. "/youtube-transcribe/init.lua")
#    hs.hotkey.bind({"cmd", "shift"}, "T", yt.transcribeYouTubeFromClipboard)

# 5. Reload Hammerspoon

# 6. Copie URL do YouTube e pressione Cmd+Shift+T
```

## 🧹 Arquivos Temporários

Durante a execução, o script cria arquivos temporários em `/tmp/youtube_transcribe_*/`:
- downloaded_audio.mp3
- chunk_000.mp3, chunk_001.mp3, etc.

Todos são automaticamente deletados ao final da execução (sucesso ou erro).

## 🔒 Segurança e Git

**NUNCA commitar:**
- `.env` (contém API key)
- `venv/` (ambiente virtual Python)
- `*.mp3`, `*.wav` (arquivos de áudio)
- `__pycache__/` (cache Python)

Todos já estão no `.gitignore`.

---

**Última atualização:** 2025-10-02
**Versão:** 1.0.0
