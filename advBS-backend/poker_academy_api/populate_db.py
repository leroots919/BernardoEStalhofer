# populate_db.py - Script para popular o banco com dados de teste
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.main import app
from src.models import db, Users, Classes, UserType, ClassCategory, VideoType
from src.auth import AuthService
from datetime import datetime, date

def create_test_data():
    with app.app_context():
        # Criar tabelas se não existirem
        db.create_all()
        
        # Verificar se já existem dados
        if Users.query.first():
            print("Dados já existem no banco. Pulando criação...")
            return
        
        print("Criando dados de teste...")
        
        # Criar usuários de teste
        admin_user = Users(
            name="admin",
            email="admin@pokeracademy.com",
            password_hash=AuthService.hash_password("admin123"),
            type=UserType.admin,
            register_date=datetime.utcnow()
        )
        
        student_user = Users(
            name="aluno",
            email="aluno@pokeracademy.com",
            password_hash=AuthService.hash_password("aluno123"),
            type=UserType.student,
            register_date=datetime.utcnow()
        )
        
        student_user2 = Users(
            name="joao",
            email="joao@email.com",
            password_hash=AuthService.hash_password("123456"),
            type=UserType.student,
            register_date=datetime.utcnow()
        )
        
        db.session.add_all([admin_user, student_user, student_user2])
        db.session.commit()
        
        # Criar aulas de teste
        classes_data = [
            {
                "name": "Fundamentos do Pré-Flop",
                "instructor": "Daniel Negreanu",
                "date": date(2024, 1, 15),
                "category": ClassCategory.preflop,
                "video_type": VideoType.youtube,
                "video_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                "priority": 1,
                "views": 150
            },
            {
                "name": "Estratégias Avançadas de Pós-Flop",
                "instructor": "Phil Ivey",
                "date": date(2024, 1, 20),
                "category": ClassCategory.postflop,
                "video_type": VideoType.youtube,
                "video_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                "priority": 2,
                "views": 89
            },
            {
                "name": "Psicologia do Poker",
                "instructor": "Annie Duke",
                "date": date(2024, 1, 25),
                "category": ClassCategory.mental,
                "video_type": VideoType.youtube,
                "video_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                "priority": 3,
                "views": 234
            },
            {
                "name": "Estratégias para Torneios",
                "instructor": "Chris Moneymaker",
                "date": date(2024, 2, 1),
                "category": ClassCategory.torneos,
                "video_type": VideoType.youtube,
                "video_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                "priority": 4,
                "views": 67
            },
            {
                "name": "Cash Game: Gestão de Bankroll",
                "instructor": "Doyle Brunson",
                "date": date(2024, 2, 5),
                "category": ClassCategory.cash,
                "video_type": VideoType.youtube,
                "video_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                "priority": 5,
                "views": 123
            },
            {
                "name": "Leitura de Tells",
                "instructor": "Mike Caro",
                "date": date(2024, 2, 10),
                "category": ClassCategory.mental,
                "video_type": VideoType.youtube,
                "video_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                "priority": 6,
                "views": 98
            },
            {
                "name": "Matemática do Poker",
                "instructor": "Ed Miller",
                "date": date(2024, 2, 15),
                "category": ClassCategory.preflop,
                "video_type": VideoType.youtube,
                "video_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                "priority": 7,
                "views": 176
            },
            {
                "name": "Blefes e Semi-Blefes",
                "instructor": "Tom Dwan",
                "date": date(2024, 2, 20),
                "category": ClassCategory.postflop,
                "video_type": VideoType.youtube,
                "video_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                "priority": 8,
                "views": 145
            }
        ]
        
        for class_data in classes_data:
            new_class = Classes(**class_data)
            db.session.add(new_class)
        
        db.session.commit()
        
        print("Dados de teste criados com sucesso!")
        print("\n=== CREDENCIAIS DE TESTE ===")
        print("ADMIN:")
        print("  Email: admin@pokeracademy.com")
        print("  Senha: admin123")
        print("\nALUNO:")
        print("  Email: aluno@pokeracademy.com")
        print("  Senha: aluno123")
        print("\nALUNO 2:")
        print("  Email: joao@email.com")
        print("  Senha: 123456")
        print("=============================")

if __name__ == "__main__":
    create_test_data()
