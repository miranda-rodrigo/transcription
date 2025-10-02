-- Hammerspoon module: Transcribe YouTube URL from clipboard
-- Reads URL from clipboard, runs Python pipeline, and sets clipboard to transcript.
-- Place this file in your repo and require it from your Hammerspoon config.

local M = {}

local function isYouTubeUrl(url)
  if url == nil then return false end
  return string.match(url, 'https?://[%w%.%-]*youtube%.com/') or string.match(url, 'https?://youtu%.be/')
end

local function repoRootFromThisFile()
  -- Resolve repo root as parent of this file's directory
  local src = debug.getinfo(1, 'S').source
  if src:sub(1,1) == '@' then src = src:sub(2) end
  local dir = src:match('(.*/)') or './'
  -- assuming structure: repo/hammerspoon/this_file.lua -> repo
  return hs.fs.pathToAbsolute(dir .. '../')
end

local function pythonScriptPath()
  local root = repoRootFromThisFile()
  return root .. '/scripts/transcribe_youtube.py'
end

function M.transcribeFromClipboard()
  local url = hs.pasteboard.getContents()
  if not isYouTubeUrl(url) then
    hs.alert.show('Clipboard não contém um URL do YouTube')
    return
  end

  local script = pythonScriptPath()
  if not hs.fs.attributes(script) then
    hs.alert.show('Script Python não encontrado: ' .. script)
    return
  end

  hs.alert.show('Transcrevendo áudio do YouTube...')
  local cmd = string.format('/usr/bin/env python3 %q --url %q --review auto --to-clipboard', script, url)
  local output, success, typ, rc = hs.execute(cmd, true)
  if success then
    -- Transcript already copied by Python; ensure clipboard contains latest output as fallback
    if output and #output > 0 then
      hs.pasteboard.setContents(output)
    end
    hs.alert.show('Transcript copiado para a área de transferência')
  else
    local msg = output or ('Erro de execução (code ' .. tostring(rc) .. ')')
    hs.alert.show('Falha na transcrição: ' .. msg)
  end
end

-- Optional helper to bind a hotkey (example: cmd+alt+t)
function M.bindHotkey(mods, key)
  hs.hotkey.bind(mods, key, function()
    M.transcribeFromClipboard()
  end)
end

return M
