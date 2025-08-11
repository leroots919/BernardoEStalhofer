#!/usr/bin/env python3
"""
Script para corrigir o banco de dados após remoção do YouTube
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.models import db, Classes, VideoType
from flask import Flask
import sqlite3

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///poker_academy.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'your-secret-key-here'
    
    db.init_app(app)
    return app

def fix_database():
    """Corrige o banco de dados removendo aulas sem vídeo local"""
    app = create_app()
    
    with app.app_context():
        try:
            print("🔧 Iniciando correção do banco de dados...")
            
            # Buscar todas as aulas
            all_classes = Classes.query.all()
            print(f"📊 Total de aulas encontradas: {len(all_classes)}")
            
            # Contar aulas problemáticas
            problematic_classes = []
            for cls in all_classes:
                if not cls.video_path or cls.video_path.strip() == '':
                    problematic_classes.append(cls)
            
            print(f"⚠️  Aulas sem video_path: {len(problematic_classes)}")
            
            if problematic_classes:
                print("\n🗑️  Removendo aulas sem vídeo local:")
                for cls in problematic_classes:
                    print(f"   - ID {cls.id}: {cls.name}")
                    db.session.delete(cls)
                
                db.session.commit()
                print(f"✅ {len(problematic_classes)} aulas removidas com sucesso!")
            
            # Atualizar todas as aulas restantes para video_type = 'local'
            remaining_classes = Classes.query.all()
            updated_count = 0
            
            for cls in remaining_classes:
                if cls.video_type != VideoType.local:
                    cls.video_type = VideoType.local
                    updated_count += 1
            
            if updated_count > 0:
                db.session.commit()
                print(f"✅ {updated_count} aulas atualizadas para tipo 'local'")
            
            print(f"\n📊 Total de aulas válidas: {len(remaining_classes)}")
            print("✅ Banco de dados corrigido com sucesso!")
            
        except Exception as e:
            print(f"❌ Erro ao corrigir banco de dados: {e}")
            db.session.rollback()
            return False
    
    return True

def check_database():
    """Verifica o estado atual do banco de dados"""
    app = create_app()
    
    with app.app_context():
        try:
            print("🔍 Verificando estado do banco de dados...")
            
            # Verificar se a tabela existe
            all_classes = Classes.query.all()
            print(f"📊 Total de aulas: {len(all_classes)}")
            
            # Verificar aulas por tipo
            local_classes = Classes.query.filter_by(video_type=VideoType.local).all()
            print(f"📹 Aulas locais: {len(local_classes)}")
            
            # Verificar aulas sem video_path
            empty_path_classes = Classes.query.filter(
                (Classes.video_path == None) | (Classes.video_path == '')
            ).all()
            print(f"⚠️  Aulas sem video_path: {len(empty_path_classes)}")
            
            if empty_path_classes:
                print("\n📋 Aulas problemáticas:")
                for cls in empty_path_classes:
                    print(f"   - ID {cls.id}: {cls.name} (video_path: '{cls.video_path}')")
            
            return True
            
        except Exception as e:
            print(f"❌ Erro ao verificar banco de dados: {e}")
            return False

if __name__ == "__main__":
    print("🎯 Poker Academy - Correção do Banco de Dados")
    print("=" * 50)
    
    # Verificar estado atual
    if not check_database():
        print("❌ Falha na verificação inicial")
        sys.exit(1)
    
    print("\n" + "=" * 50)
    
    # Perguntar se deve corrigir
    response = input("🤔 Deseja corrigir o banco de dados? (s/N): ").lower().strip()
    
    if response in ['s', 'sim', 'y', 'yes']:
        if fix_database():
            print("\n🎉 Correção concluída com sucesso!")
        else:
            print("\n❌ Falha na correção")
            sys.exit(1)
    else:
        print("\n⏭️  Correção cancelada pelo usuário")
    
    print("\n" + "=" * 50)
    print("✅ Script finalizado")
