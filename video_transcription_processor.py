#!/usr/bin/env python3
"""
Script para processar video longo (Recording.mp4) com:
1. Melhoria da qualidade do áudio
2. Divisão em chunks
3. Transcrição usando Whisper
4. Concatenação e refinamento com IA

Autor: Background Agent
Data: 2025-10-03
"""

import os
import sys
import logging
from pathlib import Path
from typing import List, Optional
import time
import subprocess
import json

# Third-party imports
try:
    import torch
    from faster_whisper import WhisperModel
    from pydub import AudioSegment
    from pydub.effects import normalize, high_pass_filter, low_pass_filter
    from openai import OpenAI
    from dotenv import load_dotenv
except ImportError as e:
    print(f"Erro ao importar dependências: {e}")
    print("Execute: pip install -r requirements.txt")
    sys.exit(1)

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('transcription_process.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class AudioTranscriptionProcessor:
    """Processador principal para transcrição de áudio longo."""
    
    def __init__(
        self,
        input_file: str = "/Users/rodrigomiranda/useful-repos/audio_transcription/long-audio/Recording.m4a",
        output_dir: str = "transcription_output",
        chunk_duration_minutes: int = 5,
        whisper_model_size: str = "large-v2"
    ):
        self.input_file = Path(input_file)
        self.output_dir = Path(output_dir)
        self.chunk_duration = chunk_duration_minutes * 60  # Converter para segundos
        self.whisper_model_size = whisper_model_size
        
        # Criar diretórios necessários
        self.output_dir.mkdir(exist_ok=True)
        self.chunks_dir = self.output_dir / "audio_chunks"
        self.chunks_dir.mkdir(exist_ok=True)
        
        # Carregar variáveis de ambiente
        load_dotenv()
        
        # Inicializar modelo Whisper
        self.whisper_model = None
        
        # Inicializar cliente OpenAI
        self.openai_client = None
        if os.getenv("OPENAI_API_KEY"):
            self.openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        logger.info(f"Processador inicializado para: {self.input_file}")
    
    def extract_and_enhance_audio(self) -> Path:
        """
        Processa e melhora a qualidade do arquivo de áudio M4A.
        
        Returns:
            Path para o arquivo de áudio processado
        """
        logger.info("Iniciando processamento e melhoria do áudio...")
        
        # Verificar se o arquivo de áudio existe
        if not self.input_file.exists():
            raise FileNotFoundError(f"Arquivo não encontrado: {self.input_file}")
        
        enhanced_audio_path = self.output_dir / "enhanced_audio.wav"
        
        try:
            # Usar FFmpeg para conversão e melhoria do M4A
            ffmpeg_command = [
                "ffmpeg", "-i", str(self.input_file),
                "-af", (
                    "highpass=f=80,"           # Remove frequências baixas (ruído)
                    "lowpass=f=8000,"         # Remove frequências muito altas
                    "dynaudnorm=f=75:g=25,"   # Normalização dinâmica
                    "anlmdn=s=0.001:p=0.001," # Redução de ruído
                    "acompressor=threshold=0.089:ratio=9:attack=0.003:release=0.09"  # Compressor
                ),
                "-ar", "16000",               # Taxa de amostragem para Whisper
                "-ac", "1",                   # Mono
                "-y",                         # Sobrescrever arquivo existente
                str(enhanced_audio_path)
            ]
            
            logger.info("Executando comando FFmpeg para melhoria do áudio...")
            result = subprocess.run(ffmpeg_command, capture_output=True, text=True, check=True)
            
            logger.info(f"Áudio processado salvo em: {enhanced_audio_path}")
            return enhanced_audio_path
            
        except subprocess.CalledProcessError as e:
            logger.error(f"Erro no FFmpeg: {e.stderr}")
            raise
        except Exception as e:
            logger.error(f"Erro na extração do áudio: {e}")
            raise
    
    def detect_silence_and_split(self, audio_path: Path) -> List[Path]:
        """
        Detecta momentos de silêncio e divide o áudio em chunks inteligentes.
        
        Args:
            audio_path: Caminho para o arquivo de áudio
            
        Returns:
            Lista de caminhos dos chunks de áudio
        """
        logger.info("Carregando áudio para divisão em chunks...")
        
        try:
            # Carregar áudio com pydub
            audio = AudioSegment.from_wav(str(audio_path))
            logger.info(f"Áudio carregado: {len(audio) / 1000:.1f} segundos")
            
            chunk_paths = []
            chunk_duration_ms = self.chunk_duration * 1000  # Converter para ms
            
            # Dividir em chunks de duração fixa, mas tentando quebrar em silêncios
            for i in range(0, len(audio), chunk_duration_ms):
                end_time = min(i + chunk_duration_ms, len(audio))
                
                # Se não é o último chunk, tentar encontrar um ponto de silêncio próximo
                if end_time < len(audio):
                    # Procurar silêncio nos últimos 30 segundos do chunk
                    search_start = max(end_time - 30000, i)  # 30s antes do fim
                    search_segment = audio[search_start:end_time]
                    
                    # Detectar silêncio (threshold baixo para capturar pausas sutis)
                    silence_threshold = search_segment.dBFS - 20  # 20 dB abaixo da média
                    
                    # Procurar o último momento de silêncio
                    for j in range(len(search_segment) - 1000, 0, -1000):  # Procurar em janelas de 1s
                        if j < len(search_segment) and search_segment[j:j+1000].dBFS < silence_threshold:
                            end_time = search_start + j
                            break
                
                # Extrair o chunk
                chunk = audio[i:end_time]
                
                # Pular chunks muito pequenos (menos de 10 segundos)
                if len(chunk) < 10000:
                    continue
                
                chunk_filename = f"chunk_{i//1000:05d}_{end_time//1000:05d}.wav"
                chunk_path = self.chunks_dir / chunk_filename
                
                # Aplicar normalização adicional no chunk
                normalized_chunk = normalize(chunk)
                normalized_chunk.export(str(chunk_path), format="wav")
                
                chunk_paths.append(chunk_path)
                logger.info(f"Chunk criado: {chunk_filename} ({len(chunk)/1000:.1f}s)")
            
            logger.info(f"Total de chunks criados: {len(chunk_paths)}")
            return chunk_paths
            
        except Exception as e:
            logger.error(f"Erro na divisão do áudio: {e}")
            raise
    
    def transcribe_chunks(self, chunk_paths: List[Path]) -> List[str]:
        """
        Transcreve cada chunk usando Whisper.
        
        Args:
            chunk_paths: Lista de caminhos dos chunks
            
        Returns:
            Lista de transcrições
        """
        logger.info("Iniciando transcrição dos chunks...")
        
        try:
            # Inicializar modelo Whisper se necessário
            if self.whisper_model is None:
                logger.info(f"Carregando modelo Whisper: {self.whisper_model_size}")
                device = "cuda" if torch.cuda.is_available() else "cpu"
                compute_type = "float16" if device == "cuda" else "int8"
                
                self.whisper_model = WhisperModel(
                    self.whisper_model_size,
                    device=device,
                    compute_type=compute_type
                )
                logger.info(f"Modelo Whisper carregado em: {device}")
            
            transcriptions = []
            
            for i, chunk_path in enumerate(chunk_paths):
                logger.info(f"Transcrevendo chunk {i+1}/{len(chunk_paths)}: {chunk_path.name}")
                
                try:
                    # Transcrever o chunk
                    segments, info = self.whisper_model.transcribe(
                        str(chunk_path),
                        language="pt",  # Português
                        beam_size=5,
                        best_of=5,
                        temperature=0.0,
                        condition_on_previous_text=False
                    )
                    
                    # Juntar todos os segmentos do chunk
                    chunk_text = ""
                    for segment in segments:
                        chunk_text += segment.text + " "
                    
                    chunk_text = chunk_text.strip()
                    
                    if chunk_text:
                        # Adicionar marcador de chunk para facilitar refinamento posterior
                        marked_text = f"[CHUNK {i+1}] {chunk_text}"
                        transcriptions.append(marked_text)
                        logger.info(f"Chunk {i+1} transcrito: {len(chunk_text)} caracteres")
                    else:
                        logger.warning(f"Chunk {i+1} resultou em transcrição vazia")
                        transcriptions.append(f"[CHUNK {i+1}] [SILÊNCIO OU SEM ÁUDIO DETECTÁVEL]")
                        
                except Exception as e:
                    logger.error(f"Erro ao transcrever chunk {i+1}: {e}")
                    transcriptions.append(f"[CHUNK {i+1}] [ERRO NA TRANSCRIÇÃO: {str(e)}]")
            
            logger.info(f"Transcrição concluída: {len(transcriptions)} chunks processados")
            return transcriptions
            
        except Exception as e:
            logger.error(f"Erro no processo de transcrição: {e}")
            raise
    
    def concatenate_transcriptions(self, transcriptions: List[str]) -> str:
        """
        Concatena todas as transcrições em um texto único.
        
        Args:
            transcriptions: Lista de transcrições
            
        Returns:
            Texto concatenado
        """
        logger.info("Concatenando transcrições...")
        
        # Adicionar cabeçalho informativo
        header = f"""# TRANSCRIÇÃO BRUTA - Recording.mp4
# Processado em: {time.strftime('%Y-%m-%d %H:%M:%S')}
# Total de chunks: {len(transcriptions)}
# Status: Transcrição automática, requer refinamento

"""
        
        # Concatenar todas as transcrições com quebras de linha
        full_text = header + "\n\n".join(transcriptions)
        
        # Salvar como transcricao-bruta.txt
        raw_transcription_path = self.output_dir / "transcricao-bruta.txt"
        
        with open(raw_transcription_path, 'w', encoding='utf-8') as f:
            f.write(full_text)
        
        logger.info(f"Transcrição bruta salva em: {raw_transcription_path}")
        return full_text
    
    def refine_with_ai(self, raw_text: str) -> str:
        """
        Usa IA (OpenAI) para refinar a transcrição.
        
        Args:
            raw_text: Texto bruto da transcrição
            
        Returns:
            Texto refinado
        """
        logger.info("Iniciando refinamento com IA...")
        
        if not self.openai_client:
            logger.warning("OpenAI API key não configurada. Pulando refinamento.")
            return raw_text
        
        try:
            # Prompt para refinamento
            refinement_prompt = """Esse arquivo é uma transcrição feita em chunks, revise-a para clareza. Algumas partes podem estar confusas por conta do chunking.

Instruções para refinamento:
1. Corrija erros de transcrição óbvios
2. Una frases que foram cortadas entre chunks
3. Melhore a pontuação e formatação
4. Mantenha o significado original
5. Remova marcadores de chunks desnecessários
6. Organize o texto em parágrafos lógicos
7. Sinalize trechos onde havia silêncio ou áudio inaudível

Texto a ser refinado:
"""

            # Dividir o texto em partes menores se for muito longo
            max_chunk_size = 15000  # Caracteres por requisição
            text_parts = []
            
            if len(raw_text) > max_chunk_size:
                # Dividir o texto preservando parágrafos
                parts = raw_text.split('\n\n')
                current_part = ""
                
                for part in parts:
                    if len(current_part + part) > max_chunk_size and current_part:
                        text_parts.append(current_part.strip())
                        current_part = part
                    else:
                        current_part += "\n\n" + part if current_part else part
                
                if current_part:
                    text_parts.append(current_part.strip())
            else:
                text_parts = [raw_text]
            
            refined_parts = []
            
            for i, part in enumerate(text_parts):
                logger.info(f"Refinando parte {i+1}/{len(text_parts)} com IA...")
                
                try:
                    response = self.openai_client.chat.completions.create(
                        model="gpt-4o",
                        messages=[
                            {"role": "system", "content": "Você é um especialista em revisão e refinamento de transcrições de áudio. Sua tarefa é melhorar a clareza e correção do texto mantendo o significado original."},
                            {"role": "user", "content": refinement_prompt + part}
                        ],
                        max_tokens=4000,
                        temperature=0.1
                    )
                    
                    refined_part = response.choices[0].message.content.strip()
                    refined_parts.append(refined_part)
                    
                    logger.info(f"Parte {i+1} refinada com sucesso")
                    
                    # Pequena pausa entre requisições
                    time.sleep(1)
                    
                except Exception as e:
                    logger.error(f"Erro ao refinar parte {i+1}: {e}")
                    refined_parts.append(part)  # Usar texto original em caso de erro
            
            # Juntar todas as partes refinadas
            refined_text = "\n\n".join(refined_parts)
            
            # Adicionar cabeçalho ao texto refinado
            refined_header = f"""# TRANSCRIÇÃO REFINADA - Recording.mp4
# Processado em: {time.strftime('%Y-%m-%d %H:%M:%S')}
# Status: Revisado e refinado com IA

"""
            
            final_text = refined_header + refined_text
            
            # Salvar texto refinado
            refined_path = self.output_dir / "transcricao-final.txt"
            with open(refined_path, 'w', encoding='utf-8') as f:
                f.write(final_text)
            
            logger.info(f"Transcrição refinada salva em: {refined_path}")
            return final_text
            
        except Exception as e:
            logger.error(f"Erro no refinamento com IA: {e}")
            logger.info("Retornando texto original sem refinamento")
            return raw_text
    
    def process_audio(self) -> dict:
        """
        Executa todo o pipeline de processamento do áudio.
        
        Returns:
            Dicionário com informações do processamento
        """
        start_time = time.time()
        logger.info("=== INICIANDO PROCESSAMENTO DO ÁUDIO ===")
        
        try:
            # 1. Processar e melhorar áudio
            logger.info("Etapa 1/5: Processamento e melhoria do áudio")
            enhanced_audio = self.extract_and_enhance_audio()
            
            # 2. Dividir em chunks
            logger.info("Etapa 2/5: Divisão em chunks")
            chunk_paths = self.detect_silence_and_split(enhanced_audio)
            
            # 3. Transcrever chunks
            logger.info("Etapa 3/5: Transcrição dos chunks")
            transcriptions = self.transcribe_chunks(chunk_paths)
            
            # 4. Concatenar transcrições
            logger.info("Etapa 4/5: Concatenação das transcrições")
            raw_text = self.concatenate_transcriptions(transcriptions)
            
            # 5. Refinar com IA
            logger.info("Etapa 5/5: Refinamento com IA")
            final_text = self.refine_with_ai(raw_text)
            
            # Calcular estatísticas
            total_time = time.time() - start_time
            
            result = {
                "success": True,
                "input_file": str(self.input_file),
                "output_directory": str(self.output_dir),
                "total_chunks": len(chunk_paths),
                "raw_transcription_file": str(self.output_dir / "transcricao-bruta.txt"),
                "final_transcription_file": str(self.output_dir / "transcricao-final.txt"),
                "processing_time_seconds": round(total_time, 2),
                "processing_time_formatted": time.strftime('%H:%M:%S', time.gmtime(total_time))
            }
            
            logger.info("=== PROCESSAMENTO CONCLUÍDO COM SUCESSO ===")
            logger.info(f"Tempo total: {result['processing_time_formatted']}")
            logger.info(f"Chunks processados: {result['total_chunks']}")
            logger.info(f"Arquivo final: {result['final_transcription_file']}")
            
            return result
            
        except Exception as e:
            logger.error(f"Erro no processamento: {e}")
            return {
                "success": False,
                "error": str(e),
                "processing_time_seconds": time.time() - start_time
            }


def main():
    """Função principal do script."""
    print("🎵 PROCESSADOR DE TRANSCRIÇÃO DE ÁUDIO 🎵")
    print("=" * 50)
    
    # Verificar se o arquivo Recording.m4a existe
    audio_file = "/Users/rodrigomiranda/useful-repos/audio_transcription/long-audio/Recording.m4a"
    if not Path(audio_file).exists():
        print(f"❌ Erro: Arquivo não encontrado: {audio_file}")
        print("Por favor, certifique-se de que o arquivo está presente antes de executar o script.")
        sys.exit(1)
    
    # Criar processador
    processor = AudioTranscriptionProcessor(
        input_file=audio_file,
        chunk_duration_minutes=5,  # Chunks de 5 minutos
        whisper_model_size="large-v2"  # Melhor qualidade
    )
    
    # Executar processamento
    result = processor.process_audio()
    
    # Mostrar resultados
    print("\n" + "=" * 50)
    if result["success"]:
        print("✅ PROCESSAMENTO CONCLUÍDO!")
        print(f"📁 Diretório de saída: {result['output_directory']}")
        print(f"📄 Transcrição bruta: {result['raw_transcription_file']}")
        print(f"📄 Transcrição final: {result['final_transcription_file']}")
        print(f"⏱️  Tempo de processamento: {result['processing_time_formatted']}")
        print(f"📊 Total de chunks: {result['total_chunks']}")
    else:
        print("❌ PROCESSAMENTO FALHOU!")
        print(f"Erro: {result['error']}")
        sys.exit(1)


if __name__ == "__main__":
    main()