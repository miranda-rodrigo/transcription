#!/bin/bash
# Script de diagnóstico para YouTube Transcriber
# Verifica todas as dependências e configurações

echo "🔍 YouTube Transcriber - Diagnóstico"
echo "===================================="
echo ""

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
ERRORS=0
WARNINGS=0

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

check_ok() {
    echo -e "${GREEN}✓${NC} $1"
}

check_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
    ((WARNINGS++))
}

check_error() {
    echo -e "${RED}✗${NC} $1"
    ((ERRORS++))
}

# ============================================================================
echo "📋 Sistema Operacional"
echo "------------------------------------"

if [[ "$OSTYPE" == "darwin"* ]]; then
    check_ok "macOS detectado: $(sw_vers -productVersion)"
else
    check_warning "Sistema não é macOS (este projeto é otimizado para macOS)"
fi

echo ""

# ============================================================================
echo "🔧 Dependências do Sistema"
echo "------------------------------------"

# Homebrew
if command -v brew &> /dev/null; then
    check_ok "Homebrew instalado: $(brew --version | head -n1)"
else
    check_error "Homebrew não encontrado - instale em https://brew.sh/"
fi

# Python
if command -v python3 &> /dev/null; then
    check_ok "Python 3 instalado: $(python3 --version)"
else
    check_error "Python 3 não encontrado - instale com 'brew install python3'"
fi

# ffmpeg
if command -v ffmpeg &> /dev/null; then
    check_ok "ffmpeg instalado: $(ffmpeg -version | head -n1 | cut -d' ' -f3)"
else
    check_error "ffmpeg não encontrado - instale com 'brew install ffmpeg'"
fi

# Hammerspoon
if [ -d "/Applications/Hammerspoon.app" ]; then
    check_ok "Hammerspoon instalado"
    if [ -d "$HOME/.hammerspoon" ]; then
        check_ok "Diretório de configuração existe: ~/.hammerspoon"
    else
        check_warning "Diretório ~/.hammerspoon não existe - Hammerspoon precisa ser executado uma vez"
    fi
else
    check_error "Hammerspoon não encontrado - instale em https://www.hammerspoon.org/"
fi

echo ""

# ============================================================================
echo "🐍 Ambiente Virtual Python"
echo "------------------------------------"

if [ -d "$SCRIPT_DIR/venv" ]; then
    check_ok "Virtual environment encontrado"
    
    if [ -f "$SCRIPT_DIR/venv/bin/python3" ]; then
        check_ok "Python no venv: $($SCRIPT_DIR/venv/bin/python3 --version)"
        
        # Verificar pacotes instalados
        echo ""
        echo "Verificando pacotes Python..."
        
        for package in openai yt-dlp pydub python-dotenv; do
            if $SCRIPT_DIR/venv/bin/python3 -c "import $package" 2>/dev/null; then
                VERSION=$($SCRIPT_DIR/venv/bin/pip show $package 2>/dev/null | grep Version | cut -d' ' -f2)
                check_ok "$package instalado (v$VERSION)"
            else
                check_error "$package não instalado - execute 'pip install -r requirements.txt'"
            fi
        done
    else
        check_error "Python não encontrado no venv"
    fi
else
    check_error "Virtual environment não encontrado - execute './setup.sh'"
fi

echo ""

# ============================================================================
echo "🔑 Configuração"
echo "------------------------------------"

# Arquivo .env
if [ -f "$SCRIPT_DIR/.env" ]; then
    check_ok "Arquivo .env encontrado"
    
    if grep -q "OPENAI_API_KEY=sk-" "$SCRIPT_DIR/.env" 2>/dev/null; then
        check_ok "OPENAI_API_KEY configurada"
    elif grep -q "OPENAI_API_KEY=" "$SCRIPT_DIR/.env" 2>/dev/null; then
        check_warning "OPENAI_API_KEY presente mas parece não estar configurada"
    else
        check_error "OPENAI_API_KEY não encontrada no .env"
    fi
else
    check_error "Arquivo .env não encontrado - copie de env.example e configure"
fi

echo ""

# ============================================================================
echo "📁 Arquivos do Projeto"
echo "------------------------------------"

for file in init.lua youtube_transcribe.py requirements.txt setup.sh; do
    if [ -f "$SCRIPT_DIR/$file" ]; then
        check_ok "$file existe"
    else
        check_error "$file não encontrado"
    fi
done

echo ""

# ============================================================================
echo "🔗 Integração com Hammerspoon"
echo "------------------------------------"

if [ -d "$HOME/.hammerspoon/youtube-transcribe" ]; then
    check_ok "Módulo instalado em ~/.hammerspoon/youtube-transcribe"
    
    # Verificar arquivos copiados
    if [ -f "$HOME/.hammerspoon/youtube-transcribe/youtube_transcribe.py" ]; then
        check_ok "youtube_transcribe.py copiado"
    else
        check_warning "youtube_transcribe.py não encontrado - execute './setup.sh'"
    fi
    
    if [ -f "$HOME/.hammerspoon/youtube-transcribe/.env" ]; then
        check_ok ".env copiado"
    else
        check_warning ".env não encontrado no diretório do Hammerspoon"
    fi
else
    check_warning "Módulo não instalado no Hammerspoon - execute './setup.sh'"
fi

# Verificar init.lua do Hammerspoon
if [ -f "$HOME/.hammerspoon/init.lua" ]; then
    check_ok "~/.hammerspoon/init.lua existe"
    
    if grep -q "youtube-transcribe" "$HOME/.hammerspoon/init.lua" 2>/dev/null; then
        check_ok "Referência ao módulo encontrada no init.lua"
    else
        check_warning "Módulo não parece estar integrado ao init.lua"
        echo "         Adicione ao ~/.hammerspoon/init.lua:"
        echo "         local ytTranscribe = dofile(hs.configdir .. \"/youtube-transcribe/init.lua\")"
    fi
else
    check_warning "~/.hammerspoon/init.lua não encontrado"
fi

echo ""

# ============================================================================
echo "📊 Resumo"
echo "===================================="

if [ $ERRORS -eq 0 ] && [ $WARNINGS -eq 0 ]; then
    echo -e "${GREEN}✓ Tudo OK! Sistema pronto para uso.${NC}"
    echo ""
    echo "Para usar:"
    echo "1. Copie um URL do YouTube"
    echo "2. Pressione Cmd+Shift+T (ou seu atalho configurado)"
    echo "3. Aguarde a notificação"
elif [ $ERRORS -eq 0 ]; then
    echo -e "${YELLOW}Sistema funcional com $WARNINGS aviso(s).${NC}"
    echo "Revise os avisos acima para otimizar a configuração."
else
    echo -e "${RED}Encontrados $ERRORS erro(s) e $WARNINGS aviso(s).${NC}"
    echo "Corrija os erros antes de usar o sistema."
    echo ""
    echo "Passos sugeridos:"
    if [ $ERRORS -gt 0 ]; then
        echo "1. Execute './setup.sh' para instalar dependências"
        echo "2. Configure a API key no arquivo .env"
        echo "3. Execute este diagnóstico novamente"
    fi
fi

echo ""

# ============================================================================
echo "🧪 Teste Rápido"
echo "===================================="
echo ""
echo "Para testar manualmente:"
echo "  ./test_local.sh \"https://www.youtube.com/watch?v=jNQXAC9IVRw\""
echo ""
echo "Para ver logs detalhados:"
echo "  tail -f /tmp/youtube_transcribe.log  (se implementado)"
echo ""
echo "Para abrir console do Hammerspoon:"
echo "  Clique no ícone do Hammerspoon → Console"
echo ""

exit $ERRORS
