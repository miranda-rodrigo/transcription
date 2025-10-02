# 🚀 START HERE - YouTube Transcriber

```
██╗   ██╗ ██████╗ ██╗   ██╗████████╗██╗   ██╗██████╗ ███████╗
╚██╗ ██╔╝██╔═══██╗██║   ██║╚══██╔══╝██║   ██║██╔══██╗██╔════╝
 ╚████╔╝ ██║   ██║██║   ██║   ██║   ██║   ██║██████╔╝█████╗  
  ╚██╔╝  ██║   ██║██║   ██║   ██║   ██║   ██║██╔══██╗██╔══╝  
   ██║   ╚██████╔╝╚██████╔╝   ██║   ╚██████╔╝██████╔╝███████╗
   ╚═╝    ╚═════╝  ╚═════╝    ╚═╝    ╚═════╝ ╚═════╝ ╚══════╝
                                                               
████████╗██████╗  █████╗ ███╗   ██╗███████╗ ██████╗██████╗  
╚══██╔══╝██╔══██╗██╔══██╗████╗  ██║██╔════╝██╔════╝██╔══██╗
   ██║   ██████╔╝███████║██╔██╗ ██║███████╗██║     ██████╔╝
   ██║   ██╔══██╗██╔══██║██║╚██╗██║╚════██║██║     ██╔══██╗
   ██║   ██║  ██║██║  ██║██║ ╚████║███████║╚██████╗██║  ██║
   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝╚══════╝ ╚═════╝╚═╝  ╚═╝
```

## 🎯 O Que É Isso?

**Transcrição automática de vídeos do YouTube direto do clipboard!**

```
📋 Copie URL → ⌨️  Cmd+Shift+T → 📝 Cole transcrição
```

## ⚡ Quick Start (5 minutos)

### 1️⃣ Instale

```bash
./setup.sh
```

### 2️⃣ Configure

Adicione ao `~/.hammerspoon/init.lua`:

```lua
local yt = dofile(hs.configdir .. "/youtube-transcribe/init.lua")
hs.hotkey.bind({"cmd", "shift"}, "T", yt.transcribeYouTubeFromClipboard)
```

### 3️⃣ Use

1. Copie: `https://www.youtube.com/watch?v=dQw4w9WgXcQ`
2. Pressione: `Cmd+Shift+T`
3. Aguarde: Notificação
4. Cole: Transcrição completa! ✨

---

## 📚 Documentação

| Arquivo | Descrição | Tempo |
|---------|-----------|-------|
| **[QUICKSTART.md](QUICKSTART.md)** ⚡ | Instalação em 5 minutos | 5 min |
| **[README.md](README.md)** 📘 | Documentação completa | 15 min |
| **[INSTALL.md](INSTALL.md)** 🔧 | Guia detalhado | 20 min |
| **[INTEGRATION.md](INTEGRATION.md)** 🎨 | Customizações | 30 min |
| **[API.md](API.md)** 💻 | Docs técnicas | 30 min |
| **[INDEX.md](INDEX.md)** 🗺️ | Navegação completa | - |

---

## ✨ Features

- 🎥 **YouTube → Texto** em minutos
- 🌍 **Auto-detecção de idioma**
- ⚡ **Transcrição paralela** (chunks)
- 🤖 **Revisão com GPT** para coerência
- 📋 **100% clipboard** (sem arquivos salvos)
- 🔔 **Notificações** em cada etapa
- 🧹 **Cleanup automático**
- 🔒 **API keys protegidas**

---

## 🛠️ Tecnologias

- 🔨 **Hammerspoon** (macOS automation)
- 🐍 **Python 3.8+** (lógica principal)
- 🎙️ **OpenAI Whisper** (transcrição)
- 🤖 **GPT-4o-mini** (revisão)
- 📦 **yt-dlp** (download)
- 🎵 **ffmpeg** (processamento)

---

## 💰 Custos

| Duração | Custo |
|---------|-------|
| 10 min  | ~$0.06 |
| 30 min  | ~$0.18 |
| 1 hora  | ~$0.36 |

---

## 🎓 Quem Usa?

✅ **Estudantes** - Transcrever aulas  
✅ **Criadores** - Transcrever podcasts  
✅ **Pesquisadores** - Documentar entrevistas  
✅ **Profissionais** - Atas de reunião  
✅ **Desenvolvedores** - Talks e tutoriais  

---

## 🤔 FAQ Rápido

**P: Funciona offline?**  
R: Não, precisa de internet (API OpenAI)

**P: Quanto custa?**  
R: ~$0.006 por minuto de vídeo

**P: Que idiomas?**  
R: Todos que o Whisper suporta (100+)

**P: Vídeos privados?**  
R: Só vídeos públicos do YouTube

**P: Quanto tempo demora?**  
R: 30-60 segundos para vídeo de 10 min

---

## 🚦 Status do Projeto

```
✅ Core implementado
✅ Documentação completa (80 KB)
✅ Setup automatizado
✅ Testes funcionais
✅ Production-ready
```

**Versão:** 1.0.0  
**Licença:** MIT  
**Status:** 🟢 Stable

---

## 🗺️ Navegação Rápida

```
├─ 🚀 Começar          → QUICKSTART.md
├─ 📖 Usar             → README.md
├─ 🔧 Instalar         → INSTALL.md
├─ 🎨 Customizar       → INTEGRATION.md
├─ 💻 Desenvolver      → API.md
└─ 🗺️ Navegar          → INDEX.md
```

---

## 🎁 Bonus: Scripts Úteis

```bash
./setup.sh         # Instala tudo
./diagnose.sh      # Verifica problemas
./test_local.sh    # Testa sem Hammerspoon
```

---

## 🤝 Contribuir

Veja [CONTRIBUTING.md](CONTRIBUTING.md)

---

## 📊 Stats

- 📁 **23 arquivos** criados
- 💻 **3.400+ linhas** de código
- 📚 **80 KB** de documentação
- ⭐ **10 arquivos** de docs
- 🚀 **5 minutos** para começar

---

## 🎉 Pronto?

```bash
cat QUICKSTART.md
```

ou

```bash
./setup.sh
```

---

**Feito com ❤️ para a comunidade Hammerspoon**

