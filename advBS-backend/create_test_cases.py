#!/usr/bin/env python3
"""
Script para criar casos de teste para o cliente vanessa
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'poker_academy_api', 'src'))

from poker_academy_api.src.models import db, Users, ClientCases, CaseStatus, Services
from poker_academy_api.src.database import get_db_session
from datetime import datetime

def create_test_cases():
    """Criar casos de teste para o cliente vanessa"""
    
    # Obter sessão do banco
    session = get_db_session()
    
    try:
        print("🔧 Criando casos de teste para vanessa...")
        
        # Buscar o cliente vanessa (ID: 9)
        vanessa = session.query(Users).filter(Users.id == 9).first()
        if not vanessa:
            print("❌ Cliente vanessa não encontrado!")
            return
        
        print(f"✅ Cliente encontrado: {vanessa.name} ({vanessa.email})")
        
        # Verificar se já existem casos
        existing_cases = session.query(ClientCases).filter(ClientCases.user_id == 9).count()
        print(f"📊 Casos existentes: {existing_cases}")
        
        # Criar casos de teste
        test_cases = [
            {
                "title": "Recurso de Multa por Excesso de Velocidade",
                "description": "Contestação de multa por excesso de velocidade na BR-116. Cliente alega que o radar estava mal calibrado.",
                "status": CaseStatus.em_andamento,
                "service_id": 1
            },
            {
                "title": "Suspensão de CNH - Pontuação",
                "description": "Processo administrativo para evitar suspensão da CNH por acúmulo de pontos. Análise de recursos cabíveis.",
                "status": CaseStatus.pendente,
                "service_id": 2
            },
            {
                "title": "Recurso de Multa por Estacionamento",
                "description": "Contestação de multa por estacionamento irregular. Cliente possui comprovante de pagamento do estacionamento.",
                "status": CaseStatus.arquivado,
                "service_id": 1
            },
            {
                "title": "Renovação de CNH Vencida",
                "description": "Processo concluído para renovação de CNH vencida há mais de 5 anos. Documentação regularizada.",
                "status": CaseStatus.concluido,
                "service_id": 2
            }
        ]
        
        # Adicionar casos se não existirem muitos
        if existing_cases < 3:
            for case_data in test_cases:
                new_case = ClientCases(
                    user_id=9,  # ID da vanessa
                    service_id=case_data["service_id"],
                    title=case_data["title"],
                    description=case_data["description"],
                    status=case_data["status"]
                )
                
                session.add(new_case)
                print(f"✅ Caso criado: {case_data['title']}")
            
            session.commit()
            print("🎉 Todos os casos foram criados com sucesso!")
        else:
            print("ℹ️ Casos já existem, não criando novos.")
        
        # Verificar casos criados
        final_cases = session.query(ClientCases).filter(ClientCases.user_id == 9).all()
        print(f"\n📋 Total de casos para vanessa: {len(final_cases)}")
        
        for case in final_cases:
            print(f"   - {case.title} ({case.status.value})")
            
    except Exception as e:
        session.rollback()
        print(f"❌ Erro ao criar casos: {e}")
        import traceback
        traceback.print_exc()
    finally:
        session.close()

if __name__ == "__main__":
    create_test_cases()
