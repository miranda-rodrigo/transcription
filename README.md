# Audio Transcription Project

Este projeto contém scripts para transcrição de áudio usando a API da OpenAI.

## Arquivos

- `transcribe.py` - Script principal de transcrição em Python
- `transcribe.sh` - Script shell para execução da transcrição
- `env.example` - Arquivo de exemplo para configuração de variáveis de ambiente

## Configuração

1. Copie o arquivo `env.example` para `.env`:
   ```bash
   cp env.example .env
   ```

2. Edite o arquivo `.env` e adicione sua chave da API OpenAI:
   ```
   OPENAI_API_KEY=sua_chave_real_aqui
   ```

## Uso

Execute o script de transcrição:
```bash
./transcribe.sh caminho_para_arquivo_audio
```

## Segurança

- O arquivo `.env` está incluído no `.gitignore` para proteger suas chaves de API
- Nunca commite chaves de API diretamente no código
- Use sempre o arquivo `.env` para variáveis sensíveis
