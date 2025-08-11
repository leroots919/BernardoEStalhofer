#!/usr/bin/env python3
"""
Script para verificar e corrigir a tabela process_files
"""

import sys
import os

# Adicionar o diretório src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.models import db, ProcessFiles, ClientCases, Users
from src.main import app
from sqlalchemy import text

def check_and_fix_process_files():
    with app.app_context():
        try:
            print("🔍 Verificando tabela process_files...")
            
            # Tentar fazer uma query simples
            try:
                count = ProcessFiles.query.count()
                print(f"✅ Tabela process_files existe! Total de arquivos: {count}")
                
                if count > 0:
                    files = ProcessFiles.query.limit(3).all()
                    print("📁 Primeiros arquivos:")
                    for file in files:
                        print(f"   - ID: {file.id} | {file.original_filename} | User: {file.user_id} | Case: {file.case_id}")
                else:
                    print("⚠️ Tabela existe mas está vazia")
                    
            except Exception as e:
                print(f"❌ Erro ao acessar tabela process_files: {e}")
                print("🔧 Tentando criar a tabela...")
                
                # Criar todas as tabelas
                db.create_all()
                print("✅ Tabelas criadas!")
                
                # Verificar novamente
                count = ProcessFiles.query.count()
                print(f"📊 Total de arquivos após criação: {count}")
            
            # Verificar casos da Vanessa
            print("\n🔍 Verificando casos da Vanessa (ID: 9)...")
            vanessa_cases = ClientCases.query.filter_by(user_id=9).all()
            print(f"📋 Casos da Vanessa: {len(vanessa_cases)}")
            
            for case in vanessa_cases:
                print(f"   - Caso ID: {case.id} | {case.title}")
                case_files = ProcessFiles.query.filter_by(user_id=9, case_id=case.id).all()
                print(f"     📁 Arquivos: {len(case_files)}")
                for file in case_files:
                    print(f"       - {file.original_filename}")
                    
        except Exception as e:
            print(f"❌ Erro geral: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    check_and_fix_process_files()
