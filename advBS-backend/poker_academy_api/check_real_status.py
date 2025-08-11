#!/usr/bin/env python3
"""Verificar os status reais no banco de dados"""

import requests
import json

def check_real_status():
    print('🔍 VERIFICANDO STATUS REAIS NO BANCO')
    print('=' * 50)

    try:
        # Login
        login_response = requests.post('http://localhost:8000/api/auth/login', 
                                     json={'email': 'admin', 'password': 'admin123'})
        
        if login_response.status_code != 200:
            print(f'❌ Erro no login: {login_response.status_code}')
            return
            
        token = login_response.json()['access_token']
        headers = {'Authorization': f'Bearer {token}'}

        # Buscar casos
        cases_response = requests.get('http://localhost:8000/api/admin/cases', headers=headers)
        
        if cases_response.status_code != 200:
            print(f'❌ Erro ao buscar casos: {cases_response.status_code}')
            print(f'Resposta: {cases_response.text}')
            return

        cases = cases_response.json()
        print(f'📊 Total de casos encontrados: {len(cases)}')

        # Analisar status únicos
        status_counts = {}
        print('\n📋 STATUS ENCONTRADOS NO BANCO:')
        
        for case in cases:
            status = case['status']
            status_counts[status] = status_counts.get(status, 0) + 1
            
        for status, count in sorted(status_counts.items()):
            print(f'  - "{status}": {count} casos')

        # Mostrar alguns exemplos
        print('\n🔍 EXEMPLOS DE CASOS:')
        for i, case in enumerate(cases[:3]):
            print(f'  {i+1}. ID {case["id"]} - Status: "{case["status"]}" - Cliente: {case.get("client_name", "N/A")}')

        # Verificar se os status do frontend estão corretos
        frontend_status = ['em_andamento', 'parado_na_justica', 'concluido']
        backend_status = list(status_counts.keys())
        
        print('\n🔄 COMPARAÇÃO:')
        print(f'Frontend espera: {frontend_status}')
        print(f'Backend tem: {backend_status}')
        
        missing_in_backend = [s for s in frontend_status if s not in backend_status]
        missing_in_frontend = [s for s in backend_status if s not in frontend_status]
        
        if missing_in_backend:
            print(f'❌ Status que o frontend espera mas não estão no backend: {missing_in_backend}')
        if missing_in_frontend:
            print(f'⚠️ Status que estão no backend mas o frontend não trata: {missing_in_frontend}')
            
        if not missing_in_backend and not missing_in_frontend:
            print('✅ Status do frontend e backend estão alinhados!')

    except Exception as e:
        print(f'❌ Erro: {e}')
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check_real_status()
