# test_cases_join.py - Testar JOIN de casos
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.main import app
from src.models import db, ClientCases, Services, Users

def test_cases_join():
    with app.app_context():
        print('🔍 Testando JOIN de casos...')
        
        # Fazer o mesmo JOIN que a rota faz
        cases_with_services = db.session.query(ClientCases, Services, Users).join(
            Services, ClientCases.service_id == Services.id, isouter=True
        ).join(
            Users, ClientCases.user_id == Users.id, isouter=True
        ).all()
        
        print(f'📊 Total de casos encontrados: {len(cases_with_services)}')
        
        for case, service, user in cases_with_services:
            print(f'ID: {case.id}')
            print(f'  Título: {case.title}')
            print(f'  Service ID: {case.service_id}')
            print(f'  Service Name: {service.name if service else "NULO"}')
            print(f'  Cliente: {user.name if user else "NULO"}')
            print('---')

if __name__ == "__main__":
    test_cases_join()
