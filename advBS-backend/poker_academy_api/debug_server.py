#!/usr/bin/env python3
"""
Script de debug para identificar problemas no servidor
"""

import sys
import os

# Adicionar o diretório atual ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("🔍 Iniciando debug do servidor...")

try:
    print("1. Testando imports básicos...")
    from flask import Flask, jsonify
    from flask_cors import CORS
    print("✅ Imports básicos OK")
    
    print("2. Testando import dos modelos...")
    from src.models import db, Classes, Users
    print("✅ Modelos OK")
    
    print("3. Criando app Flask...")
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = "test-key"
    
    CORS(app)
    db.init_app(app)
    print("✅ App criada OK")
    
    print("4. Testando rota simples...")
    @app.route("/test")
    def test():
        return jsonify({"status": "OK", "message": "Funcionando!"})
    
    print("5. Testando contexto do banco...")
    with app.app_context():
        db.create_all()
        classes_count = Classes.query.count()
        print(f"✅ Banco OK - {classes_count} aulas")
    
    print("6. Iniciando servidor de teste...")
    print("🌐 Acesse: http://localhost:5001/test")
    app.run(host="0.0.0.0", port=5001, debug=False)
    
except Exception as e:
    print(f"❌ Erro: {e}")
    import traceback
    traceback.print_exc()
