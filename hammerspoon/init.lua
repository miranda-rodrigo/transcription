-- Example integration for Hammerspoon
-- Adjust the path below to point to your repo clone

local repo_path = hs.fs.pathToAbsolute(os.getenv('YT_TRANSCRIBE_REPO') or '/workspace')
local module_path = repo_path .. '/hammerspoon/youtube_transcribe.lua'
local youtube_transcribe = dofile(module_path)

youtube_transcribe.bindHotkey({'cmd','alt'}, 't')




