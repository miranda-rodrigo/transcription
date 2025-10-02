# Guia de Integração com Hammerspoon

Este documento explica como integrar este módulo ao seu setup existente do Hammerspoon.

## 🎯 Cenários de Integração

### 1. Setup Básico - Atalho Único

Para usuários que querem apenas o atalho de transcrição:

```lua
-- ~/.hammerspoon/init.lua

-- YouTube Transcription
local ytTranscribe = dofile(hs.configdir .. "/youtube-transcribe/init.lua")

-- Cmd+Shift+T para transcrever
hs.hotkey.bind({"cmd", "shift"}, "T", function()
    ytTranscribe.transcribeYouTubeFromClipboard()
end)
```

### 2. Integração em Configuração Modular

Se você já tem uma estrutura modular:

```lua
-- ~/.hammerspoon/init.lua

-- Carregar módulos
local modules = {
    youtube = require("youtube-transcribe.init"),
    -- seus outros módulos...
}

-- Configurar atalhos
hs.hotkey.bind({"cmd", "shift"}, "T", modules.youtube.transcribeYouTubeFromClipboard)
```

### 3. Menu Personalizado com Chooser

Adicionar ao menu/chooser do Hammerspoon:

```lua
local ytTranscribe = dofile(hs.configdir .. "/youtube-transcribe/init.lua")

-- Criar menu de ações
local function showActionsMenu()
    local choices = {
        {
            text = "📝 Transcribe YouTube from Clipboard",
            subText = "Download and transcribe YouTube audio",
            action = ytTranscribe.transcribeYouTubeFromClipboard
        },
        -- outras ações...
    }
    
    local chooser = hs.chooser.new(function(choice)
        if choice then choice.action() end
    end)
    
    chooser:choices(choices)
    chooser:show()
end

hs.hotkey.bind({"cmd", "shift"}, "A", showActionsMenu)
```

### 4. Integração com Menu Bar

Adicionar item ao menu bar:

```lua
local ytTranscribe = dofile(hs.configdir .. "/youtube-transcribe/init.lua")

-- Criar menu bar item
local menubar = hs.menubar.new()
menubar:setTitle("🎬")
menubar:setMenu({
    {
        title = "Transcribe YouTube URL",
        fn = ytTranscribe.transcribeYouTubeFromClipboard
    },
    {
        title = "-"  -- separator
    },
    {
        title = "Reload Config",
        fn = function() hs.reload() end
    }
})
```

### 5. Detecção Automática de URLs

Transcrever automaticamente quando copiar URL do YouTube:

```lua
local ytTranscribe = dofile(hs.configdir .. "/youtube-transcribe/init.lua")

-- Watcher para clipboard
local lastClipboard = ""
local clipboardWatcher = hs.timer.new(2, function()
    local currentClipboard = hs.pasteboard.getContents()
    if currentClipboard and currentClipboard ~= lastClipboard then
        lastClipboard = currentClipboard
        
        -- Verificar se é URL do YouTube
        if string.match(currentClipboard, "youtube%.com") or 
           string.match(currentClipboard, "youtu%.be") then
            
            -- Mostrar alerta
            local button = hs.dialog.blockAlert(
                "YouTube URL Detected",
                "Transcribe this video?\n" .. currentClipboard,
                "Transcribe",
                "Cancel"
            )
            
            if button == "Transcribe" then
                ytTranscribe.transcribeYouTubeFromClipboard()
            end
        end
    end
end)

-- Iniciar watcher (OPCIONAL - pode ser intrusivo)
-- clipboardWatcher:start()

-- Atalho para toggle do watcher
hs.hotkey.bind({"cmd", "shift", "ctrl"}, "W", function()
    if clipboardWatcher:running() then
        clipboardWatcher:stop()
        hs.notify.new({title="Clipboard Watcher", informativeText="Stopped"}):send()
    else
        clipboardWatcher:start()
        hs.notify.new({title="Clipboard Watcher", informativeText="Started"}):send()
    end
end)
```

### 6. Integração com Alfred/Raycast

Se usar Alfred ou Raycast, você pode criar um workflow que chama o Hammerspoon:

```bash
#!/bin/bash
# Alfred Script Filter

YOUTUBE_URL="{query}"

osascript -e "
tell application \"Hammerspoon\"
    execute lua code \"dofile(hs.configdir .. '/youtube-transcribe/init.lua').transcribeYouTubeFromClipboard()\"
end tell
"
```

## 🎨 Customizações Avançadas

### Notificações Personalizadas

Editar `init.lua` para customizar notificações:

