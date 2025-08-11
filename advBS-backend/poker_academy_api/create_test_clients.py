#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from database import get_db_session
from models import Users, UserType, ClientCases, CaseStatus
from werkzeug.security import generate_password_hash
from datetime import datetime

def create_test_clients():
    """Criar clientes de teste para o sistema"""
    print("🚀 Criando clientes de teste...")
    
    # Conectar ao banco
    db_session = get_db_session()
    
    try:
        # Verificar se já existem clientes
        existing_clients = db_session.query(Users).filter(Users.type == UserType.cliente).count()
        print(f"📊 Clientes existentes: {existing_clients}")
        
        if existing_clients > 0:
            print("✅ Já existem clientes no sistema!")
            return
        
        # Criar clientes de teste
        test_clients = [
            {
                "name": "João Silva",
                "email": "joao.silva@email.com",
                "phone": "(51) 99999-1111",
                "cpf": "123.456.789-01",
                "address": "Rua das Flores, 123 - Centro - Porto Alegre/RS"
            },
            {
                "name": "Maria Santos",
                "email": "maria.santos@email.com", 
                "phone": "(51) 99999-2222",
                "cpf": "987.654.321-02",
                "address": "Av. Brasil, 456 - Cidade Baixa - Porto Alegre/RS"
            },
            {
                "name": "Pedro Oliveira",
                "email": "pedro.oliveira@email.com",
                "phone": "(51) 99999-3333", 
                "cpf": "456.789.123-03",
                "address": "Rua da Praia, 789 - Centro - Porto Alegre/RS"
            },
            {
                "name": "Ana Costa",
                "email": "ana.costa@email.com",
                "phone": "(51) 99999-4444",
                "cpf": "789.123.456-04", 
                "address": "Rua Voluntários da Pátria, 321 - Santana - Porto Alegre/RS"
            },
            {
                "name": "Carlos Ferreira",
                "email": "carlos.ferreira@email.com",
                "phone": "(51) 99999-5555",
                "cpf": "321.654.987-05",
                "address": "Av. Ipiranga, 654 - Azenha - Porto Alegre/RS"
            }
        ]
        
        created_clients = []
        
        for client_data in test_clients:
            # Verificar se email já existe
            existing = db_session.query(Users).filter(Users.email == client_data["email"]).first()
            if existing:
                print(f"⚠️ Cliente {client_data['email']} já existe")
                continue
                
            # Criar cliente
            client = Users(
                name=client_data["name"],
                email=client_data["email"],
                phone=client_data["phone"],
                cpf=client_data["cpf"],
                address=client_data["address"],
                type=UserType.cliente,
                password_hash=generate_password_hash("cliente123"),  # Senha padrão
                register_date=datetime.now()
            )
            
            db_session.add(client)
            db_session.flush()  # Para obter o ID
            created_clients.append(client)
            
            print(f"✅ Cliente criado: {client.name} (ID: {client.id})")
        
        # Criar alguns casos de teste
        test_cases = [
            {
                "title": "Recurso de Multa por Velocidade",
                "description": "Contestação de multa por excesso de velocidade na BR-116",
                "status": CaseStatus.em_andamento
            },
            {
                "title": "Defesa CNH - Suspensão",
                "description": "Defesa contra suspensão da CNH por pontuação",
                "status": CaseStatus.pendente
            },
            {
                "title": "Recurso Multa Estacionamento",
                "description": "Contestação de multa por estacionamento irregular",
                "status": CaseStatus.concluido
            }
        ]
        
        # Criar casos para alguns clientes
        for i, client in enumerate(created_clients[:3]):  # Apenas para os 3 primeiros
            case_data = test_cases[i]
            
            case = ClientCases(
                user_id=client.id,
                title=case_data["title"],
                description=case_data["description"],
                status=case_data["status"],
                service_id=1,  # ID padrão
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
            
            db_session.add(case)
            print(f"✅ Caso criado: {case.title} para {client.name}")
        
        # Salvar tudo
        db_session.commit()
        print(f"🎉 Criados {len(created_clients)} clientes e {len(test_cases)} casos de teste!")
        
    except Exception as e:
        db_session.rollback()
        print(f"❌ Erro ao criar clientes de teste: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db_session.close()

if __name__ == "__main__":
    create_test_clients()
