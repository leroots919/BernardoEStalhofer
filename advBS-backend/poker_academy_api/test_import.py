#!/usr/bin/env python3
"""
Script para testar imports e identificar problemas
"""

print("🔍 Testando imports...")

try:
    print("1. Testando import do Flask...")
    from flask import Flask
    print("✅ Flask OK")
    
    print("2. Testando import do SQLAlchemy...")
    from flask_sqlalchemy import SQLAlchemy
    print("✅ SQLAlchemy OK")
    
    print("3. Testando import dos modelos...")
    import sys
    import os
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    
    from src.models import db, Classes, Users, VideoType
    print("✅ Modelos OK")
    
    print("4. Testando criação da app...")
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///poker_academy.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'test-key'
    
    db.init_app(app)
    print("✅ App criada OK")
    
    print("5. Testando contexto da app...")
    with app.app_context():
        # Testar query simples
        try:
            classes_count = Classes.query.count()
            print(f"✅ Contexto OK - {classes_count} aulas encontradas")
        except Exception as e:
            print(f"⚠️  Erro na query: {e}")
    
    print("\n🎉 Todos os imports funcionaram!")
    
except Exception as e:
    print(f"❌ Erro: {e}")
    import traceback
    traceback.print_exc()
