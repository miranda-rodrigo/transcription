#!/bin/zsh

# Caminho correto para ffmpeg e python via pyenv
export PATH="/opt/homebrew/bin:/Users/rodrigomiranda/.pyenv/shims:$PATH"

# Carrega a chave da OpenAI do arquivo .env
if [ -f .env ]; then
    export $(grep -v '^#' .env | xargs)
fi

# Executa o script de transcrição
/Users/rodrigomiranda/.pyenv/shims/python3 /Users/rodrigomiranda/useful-repos/download-whatsapp/zap.py "$1"
