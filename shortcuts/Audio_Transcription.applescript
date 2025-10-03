-- Audio Transcription Shortcut for macOS Shortcuts App
-- This script integrates our transcribe-shortcut into macOS Shortcuts
-- 
-- Usage: Can be called with text input (file path or URL) or without input (uses clipboard)

on run {input, parameters}
	-- Get the repository root directory (hardcoded path for reliability)
	set repoRoot to "/Users/rodrigomiranda/useful-repos/audio_transcription"
	set transcribeScript to repoRoot & "/bin/transcribe-shortcut"
	
	try
		-- Check if input is provided
		if (count of input) > 0 then
			-- Use provided input (file path or URL)
			set inputText to item 1 of input as text
			set shellCommand to quoted form of transcribeScript & " " & quoted form of inputText
		else
			-- Use clipboard workflow
			set shellCommand to quoted form of transcribeScript & " --from-clipboard --to-clipboard"
		end if
		
		-- Execute transcription
		set transcriptResult to do shell script shellCommand
		
		-- Show notification
		display notification "Transcription completed!" with title "Audio Transcription"
		
		-- Return result
		return transcriptResult
		
	on error errorMessage number errorNumber
		-- Handle errors gracefully
		display notification errorMessage with title "Transcription Error"
		return "Transcription failed: " & errorMessage
	end try
end run