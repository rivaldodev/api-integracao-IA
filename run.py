#!/usr/bin/env python3
"""
Script para inicializar e executar a API de Análise de Texto
"""

import os
import sys
import subprocess
from pathlib import Path

def check_requirements():
    """Verifica se os requirements estão instalados"""
    try:
        import fastapi
        import uvicorn
        import google.generativeai
        return True
    except ImportError:
        return False

def install_requirements():
    """Instala os requirements"""
    print("Instalando dependências...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])

def check_env_file():
    """Verifica se o arquivo .env existe"""
    env_file = Path(".env")
    if not env_file.exists():
        print("Arquivo .env não encontrado.")
        print("Copie o arquivo .env.example para .env e configure sua API key do Gemini:")
        print("cp .env.example .env")
        return False
    return True

def main():
    """Função principal"""
    print("🚀 Iniciando API de Análise de Texto")
    print("=" * 50)
    
    # Verifica requirements
    if not check_requirements():
        print("📦 Instalando dependências...")
        install_requirements()
    
    # Verifica arquivo .env
    if not check_env_file():
        print("⚠️  Configure o arquivo .env antes de continuar.")
        return
    
    # Carrega variáveis de ambiente
    from dotenv import load_dotenv
    load_dotenv()
      # Inicia a aplicação    print("🌐 Iniciando servidor...")
    print("📍 Acesse: http://localhost:3000")
    print("📖 Documentação: http://localhost:3000/docs")
    print("=" * 50)
    
    import uvicorn
    uvicorn.run(
        "main:app",
        host=os.getenv("APP_HOST", "0.0.0.0"),
        port=int(os.getenv("APP_PORT", 3000)),
        reload=os.getenv("APP_DEBUG", "False").lower() == "true"
    )

if __name__ == "__main__":
    main()
