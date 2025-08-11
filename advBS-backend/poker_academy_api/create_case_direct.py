# create_case_direct.py - Criar caso diretamente no banco
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.main import app
from src.models import db, ClientCases, CaseStatus

def create_case_directly():
    with app.app_context():
        print("🔧 Criando caso diretamente no banco...")
        
        try:
            # Criar novo caso
            new_case = ClientCases(
                user_id=2,  # Cliente Teste
                service_id=1,  # Recurso de Multa
                title="Processo de Suspensão de CNH",
                description="Cliente com CNH suspensa por excesso de pontos. Necessário recurso administrativo.",
                status=CaseStatus.pendente
            )
            
            db.session.add(new_case)
            db.session.commit()
            
            print("✅ Caso criado com sucesso!")
            print(f"   ID: {new_case.id}")
            print(f"   Título: {new_case.title}")
            print(f"   Status: {new_case.status.value}")
            print(f"   Data: {new_case.created_at}")
            
            return new_case.id
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ Erro ao criar caso: {e}")
            import traceback
            traceback.print_exc()
            return None

def list_cases():
    with app.app_context():
        print("\n📋 Casos existentes:")
        cases = ClientCases.query.all()
        
        if not cases:
            print("   Nenhum caso encontrado.")
            return
        
        for case in cases:
            print(f"   ID {case.id}: {case.title} - {case.status.value}")
            print(f"      Cliente: {case.user_id}, Serviço: {case.service_id}")
            print(f"      Criado: {case.created_at}")
            print()

if __name__ == "__main__":
    print("🔍 Listando casos existentes...")
    list_cases()
    
    print("🔧 Criando novo caso...")
    case_id = create_case_directly()
    
    if case_id:
        print("\n🔍 Listagem final...")
        list_cases()
        
        print(f"\n🎉 Caso criado com sucesso! ID: {case_id}")
        print("✅ O sistema de criação de casos funciona!")
        print("❌ O problema está nas rotas da API.")
    else:
        print("\n❌ Falha ao criar caso.")
