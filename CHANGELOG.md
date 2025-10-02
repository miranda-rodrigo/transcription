# Changelog

Todas as mudanças notáveis deste projeto serão documentadas neste arquivo.

## [1.0.0] - 2025-10-02

### ✨ Adicionado
- Módulo Hammerspoon para transcrição de áudio do YouTube
- Script Python com suporte a download via yt-dlp
- Detecção automática de idioma via Whisper API
- Divisão inteligente de áudio em chunks para arquivos grandes
- Transcrição paralela de múltiplos chunks
- Revisão de texto com GPT-4o-mini para melhor coerência
- Workflow completo clipboard → clipboard (sem salvar arquivos)
- Script de setup automatizado (`setup.sh`)
- Documentação completa:
  - README.md com guia de uso
  - INSTALL.md com instalação detalhada
  - INTEGRATION.md com exemplos de integração
- Suporte para macOS com Homebrew
- Tratamento básico de erros e notificações
- Limpeza automática de arquivos temporários

### 🔧 Técnico
- Integração Lua (Hammerspoon) + Python
- Uso de ambiente virtual Python
- Variáveis de ambiente via `.env`
- `.gitignore` configurado para segurança
- Dependências claras em `requirements.txt`
- Script de teste local (`test_local.sh`)

### 📋 Dependências
- Hammerspoon (macOS)
- Python 3.8+
- ffmpeg
- OpenAI API (Whisper + GPT)
- Pacotes Python: openai, yt-dlp, pydub, python-dotenv

---

## Roadmap Futuro

### [1.1.0] - Planejado
- [ ] Suporte a outros sites de vídeo (Vimeo, Dailymotion)
- [ ] Opção para salvar transcrições localmente
- [ ] Formato de saída configurável (plain text, markdown, JSON)
- [ ] Cache de transcrições para evitar re-processar

### [1.2.0] - Ideias
- [ ] Interface gráfica com hs.chooser
- [ ] Resumo automático com GPT
- [ ] Detecção de múltiplos speakers
- [ ] Export para Notion/Obsidian
- [ ] Timestamped transcription
- [ ] Suporte a playlists

### [2.0.0] - Longo Prazo
- [ ] Usar faster-whisper local (sem API)
- [ ] Suporte a outros modelos de transcrição
- [ ] Web interface opcional
- [ ] Batch processing de múltiplos URLs

---

**Formato baseado em [Keep a Changelog](https://keepachangelog.com/)**
