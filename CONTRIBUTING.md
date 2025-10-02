# 🤝 Contribuindo para YouTube Transcriber

Obrigado pelo interesse em contribuir! Este documento fornece diretrizes para contribuições.

## 🎯 Como Contribuir

### Reportar Bugs 🐛

Abra uma issue incluindo:
- Descrição clara do problema
- Passos para reproduzir
- Comportamento esperado vs. atual
- Versão do macOS, Python, Hammerspoon
- Output do `./diagnose.sh`

### Sugerir Melhorias 💡

Abra uma issue com:
- Descrição da funcionalidade
- Caso de uso
- Exemplo de como seria usado
- Benefícios para os usuários

### Fazer Pull Requests 🔧

1. **Fork o repositório**
2. **Crie uma branch**: `git checkout -b feature/minha-feature`
3. **Faça suas mudanças**
4. **Teste localmente**: `./diagnose.sh` e `./test_local.sh`
5. **Commit**: Use mensagens descritivas
6. **Push**: `git push origin feature/minha-feature`
7. **Abra um PR** descrevendo as mudanças

## 📝 Diretrizes de Código

### Python (youtube_transcribe.py)

```python
# Estilo: PEP 8
# Type hints quando possível
# Docstrings para funções públicas

def transcribe_chunk(chunk_path: str, language: Optional[str] = None) -> str:
    """
    Transcreve um único chunk de áudio.
    
    Args:
        chunk_path: Caminho do arquivo de áudio
        language: Código do idioma (opcional)
    
    Returns:
        Texto transcrito
    """
    pass
```

### Lua (init.lua)

```lua
-- Comentários claros
-- Funções locais quando possível
-- Naming: camelCase para funções

local function validateYouTubeUrl(url)
    -- Validação aqui
end
```

### Shell Scripts

```bash
#!/bin/bash
# Descrição do script
# Use set -e para exit on error
# Comentários para seções complexas

set -e

echo "Fazendo algo..."
```

## 🧪 Testando

### Antes de Submeter PR

```bash
# 1. Diagnóstico
./diagnose.sh

# 2. Teste com URL curta
./test_local.sh "URL_CURTA"

# 3. Teste com URL longa (se aplicável)
./test_local.sh "URL_LONGA"

# 4. Teste diferentes idiomas
./test_local.sh "URL_PORTUGUES"
./test_local.sh "URL_INGLES"
```

### Checklist de Teste

- [ ] Funciona com vídeos < 10 min
- [ ] Funciona com vídeos > 30 min
- [ ] Detecção de idioma funciona
- [ ] Notificações aparecem corretamente
- [ ] Erros são tratados gracefully
- [ ] Cleanup de arquivos temporários

## 📚 Documentação

Se adicionar funcionalidade nova:

1. **Atualize README.md** com exemplo de uso
2. **Documente em API.md** se for API pública
3. **Adicione exemplo em example_config.lua** se relevante
4. **Atualize CHANGELOG.md** com a mudança

## 🎨 Áreas para Contribuir

### 🟢 Beginner-Friendly

- Melhorar mensagens de erro
- Adicionar mais exemplos de configuração
- Traduzir documentação
- Corrigir typos
- Melhorar diagnóstico

### 🟡 Intermediário

- Adicionar suporte a outros sites de vídeo
- Implementar cache de transcrições
- Melhorar interface de notificações
- Adicionar mais formatos de output
- Implementar histórico de transcrições

### 🔴 Avançado

- Suporte a faster-whisper local
- Implementar timestamps
- Detecção de múltiplos speakers
- Batch processing de playlists
- Web interface

## 🌟 Ideias de Features

Vote ou implemente:

1. **Suporte a mais sites**
   - Vimeo
   - Dailymotion
   - Twitch VODs

2. **Melhor integração**
   - Alfred/Raycast workflows
   - Menu bar app
   - hs.chooser interface

3. **Output avançado**
   - Markdown formatado
   - JSON com timestamps
   - SRT/VTT para legendas

4. **Performance**
   - Cache de transcrições
   - Resumo progressivo
   - Preview de primeiros 30s

5. **Localização**
   - UI em múltiplos idiomas
   - Detecção automática de UI language

## 📋 Code Review

Ao revisar PRs, verificamos:

- ✅ Código limpo e legível
- ✅ Funcionalidade funciona conforme descrito
- ✅ Testes passam
- ✅ Documentação atualizada
- ✅ Sem quebras de compatibilidade (ou documentadas)
- ✅ Segurança (sem expor API keys, etc.)

## 🔐 Segurança

**Nunca commite:**
- API keys
- Tokens de acesso
- Dados pessoais
- Arquivos de áudio

Se encontrar vulnerabilidade de segurança, reporte privadamente.

## 📜 Licença

Ao contribuir, você concorda que suas contribuições serão licenciadas sob MIT License.

## 🎉 Reconhecimento

Contribuidores serão listados no README.md e CHANGELOG.md.

## 💬 Comunicação

- **Issues**: Para bugs e features
- **Discussions**: Para perguntas e ideias
- **PRs**: Para código

## 🚀 Começar a Contribuir

1. **Fork** o repositório
2. **Clone** seu fork
3. **Execute** `./setup.sh`
4. **Faça** suas mudanças
5. **Teste** tudo
6. **Submit** PR

---

**Obrigado por contribuir! 🙏**

Toda contribuição, grande ou pequena, é valiosa e apreciada.
