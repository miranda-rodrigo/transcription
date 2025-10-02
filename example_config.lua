-- Exemplo de Configuração Completa do Hammerspoon
-- com YouTube Transcription integrado
-- 
-- Copie as partes relevantes para o seu ~/.hammerspoon/init.lua

-- ============================================================================
-- CONFIGURAÇÃO BÁSICA
-- ============================================================================

-- Recarregar automaticamente quando config muda
function reloadConfig(files)
    local doReload = false
    for _, file in pairs(files) do
        if file:sub(-4) == ".lua" then
            doReload = true
        end
    end
    if doReload then
        hs.reload()
    end
end
local myWatcher = hs.pathwatcher.new(os.getenv("HOME") .. "/.hammerspoon/", reloadConfig):start()
hs.alert.show("Config loaded")

-- ============================================================================
-- YOUTUBE TRANSCRIPTION MODULE
-- ============================================================================

local ytTranscribe = dofile(hs.configdir .. "/youtube-transcribe/init.lua")

-- Atalho principal: Cmd+Shift+T
hs.hotkey.bind({"cmd", "shift"}, "T", function()
    ytTranscribe.transcribeYouTubeFromClipboard()
end)

-- ============================================================================
-- OPÇÕES AVANÇADAS (ESCOLHA O QUE USAR)
-- ============================================================================

-- Opção 1: Adicionar ao menu bar
local menubar = hs.menubar.new()
if menubar then
    menubar:setTitle("🎬")
    menubar:setTooltip("YouTube Transcriber")
    menubar:setMenu({
        {
            title = "Transcribe from Clipboard",
            fn = ytTranscribe.transcribeYouTubeFromClipboard,
            tooltip = "Cmd+Shift+T"
        },
        {
            title = "-"  -- separator
        },
        {
            title = "Open Transcriptions Folder",
            fn = function()
                os.execute("open ~/Documents/transcriptions")
            end
        },
        {
            title = "View Console",
            fn = function()
                hs.openConsole()
            end
        },
        {
            title = "-"
        },
        {
            title = "Reload Hammerspoon",
            fn = function()
                hs.reload()
            end,
            tooltip = "Cmd+Alt+R"
        }
    })
end

-- Opção 2: Menu de ações rápidas com Chooser
local function showQuickActions()
    local choices = {
        {
            text = "📝 Transcribe YouTube",
            subText = "Download and transcribe YouTube video from clipboard",
            image = hs.image.imageFromName("NSActionTemplate"),
            action = ytTranscribe.transcribeYouTubeFromClipboard
        },
        {
            text = "🔄 Reload Hammerspoon",
            subText = "Reload configuration",
            image = hs.image.imageFromName("NSRefreshTemplate"),
            action = function() hs.reload() end
        },
        {
            text = "📊 Show Console",
            subText = "Open Hammerspoon console",
            image = hs.image.imageFromName("NSAdvanced"),
            action = function() hs.openConsole() end
        }
    }
    
    local chooser = hs.chooser.new(function(choice)
        if choice then
            choice.action()
        end
    end)
    
    chooser:choices(choices)
    chooser:placeholderText("Type to filter actions...")
    chooser:show()
end

-- Atalho para menu de ações: Cmd+Shift+Space
hs.hotkey.bind({"cmd", "shift"}, "space", showQuickActions)

-- Opção 3: Histórico de transcrições
local transcriptionHistory = {}
local HISTORY_FILE = hs.configdir .. "/transcription_history.json"

local function saveToHistory(url, status)
    table.insert(transcriptionHistory, {
        url = url,
        timestamp = os.time(),
        date = os.date("%Y-%m-%d %H:%M:%S"),
        status = status
    })
    
    -- Manter apenas últimas 50 entradas
    if #transcriptionHistory > 50 then
        table.remove(transcriptionHistory, 1)
    end
    
    -- Salvar em arquivo
    local file = io.open(HISTORY_FILE, "w")
    if file then
        file:write(hs.json.encode(transcriptionHistory))
        file:close()
    end
end

local function loadHistory()
    local file = io.open(HISTORY_FILE, "r")
    if file then
        local content = file:read("*a")
        file:close()
        transcriptionHistory = hs.json.decode(content) or {}
    end
end

loadHistory()

-- Wrapper que salva histórico
local function transcribeWithHistory()
    local url = hs.pasteboard.getContents()
    if url then
        saveToHistory(url, "started")
        ytTranscribe.transcribeYouTubeFromClipboard()
        -- Note: sucesso/erro seria detectado com callback (requer modificação do módulo)
    end
end

-- Usar este em vez do atalho direto se quiser histórico
-- hs.hotkey.bind({"cmd", "shift"}, "T", transcribeWithHistory)

-- Ver histórico
hs.hotkey.bind({"cmd", "shift", "ctrl"}, "H", function()
    local choices = {}
    for i = #transcriptionHistory, math.max(1, #transcriptionHistory - 20), -1 do
        local entry = transcriptionHistory[i]
        table.insert(choices, {
            text = entry.url,
            subText = entry.date .. " - " .. (entry.status or "unknown")
        })
    end
    
    if #choices == 0 then
        hs.alert.show("No transcription history")
        return
    end
    
    local chooser = hs.chooser.new(function(choice)
        if choice then
            hs.pasteboard.setContents(choice.text)
            hs.alert.show("URL copied to clipboard")
        end
    end)
    
    chooser:choices(choices)
    chooser:placeholderText("Transcription history...")
    chooser:show()
end)

-- ============================================================================
-- OUTROS ATALHOS ÚTEIS (OPCIONAL)
-- ============================================================================

-- Cmd+Alt+R: Recarregar config
hs.hotkey.bind({"cmd", "alt"}, "R", function()
    hs.reload()
end)

-- Cmd+Alt+C: Mostrar console
hs.hotkey.bind({"cmd", "alt"}, "C", function()
    hs.openConsole()
end)

-- Cmd+Shift+V: Colar como texto plano
hs.hotkey.bind({"cmd", "shift"}, "V", function()
    hs.eventtap.keyStrokes(hs.pasteboard.getContents())
end)

-- ============================================================================
-- NOTIFICAÇÕES CUSTOMIZADAS
-- ============================================================================

-- Mostrar notificação quando Hammerspoon carrega
hs.notify.new({
    title = "Hammerspoon",
    informativeText = "Configuration loaded successfully\nYouTube Transcriber ready!",
    withdrawAfter = 3,
    soundName = "Glass"
}):send()

-- ============================================================================
-- CONFIGURAÇÕES ADICIONAIS
-- ============================================================================

-- Desabilitar animações (opcional)
hs.window.animationDuration = 0

-- Console styling (opcional)
-- hs.console.darkMode(true)

-- Auto-update (se instalado via Homebrew)
-- hs.automaticUpdates(true)

print("✅ Hammerspoon config loaded successfully!")
print("🎬 YouTube Transcriber: Cmd+Shift+T")
print("⚡ Quick Actions: Cmd+Shift+Space")
print("📜 History: Cmd+Shift+Ctrl+H")
