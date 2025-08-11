#!/usr/bin/env python3
"""
Script para verificar aulas no banco MySQL
"""

import pymysql
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Configurações do banco
DB_USERNAME = os.getenv("DB_USERNAME", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", "3306"))
DB_NAME = os.getenv("DB_NAME", "poker_academy")

def check_classes():
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
            print("🔍 Verificando aulas no banco...")
            print("=" * 50)
            
            # Buscar todas as aulas
            cursor.execute("SELECT id, name, instructor, video_path, views FROM classes ORDER BY id")
            classes = cursor.fetchall()
            
            if not classes:
                print("❌ Nenhuma aula encontrada no banco!")
                return
            
            print(f"📚 Encontradas {len(classes)} aulas:")
            print()
            
            for class_data in classes:
                class_id, name, instructor, video_path, views = class_data
                print(f"🎓 ID: {class_id}")
                print(f"   Nome: {name}")
                print(f"   Instrutor: {instructor}")
                print(f"   Vídeo: {video_path or 'Nenhum'}")
                print(f"   Views: {views}")
                
                # Verificar se o arquivo de vídeo existe
                if video_path:
                    video_file_path = os.path.join("poker-academy-backend", "poker_academy_api", "uploads", "videos", video_path)
                    if os.path.exists(video_file_path):
                        file_size = os.path.getsize(video_file_path)
                        print(f"   ✅ Arquivo existe ({file_size / (1024*1024):.1f} MB)")
                    else:
                        print(f"   ❌ Arquivo não encontrado: {video_file_path}")
                else:
                    print(f"   ⚠️  Sem vídeo associado")
                
                print("-" * 30)
        
        connection.close()
        
    except Exception as e:
        print(f"❌ Erro ao conectar ao banco: {e}")

if __name__ == "__main__":
    check_classes()
