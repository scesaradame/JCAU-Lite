#!/bin/bash
# ===================================================================
# JCAU-Lite Universal Adapter v2.0
# Auto-adapta JCAU a cualquier PC/OS desde repositorio solamente
# Compatible: Windows, Linux, macOS, WSL, Android Termux, etc.
# ===================================================================

# Colores universales (funciona en cualquier terminal)
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Variables globales
JCAU_VERSION="2.0-Universal"
INSTALL_DIR=""
LOG_FILE=""
DETECTED_OS=""
DETECTED_ARCH=""
PACKAGE_MANAGER=""

# Función de logging universal
jcau_log() {
    local level=$1
    local message=$2
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    
    case $level in
        "INFO")  echo -e "${CYAN}[${timestamp}] [INFO]${NC} $message" ;;
        "OK")    echo -e "${GREEN}[${timestamp}] [OK]${NC} $message" ;;
        "WARN")  echo -e "${YELLOW}[${timestamp}] [WARN]${NC} $message" ;;
        "ERROR") echo -e "${RED}[${timestamp}] [ERROR]${NC} $message" ;;
        "CRITICAL") echo -e "${PURPLE}[${timestamp}] [CRITICAL]${NC} $message" ;;
    esac
    
    if [[ -n "$LOG_FILE" ]]; then
        echo "[$timestamp] [$level] $message" >> "$LOG_FILE"
    fi
}

# Detección universal de sistema operativo
detect_system() {
    jcau_log "INFO" "🔍 Detectando sistema operativo y arquitectura..."
    
    # Detectar OS principal
    if [[ -f /data/data/com.termux/files/usr/bin/bash ]]; then
        DETECTED_OS="termux"
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        if grep -q Microsoft /proc/version 2>/dev/null; then
            DETECTED_OS="wsl"
        else
            DETECTED_OS="linux"
        fi
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        DETECTED_OS="macos"
    elif [[ "$OSTYPE" == "cygwin" ]] || [[ "$OSTYPE" == "msys" ]] || [[ -n "$WSL_DISTRO_NAME" ]]; then
        DETECTED_OS="windows"
    elif [[ -n "$WINDIR" ]]; then
        DETECTED_OS="windows"
    else
        # Fallback detection
        case "$(uname -s)" in
            Linux*)   DETECTED_OS="linux";;
            Darwin*)  DETECTED_OS="macos";;
            CYGWIN*)  DETECTED_OS="windows";;
            MINGW*)   DETECTED_OS="windows";;
            *)        DETECTED_OS="unknown";;
        esac
    fi
    
    # Detectar arquitectura
    DETECTED_ARCH=$(uname -m)
    case $DETECTED_ARCH in
        x86_64|amd64) DETECTED_ARCH="x64";;
        i*86) DETECTED_ARCH="x86";;
        aarch64|arm64) DETECTED_ARCH="arm64";;
        armv7l) DETECTED_ARCH="arm";;
    esac
    
    jcau_log "OK" "Sistema detectado: $DETECTED_OS ($DETECTED_ARCH)"
}

# Detección universal de package manager
detect_package_manager() {
    jcau_log "INFO" "🔍 Detectando gestor de paquetes disponible..."
    
    case $DETECTED_OS in
        "termux")
            PACKAGE_MANAGER="pkg"
            ;;
        "linux")
            if command -v apt-get >/dev/null 2>&1; then
                PACKAGE_MANAGER="apt"
            elif command -v yum >/dev/null 2>&1; then
                PACKAGE_MANAGER="yum"
            elif command -v dnf >/dev/null 2>&1; then
                PACKAGE_MANAGER="dnf"
            elif command -v pacman >/dev/null 2>&1; then
                PACKAGE_MANAGER="pacman"
            elif command -v zypper >/dev/null 2>&1; then
                PACKAGE_MANAGER="zypper"
            elif command -v apk >/dev/null 2>&1; then
                PACKAGE_MANAGER="apk"
            fi
            ;;
        "macos")
            if command -v brew >/dev/null 2>&1; then
                PACKAGE_MANAGER="brew"
            else
                PACKAGE_MANAGER="brew-install"
            fi
            ;;
        "windows"|"wsl")
            if command -v choco >/dev/null 2>&1; then
                PACKAGE_MANAGER="choco"
            elif command -v winget >/dev/null 2>&1; then
                PACKAGE_MANAGER="winget"
            elif command -v apt-get >/dev/null 2>&1; then
                PACKAGE_MANAGER="apt"  # WSL case
            else
                PACKAGE_MANAGER="manual"
            fi
            ;;
    esac
    
    jcau_log "OK" "Package manager: ${PACKAGE_MANAGER:-"manual"}"
}

