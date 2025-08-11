import requests
import json

# Testar login direto
login_url = "http://localhost:5000/api/auth/login"
login_data = {
    "email": "vanessafk007@gmail.com",
    "password": "123456"
}

print("🔐 Testando login direto...")
print(f"URL: {login_url}")
print(f"Dados: {login_data}")

try:
    # Fazer requisição com headers explícitos
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Origin': 'http://localhost:3000',
        'Access-Control-Request-Method': 'POST',
        'Access-Control-Request-Headers': 'Content-Type'
    }
    
    # Primeiro fazer OPTIONS (preflight)
    print("\n🔍 Fazendo requisição OPTIONS (preflight)...")
    options_response = requests.options(login_url, headers=headers)
    print(f"Status OPTIONS: {options_response.status_code}")
    print(f"Headers OPTIONS: {dict(options_response.headers)}")
    
    # Agora fazer POST
    print("\n🔍 Fazendo requisição POST...")
    response = requests.post(login_url, json=login_data, headers=headers)
    print(f"Status: {response.status_code}")
    print(f"Headers: {dict(response.headers)}")
    print(f"Resposta: {response.text}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Login bem-sucedido!")
        print(f"Token: {data.get('access_token', 'N/A')[:20]}...")
        print(f"Usuário: {data.get('user', {})}")
    else:
        print(f"❌ Erro no login: {response.status_code}")
        
except Exception as e:
    print(f"❌ Erro na requisição: {e}")
    import traceback
    traceback.print_exc()
