import requests

# Login
login_response = requests.post('http://localhost:8000/api/auth/login', json={'email': 'admin', 'password': 'admin123'})
token = login_response.json()['access_token']
headers = {'Authorization': f'Bearer {token}'}

# Buscar casos
cases_response = requests.get('http://localhost:8000/api/admin/cases', headers=headers)
cases = cases_response.json()

print('STATUS REAIS NO BANCO:')
status_counts = {}
for case in cases:
    status = case['status'] or 'vazio'
    status_counts[status] = status_counts.get(status, 0) + 1
    
for status, count in sorted(status_counts.items()):
    print(f'  "{status}": {count} casos')

print('\nPrimeiros 3 casos como exemplo:')
for i, case in enumerate(cases[:3]):
    print(f'  {i+1}. ID {case["id"]} - Status: "{case["status"]}"')
