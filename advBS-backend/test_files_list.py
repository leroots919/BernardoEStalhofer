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

if login_response.status_code == 200:
    token = login_response.json()["access_token"]
    print(f"Token obtido: {token[:20]}...")
    
    # Agora testar a listagem de arquivos
    files_url = "http://localhost:5000/api/admin/process-files"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    print("\nTestando listagem de arquivos...")
    files_response = requests.get(files_url, headers=headers)
    print(f"Status da listagem: {files_response.status_code}")
    print(f"Resposta da listagem: {files_response.text}")
    
    if files_response.status_code == 200:
        files_data = files_response.json()
        print(f"\nEncontrados {len(files_data)} arquivos:")
        for file in files_data:
            print(f"  - ID: {file.get('id')}")
            print(f"    Nome: {file.get('original_filename')}")
            print(f"    Cliente: {file.get('client_name')}")
            print(f"    Data: {file.get('created_at')}")
            print("    ---")
    
else:
    print("Erro no login!")
