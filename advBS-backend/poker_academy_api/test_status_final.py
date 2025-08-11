#!/usr/bin/env python3
"""Teste final para verificar se o status parado_na_justica está funcionando"""

import requests

def test_status_final():
    print('🧪 TESTE FINAL DO STATUS "parado_na_justica"')
    print('=' * 60)

    try:
        # Login
        login_response = requests.post('http://localhost:8000/api/auth/login', 
                                     json={'email': 'admin', 'password': 'admin123'})
        token = login_response.json()['access_token']
        headers = {'Authorization': f'Bearer {token}'}

        # Buscar casos
        cases_response = requests.get('http://localhost:8000/api/admin/cases', headers=headers)
        cases = cases_response.json()

        print(f'📊 Total de casos: {len(cases)}')
        print('\n📋 STATUS ÚNICOS ENCONTRADOS:')

        # Verificar todos os status únicos
        status_counts = {}
        for case in cases:
            status = case['status']
            status_counts[status] = status_counts.get(status, 0) + 1
            
        for status, count in status_counts.items():
            print(f'  - "{status}": {count} casos')

        # Testar atualização para parado_na_justica
        if len(cases) > 0:
            test_case = cases[0]
            case_id = test_case['id']
            original_status = test_case['status']
            
            print(f'\n🧪 TESTE DE ATUALIZAÇÃO:')
            print(f'   Caso ID: {case_id}')
            print(f'   Status original: "{original_status}"')
            
            # Atualizar para parado_na_justica
            print('   Atualizando para "parado_na_justica"...')
            update_response = requests.put(f'http://localhost:8000/api/admin/processes/{case_id}',
                                         json={'description': test_case['description'], 'status': 'parado_na_justica'},
                                         headers=headers)
            
            if update_response.status_code == 200:
                result = update_response.json()
                new_status = result['process']['status']
                print(f'   ✅ Atualização bem-sucedida! Novo status: "{new_status}"')
                
                # Verificar se foi salvo corretamente
                cases_after = requests.get('http://localhost:8000/api/admin/cases', headers=headers).json()
                updated_case = next((c for c in cases_after if c['id'] == case_id), None)
                if updated_case:
                    final_status = updated_case['status']
                    print(f'   ✅ Verificação no banco: "{final_status}"')
                    
                    if final_status == 'parado_na_justica':
                        print('\n🎉 SUCESSO! Status "parado_na_justica" funcionando corretamente!')
                        print('✅ Backend: Enum atualizado com parado_na_justica')
                        print('✅ API: PUT /api/admin/processes/{id} funcionando')
                        print('✅ Banco: Status salvo corretamente')
                        print('✅ Frontend: Deve exibir "Parado na Justiça" na tabela')
                    else:
                        print(f'❌ PROBLEMA: Status esperado "parado_na_justica", mas encontrado "{final_status}"')
                else:
                    print('❌ Caso não encontrado após atualização')
            else:
                print(f'❌ Erro na atualização: {update_response.status_code} - {update_response.text}')
        else:
            print('❌ Nenhum caso encontrado para testar')

    except Exception as e:
        print(f'❌ Erro durante o teste: {e}')

if __name__ == "__main__":
    test_status_final()