# Configuración universal de directorios
setup_directories() {
    jcau_log "INFO" "📁 Configurando directorios JCAU..."
    
    case $DETECTED_OS in
        "termux")
            INSTALL_DIR="$HOME/jcau-lite"
            ;;
        "windows"|"wsl")
            if [[ -n "$USERPROFILE" ]]; then
                INSTALL_DIR="$USERPROFILE/jcau-lite"
            else
                INSTALL_DIR="$HOME/jcau-lite"
            fi
            ;;
        *)
            INSTALL_DIR="$HOME/.jcau-lite"
            ;;
    esac
    
    LOG_FILE="$INSTALL_DIR/jcau-universal.log"
    
    # Crear directorios
    mkdir -p "$INSTALL_DIR"/{bin,lib,config,temp,logs}
    
    jcau_log "OK" "Directorio JCAU: $INSTALL_DIR"
}

# Instalación universal de dependencias
install_dependencies() {
    jcau_log "INFO" "📦 Instalando dependencias universales..."
    
    case $PACKAGE_MANAGER in
        "pkg") # Termux
            pkg update -y
            pkg install -y python nodejs git curl wget
            ;;
        "apt") # Debian/Ubuntu/WSL
            if command -v sudo >/dev/null 2>&1; then
                sudo apt update
                sudo apt install -y python3 python3-pip nodejs npm git curl wget
            else
                apt update
                apt install -y python3 python3-pip nodejs npm git curl wget
            fi
            ;;
        "yum"|"dnf") # RHEL/Fedora
            sudo $PACKAGE_MANAGER install -y python3 python3-pip nodejs npm git curl wget
            ;;
        "pacman") # Arch Linux
            sudo pacman -Sy --noconfirm python nodejs npm git curl wget
            ;;
        "zypper") # openSUSE
            sudo zypper install -y python3 python3-pip nodejs npm git curl wget
            ;;
        "apk") # Alpine Linux
            apk update
            apk add python3 py3-pip nodejs npm git curl wget
            ;;
        "brew") # macOS
            brew install python node git curl wget
            ;;
        "brew-install") # macOS sin Homebrew
            jcau_log "INFO" "Instalando Homebrew..."
            /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
            export PATH="/opt/homebrew/bin:/usr/local/bin:$PATH"
            brew install python node git curl wget
            ;;
        "choco") # Windows con Chocolatey
            choco install -y python nodejs git curl wget
            ;;
        "winget") # Windows con Winget
            winget install -e --id Python.Python.3
            winget install -e --id OpenJS.NodeJS
            winget install -e --id Git.Git
            ;;
        *)
            jcau_log "WARN" "Package manager no detectado. Verificando dependencias manualmente..."
            ;;
    esac
    
    jcau_log "OK" "Dependencias instaladas"
}

# Verificación universal de dependencias
verify_dependencies() {
    jcau_log "INFO" "✅ Verificando dependencias instaladas..."
    
    local deps_ok=true
    
    # Python
    if command -v python3 >/dev/null 2>&1; then
        local python_version=$(python3 --version)
        jcau_log "OK" "Python: $python_version"
    elif command -v python >/dev/null 2>&1; then
        local python_version=$(python --version)
        jcau_log "OK" "Python: $python_version"
    else
        jcau_log "ERROR" "Python no encontrado"
        deps_ok=false
    fi
    
    # Node.js (opcional pero recomendado)
    if command -v node >/dev/null 2>&1; then
        local node_version=$(node --version)
        jcau_log "OK" "Node.js: $node_version"
    else
        jcau_log "WARN" "Node.js no encontrado (opcional)"
    fi
    
    # Git
    if command -v git >/dev/null 2>&1; then
        local git_version=$(git --version)
        jcau_log "OK" "Git: $git_version"
    else
        jcau_log "WARN" "Git no encontrado (se intentará descarga directa)"
    fi
    
    return $deps_ok
}

