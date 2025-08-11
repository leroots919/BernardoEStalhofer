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
    
    # Primeiro listar arquivos para pegar um ID
    files_url = "http://localhost:5000/api/admin/process-files"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    print("\nListando arquivos...")
    files_response = requests.get(files_url, headers=headers)
    
    if files_response.status_code == 200:
        files_data = files_response.json()
        if files_data:
            file_id = files_data[0]["id"]
            original_filename = files_data[0]["original_filename"]
            print(f"Testando download do arquivo ID: {file_id} ({original_filename})")
            
            # Testar download
            download_url = f"http://localhost:5000/api/admin/process-files/{file_id}/download"
            download_response = requests.get(download_url, headers=headers)
            
            print(f"Status do download: {download_response.status_code}")
            
            if download_response.status_code == 200:
                # Salvar arquivo baixado
                with open(f"downloaded_{original_filename}", "wb") as f:
                    f.write(download_response.content)
                print(f"✅ Arquivo baixado com sucesso: downloaded_{original_filename}")
                print(f"Tamanho: {len(download_response.content)} bytes")
            else:
                print(f"❌ Erro no download: {download_response.text}")
        else:
            print("❌ Nenhum arquivo encontrado para testar download")
    else:
        print(f"❌ Erro ao listar arquivos: {files_response.text}")
        
else:
    print("Erro no login!")
