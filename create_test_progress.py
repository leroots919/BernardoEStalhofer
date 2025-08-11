#!/usr/bin/env python3
"""
Script para criar dados de teste de progresso para o estudante
"""

import pymysql
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta

# Carregar variáveis de ambiente
load_dotenv()

# Configurações do banco
DB_USERNAME = os.getenv("DB_USERNAME", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", "3306"))
DB_NAME = os.getenv("DB_NAME", "poker_academy")

def create_test_progress():
    try:
        # Conectar ao banco
        connection = pymysql.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USERNAME,
            password=DB_PASSWORD,
            database=DB_NAME,
            charset='utf8mb4'
        )
        
        with connection.cursor() as cursor:
            print("🔍 Buscando usuário estudante...")
            
            # Buscar o usuário estudante
            cursor.execute("SELECT id, name FROM users WHERE type = 'student' LIMIT 1")
            student = cursor.fetchone()
            
            if not student:
                print("❌ Nenhum usuário estudante encontrado!")
                return
            
            student_id, student_name = student
            print(f"✅ Usuário encontrado: {student_name} (ID: {student_id})")
            
            # Buscar aulas disponíveis
            cursor.execute("SELECT id, name FROM classes ORDER BY id LIMIT 5")
            classes = cursor.fetchall()
            
            if not classes:
                print("❌ Nenhuma aula encontrada!")
                return
            
            print(f"📚 Encontradas {len(classes)} aulas")
            
            # Criar dados de progresso de teste
            test_data = [
                (classes[0][0], 75, True, 450.5, datetime.now() - timedelta(hours=2)),  # Aula 1 - 75% assistida
                (classes[1][0], 30, False, 180.0, datetime.now() - timedelta(days=1)),  # Aula 2 - 30% assistida
                (classes[2][0], 100, True, 600.0, datetime.now() - timedelta(days=3)),  # Aula 3 - 100% assistida
                (classes[3][0], 15, False, 90.0, datetime.now() - timedelta(days=7)),   # Aula 4 - 15% assistida
            ]
            
            # Se temos a aula com vídeo (ID 9), adicionar progresso para ela também
            if len(classes) >= 5 or any(c[0] == 9 for c in classes):
                test_data.append((9, 45, False, 270.0, datetime.now() - timedelta(hours=6)))  # Aula com vídeo - 45%
            
            print("➕ Criando dados de progresso...")
            
            for class_id, progress, watched, video_time, last_watched in test_data:
                # Verificar se já existe progresso para esta aula
                cursor.execute("""
                    SELECT user_id FROM user_progress 
                    WHERE user_id = %s AND class_id = %s
                """, (student_id, class_id))
                
                existing = cursor.fetchone()
                
                if existing:
                    # Atualizar progresso existente
                    cursor.execute("""
                        UPDATE user_progress 
                        SET progress = %s, watched = %s, video_time = %s, last_watched = %s
                        WHERE user_id = %s AND class_id = %s
                    """, (progress, watched, video_time, last_watched, student_id, class_id))
                    print(f"   ✏️  Atualizado progresso da aula {class_id}: {progress}%")
                else:
                    # Inserir novo progresso
                    cursor.execute("""
                        INSERT INTO user_progress (user_id, class_id, progress, watched, video_time, last_watched)
                        VALUES (%s, %s, %s, %s, %s, %s)
                    """, (student_id, class_id, progress, watched, video_time, last_watched))
                    print(f"   ➕ Criado progresso da aula {class_id}: {progress}%")
            
            connection.commit()
            print("✅ Dados de progresso criados com sucesso!")
            
            # Mostrar resultado
            print("\n📊 Histórico criado:")
            cursor.execute("""
                SELECT c.name, up.progress, up.watched, up.video_time, up.last_watched
                FROM user_progress up
                JOIN classes c ON up.class_id = c.id
                WHERE up.user_id = %s
                ORDER BY up.last_watched DESC
            """, (student_id,))
            
            history = cursor.fetchall()
            for name, progress, watched, video_time, last_watched in history:
                status = "✅ Assistida" if watched else "⏸️ Em progresso"
                print(f"   📺 {name}: {progress}% ({video_time:.1f}s) - {status}")
                print(f"      Última vez: {last_watched}")
        
        connection.close()
        
    except Exception as e:
        print(f"❌ Erro ao criar dados de teste: {e}")

if __name__ == "__main__":
    create_test_progress()
