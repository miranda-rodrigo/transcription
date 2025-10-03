-- Simplified AppleScript for macOS Shortcuts
-- Copy and paste this script into the "Run AppleScript" action in Shortcuts app

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
