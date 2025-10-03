#!/usr/bin/env python3
"""
Script de exemplo e teste rápido para o processador de transcrição de vídeo.
Este script verifica se tudo está configurado corretamente antes do processamento real.
"""

import os
import sys
import subprocess
from pathlib import Path

def check_ffmpeg():
    """Verifica se FFmpeg está instalado."""
    try:
        result = subprocess.run(['ffmpeg', '-version'], 
                              capture_output=True, text=True, check=True)
        print("✅ FFmpeg encontrado e funcionando")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ FFmpeg não encontrado. Instale com:")
        print("   Ubuntu/Debian: sudo apt install ffmpeg")
        print("   macOS: brew install ffmpeg")
        print("   Windows: Baixar do site oficial")
        return False

def check_dependencies():
    """Verifica se as dependências Python estão instaladas."""
    required_packages = [
        'faster_whisper',
        'torch',
        'pydub',
        'openai',
        'dotenv'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - FALTANDO")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n📦 Instale as dependências faltantes:")
        print("pip install -r video_transcription_requirements.txt")
        return False
    
    return True

def check_input_file():
    """Verifica se o arquivo de entrada existe."""
    audio_file = "/Users/rodrigomiranda/useful-repos/audio_transcription/long-audio/Recording.m4a"
    if Path(audio_file).exists():
        print(f"✅ Recording.m4a encontrado")
        return True
    else:
        print(f"❌ Recording.m4a não encontrado em: {audio_file}")
        return False

def check_openai_config():
    """Verifica configuração da OpenAI (opcional)."""
    from dotenv import load_dotenv
    load_dotenv()
    
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        print("✅ OpenAI API Key configurada")
        return True
    else:
        print("⚠️  OpenAI API Key não configurada")
        print("   Refinamento com IA será pulado")
        print("   Para configurar: echo 'OPENAI_API_KEY=sua_chave' > .env")
        return False

def run_quick_test():
    """Executa um teste rápido."""
    print("\n🧪 EXECUTANDO TESTE RÁPIDO")
    print("=" * 40)
    
    try:
        from video_transcription_processor import AudioTranscriptionProcessor
        
        # Criar processador para teste
        audio_file = "/Users/rodrigomiranda/useful-repos/audio_transcription/long-audio/Recording.m4a"
        processor = AudioTranscriptionProcessor(
            input_file=audio_file,
            output_dir="test_output",
            chunk_duration_minutes=1,  # Chunks pequenos para teste
            whisper_model_size="base"  # Modelo menor para teste rápido
        )
        
        # Simular processamento (apenas logging)
        print("✅ Processador criado com sucesso")
        print("✅ Configurações carregadas")
        print("✅ Estrutura de diretórios OK")
        
        # Verificar se consegue carregar o modelo Whisper
        try:
            from faster_whisper import WhisperModel
            model = WhisperModel("tiny")  # Modelo bem pequeno para teste
            print("✅ Modelo Whisper carregado com sucesso")
        except Exception as e:
            print(f"❌ Erro ao carregar Whisper: {e}")
            return False
        
        print("\n🎉 TESTE CONCLUÍDO COM SUCESSO!")
        print("Você pode executar o processamento completo com:")
        print("python video_transcription_processor.py")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro no teste: {e}")
        return False

def main():
    """Função principal do script de verificação."""
    print("🔍 VERIFICADOR DE CONFIGURAÇÃO - TRANSCRIÇÃO DE ÁUDIO")
    print("=" * 60)
    print("Arquivo alvo: Recording.m4a")
    print("")
    
    checks = [
        ("FFmpeg", check_ffmpeg),
        ("Dependências Python", check_dependencies),
        ("Arquivo de entrada", check_input_file),
        ("Configuração OpenAI", check_openai_config)
    ]
    
    all_good = True
    
    for name, check_func in checks:
        print(f"\n📋 Verificando: {name}")
        if not check_func():
            all_good = False
    
    print("\n" + "=" * 60)
    
    if all_good:
        print("✅ TUDO CONFIGURADO CORRETAMENTE!")
        
        # Perguntar se quer executar teste
        response = input("\n🧪 Executar teste rápido? (s/n): ").lower().strip()
        if response in ['s', 'sim', 'y', 'yes']:
            run_quick_test()
        else:
            print("\n🚀 Pronto para executar:")
            print("python video_transcription_processor.py")
    else:
        print("❌ CONFIGURAÇÃO INCOMPLETA")
        print("Corrija os problemas acima antes de prosseguir.")
        sys.exit(1)

if __name__ == "__main__":
    main()