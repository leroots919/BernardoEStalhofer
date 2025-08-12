# clean_services.py - Script para limpar serviços duplicados
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.main import app
from src.models import db, Services

def clean_duplicate_services():
    with app.app_context():
        print("🧹 Limpando serviços duplicados...")
        
        # Buscar todos os serviços
        all_services = Services.query.all()
        print(f"📊 Total de serviços antes: {len(all_services)}")
        
        # Agrupar por nome para identificar duplicatas
        services_by_name = {}
        for service in all_services:
            if service.name not in services_by_name:
                services_by_name[service.name] = []
            services_by_name[service.name].append(service)
        
        # Manter apenas o primeiro de cada nome e deletar os duplicados
        services_to_delete = []
        for name, service_list in services_by_name.items():
            if len(service_list) > 1:
                print(f"🔍 Encontradas {len(service_list)} duplicatas de '{name}'")
                # Manter o primeiro (menor ID) e marcar os outros para deleção
                services_to_keep = service_list[0]
                services_to_delete.extend(service_list[1:])
                print(f"   ✅ Mantendo ID {services_to_keep.id}")
                print(f"   ❌ Deletando IDs: {[s.id for s in service_list[1:]]}")
        
        # Deletar os serviços duplicados
        if services_to_delete:
            print(f"\n🗑️ Deletando {len(services_to_delete)} serviços duplicados...")
            for service in services_to_delete:
                db.session.delete(service)
            
            db.session.commit()
            print("✅ Serviços duplicados removidos!")
        else:
            print("✅ Nenhum serviço duplicado encontrado!")
        
        # Verificar resultado final
        final_services = Services.query.all()
        print(f"\n📊 Total de serviços após limpeza: {len(final_services)}")
        
        print("\n=== SERVIÇOS FINAIS ===")
        for service in final_services:
            print(f"ID: {service.id} - {service.name} ({service.category.value})")

if __name__ == "__main__":
    clean_duplicate_services()
