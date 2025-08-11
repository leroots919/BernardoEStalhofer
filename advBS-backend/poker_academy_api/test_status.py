#!/usr/bin/env python3
"""Teste para investigar problema do status parado_na_justica"""

import requests

def test_status():
    print('🔍 INVESTIGANDO PROBLEMA DO STATUS')
    print('=' * 50)

    # Login
    login_response = requests.post('http://localhost:8000/api/auth/login', 
                                 json={'email': 'admin', 'password': 'admin123'})
    token = login_response.json()['access_token']
    headers = {'Authorization': f'Bearer {token}'}

    # Buscar casos
    cases_response = requests.get('http://localhost:8000/api/admin/cases', headers=headers)
    cases = cases_response.json()

    print(f'📊 Total de casos: {len(cases)}')
    print('\n📋 STATUS DOS CASOS:')

    # Verificar todos os status únicos
    status_counts = {}
    for case in cases:
        status = case['status']
        status_counts[status] = status_counts.get(status, 0) + 1
        
    for status, count in status_counts.items():
        print(f'  - "{status}": {count} casos')

    # Mostrar alguns exemplos
    print('\n🔍 EXEMPLOS DE CASOS:')
    for i, case in enumerate(cases[:5]):
        print(f'  {i+1}. ID {case["id"]} - Status: "{case["status"]}" - Cliente: {case["client_name"]}')

    # Testar atualização para parado_na_justica
    if len(cases) > 0:
        test_case = cases[0]
        case_id = test_case['id']
        
        print(f'\n🧪 TESTANDO ATUALIZAÇÃO PARA parado_na_justica (Caso ID {case_id}):')
        
        update_response = requests.put(f'http://localhost:8000/api/admin/processes/{case_id}',
                                     json={'description': test_case['description'], 'status': 'parado_na_justica'},
                                     headers=headers)
        
        if update_response.status_code == 200:
            result = update_response.json()
            new_status = result['process']['status']
            print(f'✅ Atualização bem-sucedida! Novo status: "{new_status}"')
            
            # Verificar se foi salvo corretamente
            cases_after = requests.get('http://localhost:8000/api/admin/cases', headers=headers).json()
            updated_case = next((c for c in cases_after if c['id'] == case_id), None)
            if updated_case:
                print(f'✅ Verificação: Status no banco: "{updated_case["status"]}"')
            else:
                print('❌ Caso não encontrado após atualização')
        else:
            print(f'❌ Erro na atualização: {update_response.status_code} - {update_response.text}')

if __name__ == "__main__":
    test_status()
