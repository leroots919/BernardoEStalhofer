#!/usr/bin/env python3
"""
Script para testar a rota de usuários diretamente
"""

import requests
import json

# URL base da API
BASE_URL = "http://localhost:5000"

print("🧪 Testando rota de usuários...")

# 1. Primeiro fazer login para obter token
print("\n1️⃣ Fazendo login...")
login_data = {
    "email": "admin@pokeracademy.com",
    "password": "admin123"
}

try:
    login_response = requests.post(f"{BASE_URL}/api/auth/login", json=login_data)
    print(f"Status login: {login_response.status_code}")
    
    if login_response.status_code == 200:
        login_result = login_response.json()
        token = login_result.get("token")
        print(f"✅ Login realizado com sucesso!")
        print(f"Token: {token[:50]}...")
        
        # 2. Testar rota de usuários
        print("\n2️⃣ Testando rota /api/users...")
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        users_response = requests.get(f"{BASE_URL}/api/users", headers=headers)
        print(f"Status usuários: {users_response.status_code}")
        
        if users_response.status_code == 200:
            users_data = users_response.json()
            print(f"✅ Usuários encontrados: {len(users_data)}")
            
            for user in users_data:
                print(f"   - {user.get('id')}: {user.get('name')} ({user.get('email')}) - {user.get('type')}")
        else:
            print(f"❌ Erro na rota de usuários:")
            print(f"Response: {users_response.text}")
            
    else:
        print(f"❌ Erro no login:")
        print(f"Response: {login_response.text}")

except requests.exceptions.ConnectionError:
    print("❌ Erro: Não foi possível conectar ao servidor")
    print("🔧 Verifique se o servidor está rodando em http://localhost:5000")
    
except Exception as e:
    print(f"❌ Erro inesperado: {e}")

print("\n🔧 Para verificar logs do servidor:")
print("   - Olhe no terminal onde executou 'python src\\main.py'")
print("   - Procure por mensagens de erro quando acessar /api/users")
