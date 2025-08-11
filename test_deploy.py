#!/usr/bin/env python3
"""
Script de teste para verificar se o deploy está funcionando
"""
import requests
import sys
import os

def test_local():
    """Testar servidor local"""
    print("🧪 Testando servidor local...")
    
    try:
        response = requests.get("http://localhost:5000/api/health", timeout=5)
        if response.status_code == 200:
            print("✅ Servidor local funcionando!")
            print(f"📄 Resposta: {response.json()}")
            return True
        else:
            print(f"❌ Servidor local retornou status {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Erro ao conectar com servidor local: {e}")
        return False

def test_production(url):
    """Testar servidor em produção"""
    print(f"🌐 Testando servidor em produção: {url}")
    
    try:
        response = requests.get(f"{url}/api/health", timeout=10)
        if response.status_code == 200:
            print("✅ Servidor em produção funcionando!")
            print(f"📄 Resposta: {response.json()}")
            return True
        else:
            print(f"❌ Servidor em produção retornou status {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Erro ao conectar com servidor em produção: {e}")
        return False

def main():
    print("🚀 Teste de Deploy - Bernardo & Stahlhöfer")
    print("=" * 50)
    
    # Testar local
    local_ok = test_local()
    
    # Testar produção se URL fornecida
    production_url = os.getenv("PRODUCTION_URL")
    if production_url:
        production_ok = test_production(production_url)
    else:
        print("ℹ️  URL de produção não fornecida (defina PRODUCTION_URL)")
        production_ok = None
    
    print("\n📊 Resumo dos Testes:")
    print(f"🏠 Local: {'✅ OK' if local_ok else '❌ FALHOU'}")
    if production_ok is not None:
        print(f"🌐 Produção: {'✅ OK' if production_ok else '❌ FALHOU'}")
    
    if not local_ok:
        print("\n💡 Para testar local, execute: python advBS-backend/simple_server.py")
    
    if production_ok is False:
        print("\n💡 Verifique os logs do Railway: railway logs")

if __name__ == "__main__":
    main()
