# test_api_cases.py - Testar rota de casos via API
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import requests
import json

def test_cases_api():
    print("🔍 Testando rota /api/admin/cases...")
    
    # URL da API
    url = "http://localhost:5000/api/admin/cases"
    
    # Token de admin (você pode pegar um token válido do localStorage do navegador)
    # Por enquanto vamos testar sem token para ver se a rota responde
    
    try:
        # Primeiro teste sem autenticação para ver o erro
        print("📡 Fazendo requisição sem token...")
        response = requests.get(url)
        print(f"Status: {response.status_code}")
        print(f"Resposta: {response.text[:200]}...")
        
    except Exception as e:
        print(f"❌ Erro na requisição: {e}")

def test_services_api():
    print("\n🔍 Testando rota /api/services...")
    
    # URL da API
    url = "http://localhost:5000/api/services"
    
    try:
        # Teste sem autenticação
        print("📡 Fazendo requisição sem token...")
        response = requests.get(url)
        print(f"Status: {response.status_code}")
        print(f"Resposta: {response.text[:200]}...")
        
    except Exception as e:
        print(f"❌ Erro na requisição: {e}")

if __name__ == "__main__":
    test_cases_api()
    test_services_api()