```lua
local function notify(title, message, type)
    local notification = hs.notify.new({
        title = title,
        informativeText = message,
        withdrawAfter = type == "error" and 10 or 5,
        hasActionButton = false,
        -- Adicionar som
        soundName = type == "error" and "Basso" or "Glass",
        -- Adicionar imagem (opcional)
        -- contentImage = hs.image.imageFromPath("/path/to/icon.png")
    })
    
    -- Clicar na notificação para ver logs
    if type == "error" then
        notification:setIdImage(hs.image.imageFromName("NSCaution"))
        notification:hasActionButton(true)
        notification:actionButtonTitle("View Logs")
        notification:actions({{
            title = "View Logs",
            fn = function()
                hs.openConsole()
            end
        }})
    end
    
    notification:send()
end
```

### Callback de Progresso

Modificar para adicionar updates de progresso:

```lua
-- Em init.lua, adicionar callback
function module.transcribeWithProgress(callback)
    local clipboardContent = hs.pasteboard.getContents()
    
    -- Validações...
    
    callback("downloading")
    
    -- Modificar o task para emitir progresso
    local task = hs.task.new("/bin/bash", function(exitCode, stdOut, stdErr)
        if exitCode == 0 then
            callback("completed", stdOut)
        else
            callback("error", stdErr)
        end
    end, {"-c", command})
    
    task:start()
end

-- Usar assim:
hs.hotkey.bind({"cmd", "shift"}, "T", function()
    ytTranscribe.transcribeWithProgress(function(status, data)
        if status == "downloading" then
            hs.notify.new({title="YouTube", informativeText="Downloading..."}):send()
        elseif status == "completed" then
            hs.pasteboard.setContents(data)
            hs.notify.new({title="YouTube", informativeText="✅ Done!"}):send()
        elseif status == "error" then
            hs.notify.new({title="YouTube", informativeText="❌ " .. data}):send()
        end
    end)
end)
```

### Salvar Histórico de Transcrições

```lua
local ytTranscribe = dofile(hs.configdir .. "/youtube-transcribe/init.lua")
local historyFile = hs.configdir .. "/transcription_history.json"

-- Wrapper que salva histórico
local function transcribeAndSave()
    local url = hs.pasteboard.getContents()
    
    ytTranscribe.transcribeYouTubeFromClipboard()
    
    -- Salvar no histórico
    local history = {}
    local file = io.open(historyFile, "r")
    if file then
        history = hs.json.decode(file:read("*a")) or {}
        file:close()
    end
    
    table.insert(history, {
        url = url,
        timestamp = os.time(),
        date = os.date("%Y-%m-%d %H:%M:%S")
    })
    
    file = io.open(historyFile, "w")
    file:write(hs.json.encode(history))
    file:close()
end

hs.hotkey.bind({"cmd", "shift"}, "T", transcribeAndSave)
```

### Multi-idioma com Seleção Manual

```lua
-- Modificar youtube_transcribe.py para aceitar --language flag
-- Adicionar chooser para selecionar idioma

local function transcribeWithLanguageSelection()
    local languages = {
        {text = "Auto-detect", code = "auto"},
        {text = "Português", code = "pt"},
        {text = "English", code = "en"},
        {text = "Español", code = "es"},
        {text = "Français", code = "fr"},
    }
    
    local chooser = hs.chooser.new(function(choice)
        if choice then
            -- Modificar comando para incluir --language
            -- (requer modificação no script Python)
            ytTranscribe.transcribeYouTubeFromClipboard(choice.code)
        end
    end)
    
    chooser:choices(languages)
    chooser:show()
end

hs.hotkey.bind({"cmd", "shift", "alt"}, "T", transcribeWithLanguageSelection)
```

## 🔧 Troubleshooting de Integração

### Verificar se módulo está carregado

```lua
-- Adicionar no final do init.lua
if ytTranscribe then
    print("✅ YouTube Transcribe module loaded successfully")
else
    print("❌ Failed to load YouTube Transcribe module")
end
```

### Debug de comandos

```lua
-- Adicionar logging detalhado
local function debugTranscribe()
    local url = hs.pasteboard.getContents()
    print("Clipboard content:", url)
    
    local pythonPath = getPythonPath()
    print("Python path:", pythonPath)
    
    local command = string.format('%s "%s" "%s"', pythonPath, PYTHON_SCRIPT, url)
    print("Command:", command)
    
    -- Execute com verbose
end

hs.hotkey.bind({"cmd", "shift", "ctrl"}, "D", debugTranscribe)
```

## 📚 Recursos Adicionais

- [Hammerspoon API Documentation](https://www.hammerspoon.org/docs/)
- [Hammerspoon Getting Started Guide](https://www.hammerspoon.org/go/)
- [Community Spoons](https://www.hammerspoon.org/Spoons/)

## 🤝 Exemplos da Comunidade

Compartilhe seu setup! Abra um PR com seus exemplos de integração.