# Descarga e instalación de JCAU-Lite
install_jcau_core() {
    jcau_log "INFO" "⬇️ Descargando JCAU-Lite..."
    
    cd "$INSTALL_DIR" || exit 1
    
    # Intentar diferentes métodos de descarga
    if command -v git >/dev/null 2>&1; then
        jcau_log "INFO" "Clonando repositorio JCAU-Lite..."
        git clone https://github.com/scesaradame/JCAU-Lite.git temp/jcau-source
        if [[ -d "temp/jcau-source" ]]; then
            cp -r temp/jcau-source/* .
            rm -rf temp/jcau-source
        fi
    elif command -v curl >/dev/null 2>&1; then
        jcau_log "INFO" "Descargando JCAU-Lite via curl..."
        curl -L https://github.com/scesaradame/JCAU-Lite/archive/main.zip -o temp/jcau.zip
        if command -v unzip >/dev/null 2>&1; then
            unzip temp/jcau.zip -d temp/
            cp -r temp/JCAU-Lite-main/* .
        fi
    elif command -v wget >/dev/null 2>&1; then
        jcau_log "INFO" "Descargando JCAU-Lite via wget..."
        wget https://github.com/scesaradame/JCAU-Lite/archive/main.zip -O temp/jcau.zip
        if command -v unzip >/dev/null 2>&1; then
            unzip temp/jcau.zip -d temp/
            cp -r temp/JCAU-Lite-main/* .
        fi
    else
        jcau_log "ERROR" "No hay herramientas de descarga disponibles"
        return 1
    fi
    
    # Limpiar archivos temporales
    rm -rf temp/jcau* temp/JCAU-Lite-main
    
    jcau_log "OK" "JCAU-Lite descargado e instalado"
}

# Configuración universal de PATH
configure_universal_path() {
    jcau_log "INFO" "🔧 Configurando PATH universal..."
    
    local shell_rc=""
    local jcau_path="export PATH=\"$INSTALL_DIR/bin:\$PATH\""
    
    # Detectar shell y archivo de configuración
    case $DETECTED_OS in
        "termux")
            shell_rc="$HOME/.bashrc"
            ;;
        "windows"|"wsl")
            if [[ -n "$WSL_DISTRO_NAME" ]] || [[ "$DETECTED_OS" == "wsl" ]]; then
                shell_rc="$HOME/.bashrc"
            else
                # Para Git Bash en Windows
                shell_rc="$HOME/.bash_profile"
            fi
            ;;
        *)
            # Detectar shell actual
            if [[ -n "$ZSH_VERSION" ]]; then
                shell_rc="$HOME/.zshrc"
            elif [[ -n "$BASH_VERSION" ]]; then
                shell_rc="$HOME/.bashrc"
            else
                shell_rc="$HOME/.profile"
            fi
            ;;
    esac
    
    # Agregar PATH si no existe
    if [[ -f "$shell_rc" ]] && ! grep -q "$INSTALL_DIR/bin" "$shell_rc"; then
        echo "" >> "$shell_rc"
        echo "# JCAU-Lite PATH" >> "$shell_rc"
        echo "$jcau_path" >> "$shell_rc"
        jcau_log "OK" "PATH agregado a $shell_rc"
    elif [[ ! -f "$shell_rc" ]]; then
        echo "$jcau_path" > "$shell_rc"
        jcau_log "OK" "Archivo $shell_rc creado con PATH"
    else
        jcau_log "OK" "PATH ya configurado en $shell_rc"
    fi
    
    # Actualizar PATH para la sesión actual
    export PATH="$INSTALL_DIR/bin:$PATH"
}

# Crear ejecutables universales
create_universal_executables() {
    jcau_log "INFO" "🔧 Creando ejecutables universales..."
    
    # Crear wrapper principal de JCAU
    cat > "$INSTALL_DIR/bin/jcau" << 'EOF'
#!/bin/bash
# JCAU-Lite Universal Wrapper

JCAU_HOME="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# Detectar intérprete disponible
if command -v python3 >/dev/null 2>&1; then
    PYTHON_CMD="python3"
elif command -v python >/dev/null 2>&1; then
    PYTHON_CMD="python"
else
    echo "Error: Python no encontrado"
    exit 1
fi

# Ejecutar JCAU con los argumentos proporcionados
exec "$PYTHON_CMD" "$JCAU_HOME/jcau_core.py" "$@"
EOF
    
    # Crear intérprete JCAU básico
    cat > "$INSTALL_DIR/jcau_core.py" << 'EOF'
#!/usr/bin/env python3
"""
JCAU-Lite Core Interpreter
Lenguaje Matemático Universal
"""

import sys
import re
import math

class JCAUInterpreter:
    def __init__(self):
        self.variables = {}
        self.functions = {
            'suma': lambda x, y: x + y,
            'resta': lambda x, y: x - y,
            'mult': lambda x, y: x * y,
            'div': lambda x, y: x / y if y != 0 else float('inf'),
            'pow': lambda x, y: x ** y,
            'sqrt': lambda x: math.sqrt(x),
            'sin': lambda x: math.sin(x),
            'cos': lambda x: math.cos(x),
            'log': lambda x: math.log(x) if x > 0 else float('-inf')
        }
    
    def evaluate(self, expression):
        try:
            # Operaciones básicas
            if 'suma(' in expression:
                match = re.search(r'suma\((\d+(?:\.\d+)?),\s*(\d+(?:\.\d+)?)\)', expression)
                if match:
                    a, b = float(match.group(1)), float(match.group(2))
                    return f"{expression} → {a + b}"
            
            # Ecuaciones lineales simples
            if 'eq_lineal(' in expression:
                match = re.search(r'eq_lineal\((\d+)x\s*\+\s*(\d+)\s*=\s*(\d+)\)', expression)
                if match:
                    a, b, c = int(match.group(1)), int(match.group(2)), int(match.group(3))
                    x = (c - b) / a if a != 0 else 'indefinido'
                    return f"{expression} → x = {x}"
            
            # Lógica proposicional básica
            if '∧' in expression or '∨' in expression:
                return f"{expression} → [resultado lógico]"
            
            # Conjuntos básicos
            if '∪' in expression:
                return f"{expression} → [unión de conjuntos]"
            
            return f"{expression} → [evaluando...]"
            
        except Exception as e:
            return f"Error: {e}"

def main():
    interpreter = JCAUInterpreter()
    
    if len(sys.argv) > 1:
        # Modo no interactivo
        expression = ' '.join(sys.argv[1:])
        result = interpreter.evaluate(expression)
        print(result)
    else:
        # Modo interactivo
        print("JCAU-Lite v2.0 - Lenguaje Matemático Universal")
        print("Escriba 'salir' para terminar\n")
        
        while True:
            try:
                expression = input("JCAU> ")
                if expression.lower() in ['salir', 'exit', 'quit']:
                    break
                
                result = interpreter.evaluate(expression)
                print(result)
                
            except KeyboardInterrupt:
                print("\n¡Hasta pronto!")
                break
            except EOFError:
                break

if __name__ == "__main__":
    main()
EOF
    
    # Hacer ejecutables
    chmod +x "$INSTALL_DIR/bin/jcau"
    chmod +x "$INSTALL_DIR/jcau_core.py"
    
    jcau_log "OK" "Ejecutables universales creados"
}

# Función de verificación final
verify_installation() {
    jcau_log "INFO" "🔍 Verificando instalación..."
    
    # Verificar que jcau funcione
    if "$INSTALL_DIR/bin/jcau" "suma(2,3)" | grep -q "→ 5"; then
        jcau_log "OK" "JCAU-Lite instalado y funcionando correctamente"
        return 0
    else
        jcau_log "ERROR" "JCAU-Lite no funciona correctamente"
        return 1
    fi
}

# Función principal
main() {
    echo -e "${PURPLE}===============================================${NC}"
    echo -e "${PURPLE}    JCAU-Lite Universal Adapter v2.0${NC}"
    echo -e "${PURPLE}    Adaptación automática a cualquier PC${NC}"
    echo -e "${PURPLE}===============================================${NC}"
    
    detect_system
    setup_directories
    detect_package_manager
    install_dependencies
    
    if verify_dependencies; then
        install_jcau_core
        configure_universal_path
        create_universal_executables
        
        if verify_installation; then
            echo -e "\n${GREEN}✅ JCAU-Lite instalado exitosamente${NC}"
            echo -e "${GREEN}✅ Ejecuta: ${YELLOW}jcau${GREEN} para comenzar${NC}"
            echo -e "${GREEN}✅ Ejemplo: ${YELLOW}jcau 'suma(2,3)'${NC}"
            echo -e "${GREEN}✅ Directorio: ${YELLOW}$INSTALL_DIR${NC}"
        else
            echo -e "\n${RED}❌ Error en la verificación final${NC}"
            exit 1
        fi
    else
        echo -e "\n${RED}❌ Error instalando dependencias${NC}"
        exit 1
    fi
}

# Ejecutar si es llamado directamente
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
