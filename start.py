#!/usr/bin/env python3
"""
Script de inicialização para Railway
"""
import os
import sys
import subprocess

def main():
    print("🚀 Iniciando aplicação Bernardo & Stahlhöfer...")
    
    # Verificar se estamos no Railway
    is_railway = os.getenv("RAILWAY_ENVIRONMENT") is not None
    
    if is_railway:
        print("🌐 Ambiente: Railway (Produção)")
    else:
        print("💻 Ambiente: Local (Desenvolvimento)")
    
    # Navegar para o diretório do backend
    backend_dir = os.path.join(os.path.dirname(__file__), "advBS-backend")
    os.chdir(backend_dir)
    
    print(f"📁 Diretório atual: {os.getcwd()}")
    
    # Executar o servidor
    try:
        subprocess.run([sys.executable, "simple_server.py"], check=True)
    except KeyboardInterrupt:
        print("\n👋 Aplicação encerrada pelo usuário")
    except Exception as e:
        print(f"❌ Erro ao iniciar aplicação: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
