#!/usr/bin/env python3
"""
Script para criar casos de teste diretamente na base de dados
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.main import app
from src.models import db, Users, ClientCases, Services, CaseStatus
from datetime import datetime

def create_test_cases():
    """Criar casos de teste"""
    
    print("🔧 Criando casos de teste...")
    
    try:
        with app.app_context():
            # Verificar se há clientes
            clients = Users.query.filter_by(type='cliente').all()
            if not clients:
                print("❌ Nenhum cliente encontrado!")
                return
            
            client = clients[0]
            print(f"👤 Cliente encontrado: {client.name} (ID: {client.id})")
            
            # Verificar se há serviços
            services = Services.query.all()
            if not services:
                print("❌ Nenhum serviço encontrado!")
                return
            
            service = services[0]
            print(f"🔧 Serviço encontrado: {service.name} (ID: {service.id})")
            
            # Criar casos de teste
            test_cases = [
                {
                    'user_id': client.id,
                    'service_id': service.id,
                    'title': 'Recurso de Multa por Velocidade',
                    'description': 'Cliente recebeu multa por excesso de velocidade na BR-116. Solicitando recurso administrativo.',
                    'status': CaseStatus.em_andamento
                },
                {
                    'user_id': client.id,
                    'service_id': service.id,
                    'title': 'Defesa de Suspensão de CNH',
                    'description': 'Cliente está com processo de suspensão de CNH por pontuação. Preparando defesa.',
                    'status': CaseStatus.pendente
                },
                {
                    'user_id': client.id,
                    'service_id': service.id,
                    'title': 'Recurso de Multa por Estacionamento',
                    'description': 'Multa por estacionamento em local proibido. Caso já finalizado com sucesso.',
                    'status': CaseStatus.concluido
                }
            ]
            
            for case_data in test_cases:
                # Verificar se já existe
                existing = ClientCases.query.filter_by(
                    user_id=case_data['user_id'],
                    title=case_data['title']
                ).first()
                
                if not existing:
                    case = ClientCases(**case_data)
                    db.session.add(case)
                    print(f"✅ Caso criado: {case_data['title']}")
                else:
                    print(f"⚠️  Caso já existe: {case_data['title']}")
            
            db.session.commit()
            
            # Verificar resultados
            total_cases = ClientCases.query.count()
            print(f"\n📊 Total de casos na base: {total_cases}")
            
            print("\n🎉 Casos de teste criados com sucesso!")
            
    except Exception as e:
        db.session.rollback()
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    create_test_cases()
