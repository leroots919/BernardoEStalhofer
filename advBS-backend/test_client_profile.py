import requests
import json

# Fazer login como cliente vanessa
login_url = "http://localhost:5000/api/auth/login"
login_data = {
    "email": "vanessafk007@gmail.com",
    "password": "123456"
}

print("🔐 Fazendo login como cliente vanessa...")
login_response = requests.post(login_url, json=login_data)
print(f"Status do login: {login_response.status_code}")

if login_response.status_code == 200:
    login_result = login_response.json()
    token = login_result["access_token"]
    user_info = login_result.get("user", {})
    
    print(f"✅ Login bem-sucedido!")
    print(f"   Token: {token[:20]}...")
    print(f"   Usuário: {user_info.get('name')} ({user_info.get('email')})")
    print(f"   Tipo: {user_info.get('type')}")
    
    # Testar busca do perfil
    profile_url = "http://localhost:5000/api/client/profile"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    print(f"\n📋 Buscando perfil do cliente...")
    profile_response = requests.get(profile_url, headers=headers)
    print(f"Status da busca do perfil: {profile_response.status_code}")
    
    if profile_response.status_code == 200:
        profile_data = profile_response.json()
        print(f"✅ Perfil carregado com sucesso!")
        print(f"   Nome: {profile_data.get('name')}")
        print(f"   Email: {profile_data.get('email')}")
        print(f"   CPF: {profile_data.get('cpf')}")
        print(f"   Telefone: {profile_data.get('phone')}")
        print(f"   Endereço: {profile_data.get('address')}")
        print(f"   Cidade: {profile_data.get('city')}")
        print(f"   Estado: {profile_data.get('state')}")
        print(f"   CEP: {profile_data.get('zip_code')}")
        print(f"   Cadastro: {profile_data.get('register_date')}")
        
        # Testar atualização do perfil
        print(f"\n🔄 Testando atualização do perfil...")
        update_data = {
            "name": profile_data.get('name', 'vanessa'),
            "phone": "51999887766",
            "address": "Rua Teste, 123",
            "city": "Porto Alegre",
            "state": "RS",
            "zip_code": "90000-000"
        }
        
        update_response = requests.put(profile_url, json=update_data, headers=headers)
        print(f"Status da atualização: {update_response.status_code}")
        
        if update_response.status_code == 200:
            print(f"✅ Perfil atualizado com sucesso!")
            update_result = update_response.json()
            print(f"   Mensagem: {update_result.get('message')}")
        else:
            print(f"❌ Erro na atualização: {update_response.text}")
        
    else:
        print(f"❌ Erro ao buscar perfil: {profile_response.text}")
        
else:
    print(f"❌ Erro no login: {login_response.text}")
