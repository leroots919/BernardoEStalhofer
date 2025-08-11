# check_tables.py - Script para verificar e criar tabelas
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.main import app
from src.models import db

def check_and_create_tables():
    with app.app_context():
        print("🔍 Verificando estrutura do banco...")
        
        # Verificar se as tabelas existem
        inspector = db.inspect(db.engine)
        existing_tables = inspector.get_table_names()
        
        print(f"📋 Tabelas existentes: {existing_tables}")
        
        required_tables = ['users', 'services', 'client_cases', 'process_files']
        missing_tables = [table for table in required_tables if table not in existing_tables]
        
        if missing_tables:
            print(f"❌ Tabelas faltando: {missing_tables}")
            print("🔧 Criando tabelas...")
            
            try:
                db.create_all()
                print("✅ Tabelas criadas com sucesso!")
                
                # Verificar novamente
                inspector = db.inspect(db.engine)
                new_tables = inspector.get_table_names()
                print(f"📋 Tabelas após criação: {new_tables}")
                
            except Exception as e:
                print(f"❌ Erro ao criar tabelas: {e}")
                return False
        else:
            print("✅ Todas as tabelas necessárias existem!")
        
        # Verificar estrutura da tabela client_cases
        if 'client_cases' in inspector.get_table_names():
            print("\n🔍 Estrutura da tabela client_cases:")
            columns = inspector.get_columns('client_cases')
            for col in columns:
                print(f"   - {col['name']}: {col['type']}")
        
        return True

if __name__ == "__main__":
    check_and_create_tables()
