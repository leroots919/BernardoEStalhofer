import requests
import json

# Primeiro, fazer login para obter o token
login_url = "http://localhost:5000/api/auth/login"
login_data = {
    "email": "admin@advtransito.com",
    "password": "admin123"
}

print("Fazendo login...")
login_response = requests.post(login_url, json=login_data)
print(f"Status do login: {login_response.status_code}")
print(f"Resposta do login: {login_response.json()}")

if login_response.status_code == 200:
    token = login_response.json()["access_token"]
    print(f"Token obtido: {token[:20]}...")
    
    # Agora testar o upload
    upload_url = "http://localhost:5000/api/admin/process-files"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    # Criar um arquivo de teste
    test_content = "Este é um arquivo de teste para upload"
    files = {
        "file": ("teste.txt", test_content, "text/plain")
    }
    
    data = {
        "client_id": "9",
        "description": "Teste de upload via script"
    }
    
    print("\nTestando upload...")
    upload_response = requests.post(upload_url, headers=headers, files=files, data=data)
    print(f"Status do upload: {upload_response.status_code}")
    print(f"Resposta do upload: {upload_response.text}")
    
    # Verificar se o arquivo foi salvo
    import os
    upload_dir = "poker_academy_api/uploads"
    if os.path.exists(upload_dir):
        print(f"\nArquivos na pasta uploads:")
        for file in os.listdir(upload_dir):
            print(f"  - {file}")
    else:
        print(f"\nPasta uploads não encontrada em: {upload_dir}")
    
else:
    print("Erro no login!")
