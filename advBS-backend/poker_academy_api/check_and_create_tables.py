#!/usr/bin/env python3
"""
Script para verificar e criar tabelas necessárias na base BS
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.main import app
from src.models import db, Users, ClientCases, Services, ProcessFiles
import pymysql

def check_and_create_tables():
    """Verificar e criar tabelas necessárias"""
    
    print("🔧 Verificando e criando tabelas na base BS...")
    
    try:
        with app.app_context():
            # Verificar conexão
            print("📡 Testando conexão com a base de dados...")
            db.engine.execute("SELECT 1")
            print("✅ Conexão OK")
            
            # Criar todas as tabelas
            print("🏗️  Criando tabelas...")
            db.create_all()
            print("✅ Tabelas criadas/verificadas")
            
            # Verificar se existem dados
            print("\n📊 Verificando dados existentes:")
            
            users_count = Users.query.count()
            print(f"   👥 Usuários: {users_count}")
            
            cases_count = ClientCases.query.count()
            print(f"   📋 Casos: {cases_count}")
            
            services_count = Services.query.count()
            print(f"   🔧 Serviços: {services_count}")
            
            files_count = ProcessFiles.query.count()
            print(f"   📁 Arquivos: {files_count}")
            
            # Se não há serviços, criar alguns básicos
            if services_count == 0:
                print("\n🔧 Criando serviços básicos...")
                
                basic_services = [
                    {
                        'name': 'Recurso de Multa',
                        'description': 'Recurso administrativo contra multas de trânsito',
                        'category': 'multas',
                        'price': 150.00,
                        'duration_days': 30
                    },
                    {
                        'name': 'Suspensão de CNH',
                        'description': 'Defesa em processo de suspensão de CNH',
                        'category': 'cnh',
                        'price': 300.00,
                        'duration_days': 60
                    },
                    {
                        'name': 'Cassação de CNH',
                        'description': 'Defesa em processo de cassação de CNH',
                        'category': 'cnh',
                        'price': 500.00,
                        'duration_days': 90
                    }
                ]
                
                for service_data in basic_services:
                    service = Services(**service_data)
                    db.session.add(service)
                
                db.session.commit()
                print("✅ Serviços básicos criados")
            
            print("\n🎉 Verificação concluída com sucesso!")
            
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check_and_create_tables()
