# Integração com macOS Shortcuts

Este diretório contém a integração do nosso sistema de transcrição com o app **Shortcuts** do macOS.

## Arquivos

- `Audio_Transcription.applescript` - Script AppleScript para integração
- `README.md` - Este arquivo com instruções

## Como configurar o Shortcut no macOS

### Método 1: Usando o AppleScript (Recomendado)

1. **Abra o app Shortcuts** no macOS
2. **Clique em "+" para criar um novo shortcut**
3. **Adicione a ação "Run AppleScript":**
   - Na barra de busca, digite "AppleScript"
   - Arraste "Run AppleScript" para o workflow
4. **Cole o conteúdo do arquivo `Audio_Transcription.applescript`**:
   - Abra o arquivo no Finder ou editor de texto
   - Copie todo o conteúdo
   - Cole na caixa do AppleScript
5. **Configure o shortcut:**
   - Nome: "Transcrever Áudio"
   - Ícone: Escolha um ícone relacionado a áudio/texto
   - Cor: Escolha uma cor de sua preferência

### Método 2: Shell Script Direto

1. **Abra o app Shortcuts** no macOS
2. **Clique em "+" para criar um novo shortcut**
3. **Adicione ação "Get Clipboard"** (se quiser usar clipboard)
4. **Adicione ação "Run Shell Script":**
   - Input: "Text" como "to stdin"
   - Shell: `/bin/bash`
   - Script:
   ```bash
   cd "/Users/rodrigomiranda/useful-repos/audio_transcription"
   ./bin/transcribe-shortcut --from-clipboard --to-clipboard
   ```

## Configurações Detalhadas dos Campos

### Campos da Ação "Run Shell Script"

**Shell** → Define qual shell usar:
- `zsh` (padrão macOS) - recomendado para compatibilidade
- `/bin/bash` - mais universal
- `/bin/sh` - mais básico

**Input** → De onde o script recebe dados:
- `Clipboard` → pega conteúdo da área de transferência
- `Input` → usa entrada de ações anteriores no shortcut
- `Current App` → informações do app ativo
- `Current Date` → insere a data atual
- `Device Details` → informações do dispositivo

**Pass Input** → Como entregar o input ao script:
- `as arguments` → input vira `$1, $2, $3...` (recomendado)
- `to stdin` → input enviado via fluxo padrão (lido com `read`)

**Run as Administrator** → Execução com privilégios:
- Deixe **desativado** (nosso script não precisa de sudo)

### Configurações Avançadas

**Atalho de Teclado:**
1. **System Settings > Keyboard > Keyboard Shortcuts > Services**
2. Encontre seu shortcut e defina combinação (ex: ⌘⌥T)

**Siri e Menu Bar:**
1. No Shortcuts, selecione seu shortcut
2. Ative "Use with Siri" e/ou "Add to Menu Bar"

### Variações do Shortcut

Você pode criar diferentes versões para diferentes necessidades:

#### 1. Transcrição via Clipboard
```applescript
do shell script quoted form of "/Users/rodrigomiranda/useful-repos/audio_transcription/bin/transcribe-shortcut" & " --from-clipboard --to-clipboard"
```

#### 2. Transcrição de Arquivo Selecionado
- Adicione ação "Get Selected Finder Items"
- Use o AppleScript modificado para processar o arquivo

#### 3. Transcrição de URL
- Adicione ação "Get Clipboard" 
- Processe como URL se for válida

## Uso

### Via Siri
- "Hey Siri, Transcrever Áudio"

### Via Atalho de Teclado
- Pressione a combinação definida (ex: ⌘⌥T)

### Via Menu Bar
- Clique no ícone do Shortcuts na menu bar
- Selecione "Transcrever Áudio"

### Via Share Sheet
- Em qualquer app com share sheet
- Selecione "Transcrever Áudio"

## Funcionalidades Suportadas

- ✅ Transcrição via clipboard (texto copiado → URL do YouTube)
- ✅ Arquivos locais de áudio/vídeo
- ✅ URLs do YouTube e outras plataformas
- ✅ Review automático com IA (se OPENAI_API_KEY configurada)
- ✅ Detecção automática de idioma
- ✅ Processamento paralelo para arquivos longos

## Troubleshooting

### Erro de Permissão
Se aparecer erro de permissão:
```bash
chmod +x /Users/rodrigomiranda/useful-repos/audio_transcription/bin/transcribe-shortcut
```

### Dependências
Certifique-se que tem instalado:
```bash
brew install ffmpeg yt-dlp
pip install -r requirements.txt
```

### Paths
Se o shortcut não encontrar os scripts, ajuste o caminho no AppleScript:
- Mude `/Users/rodrigomiranda/useful-repos/audio_transcription` para o caminho correto do seu repositório

## Exemplos de Fluxos

### Fluxo 1: YouTube → Transcrição
1. Copie URL do YouTube
2. Execute shortcut (Siri/atalho/menu)
3. Transcrição aparece no clipboard
4. Cole onde precisar

### Fluxo 2: Arquivo Local → Transcrição  
1. Configure shortcut para aceitar arquivos
2. Selecione arquivo no Finder
3. Execute via share sheet
4. Transcrição salva/copiada

### Fluxo 3: Áudio Gravado → Transcrição
1. Grave áudio com QuickTime/Gravador
2. Use shortcut para transcrever o arquivo
3. Review automático se configurado
4. Resultado no clipboard
