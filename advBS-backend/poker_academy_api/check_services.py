# check_services.py - Script para verificar serviços existentes
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.main import app
from src.models import db, Services, ServiceCategory

def check_existing_services():
    with app.app_context():
        print("=== SERVIÇOS EXISTENTES NO BANCO ===")
        services = Services.query.all()
        
        if not services:
            print("Nenhum serviço encontrado no banco.")
            return False
        
        for service in services:
            print(f"ID: {service.id}")
            print(f"Nome: {service.name}")
            print(f"Categoria: {service.category.value}")
            print(f"Preço: {service.price}")
            print(f"Ativo: {service.active}")
            print("-" * 30)
        
        print(f"\nTotal de serviços: {len(services)}")
        return True

def create_test_services():
    with app.app_context():
        # Verificar se já existem serviços
        if Services.query.count() > 0:
            print("Serviços já existem!")
            return
        
        # Criar serviços de teste
        services_data = [
            {
                "name": "Defesa de Multa de Trânsito",
                "description": "Recurso contra multas de trânsito",
                "category": ServiceCategory.multas,
                "price": 150.00,
                "duration_days": 30
            },
            {
                "name": "Recuperação de CNH Suspensa",
                "description": "Processo para recuperar CNH suspensa",
                "category": ServiceCategory.cnh,
                "price": 300.00,
                "duration_days": 60
            },
            {
                "name": "Consultoria Jurídica",
                "description": "Consultoria especializada em direito de trânsito",
                "category": ServiceCategory.consultoria,
                "price": 100.00,
                "duration_days": 1
            }
        ]
        
        for service_data in services_data:
            service = Services(**service_data)
            db.session.add(service)
        
        db.session.commit()
        print("Serviços de teste criados com sucesso!")

if __name__ == "__main__":
    print("🔍 Verificando serviços...")
    has_services = check_existing_services()
    
    if not has_services:
        print("\n🔧 Criando serviços de teste...")
        create_test_services()
        
        print("\n🔍 Verificação final...")
        check_existing_services()
