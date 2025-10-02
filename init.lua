-- Hammerspoon YouTube Audio Transcription Module
-- Reads YouTube URL from clipboard, downloads audio, transcribes with Whisper,
-- and copies transcript back to clipboard

local module = {}

-- Configuration
local SCRIPT_DIR = hs.configdir .. "/youtube-transcribe"
local PYTHON_SCRIPT = SCRIPT_DIR .. "/youtube_transcribe.py"
local VENV_PYTHON = SCRIPT_DIR .. "/venv/bin/python3"

-- Check if Python virtualenv exists, otherwise use system python3
local function getPythonPath()
    local file = io.open(VENV_PYTHON, "r")
    if file then
        file:close()
        return VENV_PYTHON
    end
    return "/usr/bin/env python3"
end

-- Show notification to user
local function notify(title, message, type)
    hs.notify.new({
        title = title,
        informativeText = message,
        contentImage = type == "error" and nil or nil,
        withdrawAfter = type == "error" and 10 or 5
    }):send()
end

-- Main transcription function
function module.transcribeYouTubeFromClipboard()
    -- Get URL from clipboard
    local clipboardContent = hs.pasteboard.getContents()
    
    if not clipboardContent or clipboardContent == "" then
        notify("YouTube Transcribe", "Clipboard is empty!", "error")
        return
    end
    
    -- Check if it's a YouTube URL
    if not string.match(clipboardContent, "youtube%.com") and 
       not string.match(clipboardContent, "youtu%.be") then
        notify("YouTube Transcribe", "No YouTube URL found in clipboard!", "error")
        return
    end
    
    notify("YouTube Transcribe", "Starting transcription...\nThis may take a few minutes.", "info")
    
    -- Get Python path
    local pythonPath = getPythonPath()
    
    -- Prepare command
    local command = string.format('%s "%s" "%s"', pythonPath, PYTHON_SCRIPT, clipboardContent)
    
    -- Execute asynchronously
    hs.task.new("/bin/bash", function(exitCode, stdOut, stdErr)
        if exitCode == 0 then
            -- Copy transcript to clipboard
            hs.pasteboard.setContents(stdOut)
            notify("YouTube Transcribe", "✅ Transcription completed!\nText copied to clipboard.", "success")
        else
            notify("YouTube Transcribe", "❌ Error: " .. (stdErr or "Unknown error"), "error")
            print("STDERR:", stdErr)
            print("STDOUT:", stdOut)
        end
    end, {"-c", command}):start()
end

-- Bind to hotkey (optional - can be configured by user)
-- Example: Cmd+Shift+T
-- hs.hotkey.bind({"cmd", "shift"}, "T", function()
--     module.transcribeYouTubeFromClipboard()
-- end)

return module
