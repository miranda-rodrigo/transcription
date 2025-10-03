# Configuração Rápida - macOS Shortcuts

## Método 1: Shell Script (Mais Simples - Recomendado)

### Opção A: Workflow com Clipboard (Mais comum)

1. **Abra o app "Shortcuts"** no macOS
2. **Clique no "+" para criar um novo shortcut**
3. **Adicione a ação "Run Shell Script":**
   - Busque por "shell" e arraste "Run Shell Script"
   - Configure os campos:
     - **Shell:** `/bin/bash` (ou deixe `zsh` - padrão)
     - **Input:** "Clipboard" 
     - **Pass Input:** "as arguments"
     - **Run as Administrator:** deixe desativado

4. **Cole este script:**
```bash
cd "/Users/rodrigomiranda/useful-repos/audio_transcription"
if [ $# -gt 0 ] && [ -n "$1" ]; then
  # Se tem argumentos (URL do clipboard), usa como input
  ./bin/transcribe-shortcut "$1"
else
  # Senão usa workflow clipboard padrão
  ./bin/transcribe-shortcut --from-clipboard --to-clipboard
fi
```

### Opção B: Workflow Flexível (Aceita Input de outras ações)

1. **Configure os campos:**
   - **Shell:** `/bin/bash`
   - **Input:** "Input" (para receber de outras ações)
   - **Pass Input:** "as arguments"

2. **Cole este script:**
```bash
cd "/Users/rodrigomiranda/useful-repos/audio_transcription"
if [ $# -gt 0 ]; then
  ./bin/transcribe-shortcut "$1"
else
  ./bin/transcribe-shortcut --from-clipboard --to-clipboard
fi
```

### Opção C: Workflow apenas com Clipboard (Mais direto)

1. **Configure os campos:**
   - **Shell:** `/bin/bash`
   - **Input:** "Clipboard" 
   - **Pass Input:** "to stdin"

2. **Cole este script:**
```bash
cd "/Users/rodrigomiranda/useful-repos/audio_transcription"
# Lê URL do stdin (clipboard)
read url
if [ -n "$url" ]; then
  ./bin/transcribe-shortcut "$url"
else
  ./bin/transcribe-shortcut --from-clipboard --to-clipboard
fi
```

## Método 2: AppleScript (Alternativa)

1. **Abra o app "Shortcuts"** no macOS
2. **Clique no "+" para criar um novo shortcut**
3. **Adicione a ação "Run AppleScript":**
   - Busque por "applescript" e arraste "Run AppleScript"
   - **NÃO use "Run AppleScript with Input"** - isso causa problemas

4. **Cole este script:**
```applescript
on run input
	set repoPath to "/Users/rodrigomiranda/useful-repos/audio_transcription"
	
	try
		-- Handle input from Shortcuts app or direct execution
		if input is not missing value and (count of input) > 0 then
			set inputText to item 1 of input as text
			set shellCmd to quoted form of (repoPath & "/bin/transcribe-shortcut") & " " & quoted form of inputText
		else
			set shellCmd to quoted form of (repoPath & "/bin/transcribe-shortcut") & " --from-clipboard --to-clipboard"
		end if
		
		set result to do shell script shellCmd
		display notification "Transcrição concluída!" with title "Audio Transcription"
		return result
		
	on error errMsg
		display notification errMsg with title "Erro na Transcrição"
		return "Erro: " & errMsg
	end try
end run
```

## Configuração Final

5. **Configure o shortcut:**
   - **Nome:** "Transcrever Áudio"
   - **Ícone:** Escolha um ícone de microfone ou texto 🎤
   - **Ativar "Use with Siri"** (opcional)
   - **Ativar "Add to Menu Bar"** (opcional)

6. **Salve o shortcut**

## Como Usar

### Via Siri
- "Hey Siri, transcrever áudio" (certifique-se de ter uma URL no clipboard)

### Via Menu Bar
- Clique no ícone Shortcuts na barra de menu → "Transcrever Áudio"

### Via Atalho de Teclado
1. **System Settings > Keyboard > Keyboard Shortcuts > Services**
2. Encontre "Transcrever Áudio" 
3. Adicione um atalho (ex: ⌘⌥T)

### Via Share Sheet
- Em Safari, YouTube, ou outros apps
- Use o botão "Share" → "Transcrever Áudio"

## Variações Avançadas

### Para Arquivos Locais
Configure uma ação adicional "Get Selected Finder Items" antes do "Run Shell Script".

### Para URLs Específicas
Configure Input como "Input" e conecte com ação "Get URLs from Input".

### Para Data Atual no Nome
Use Input "Current Date" e modifique o script para incluir timestamp.

## Exemplo de Uso Completo

1. **Copie uma URL do YouTube** (⌘C)
2. **Execute o shortcut:**
   - "Hey Siri, transcrever áudio"
   - OU ⌘⌥T (se configurou atalho)
   - OU Menu Bar → Transcrever Áudio
3. **Aguarde o processamento** 
4. **Transcrição no clipboard** - cole com ⌘V

## Testando

Para verificar se funciona:
1. Copie: `https://www.youtube.com/watch?v=dQw4w9WgXcQ`
2. Execute seu shortcut
3. Cole resultado em editor de texto

## Troubleshooting

### "Permission denied"
```bash
cd /Users/rodrigomiranda/useful-repos/audio_transcription
chmod +x bin/transcribe-shortcut shortcuts/simple_shortcut.sh
```

### "Script not found"
Verifique se o caminho `/Users/rodrigomiranda/useful-repos/audio_transcription` está correto.

### "Dependencies missing"
```bash
cd /Users/rodrigomiranda/useful-repos/audio_transcription
make setup
brew install ffmpeg yt-dlp
```

### Shortcut não aparece no Siri
Certifique-se de ativar "Use with Siri" nas configurações do shortcut.

## Opções dos Campos Run Shell Script

### Shell
- **zsh** (padrão macOS) - recomendado
- **/bin/bash** - mais compatível
- **/bin/sh** - mais básico

### Input
- **Clipboard** - pega conteúdo copiado
- **Input** - recebe de ações anteriores
- **Current App** - info do app ativo
- **Current Date** - data atual
- **Device Details** - info do dispositivo

### Pass Input
- **as arguments** - passa como `$1, $2, $3...` (recomendado)
- **to stdin** - passa via `read` ou pipe

### Run as Administrator
- Deixe **desativado** (não precisa de sudo)