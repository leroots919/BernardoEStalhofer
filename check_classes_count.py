#!/usr/bin/env python3
"""
Script para verificar a diferença entre total de aulas e aulas exibidas
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
            print("🔍 INVESTIGANDO AULAS NO BANCO DE DADOS\n")
            
            # Total de aulas
            cursor.execute("SELECT COUNT(*) FROM classes")
            total_classes = cursor.fetchone()[0]
            print(f"📊 Total de aulas no banco: {total_classes}")
            
            # Aulas com vídeo
            cursor.execute("SELECT COUNT(*) FROM classes WHERE video_path IS NOT NULL AND video_path != ''")
            classes_with_video = cursor.fetchone()[0]
            print(f"🎥 Aulas com vídeo: {classes_with_video}")
            
            # Aulas sem vídeo
            cursor.execute("SELECT COUNT(*) FROM classes WHERE video_path IS NULL OR video_path = ''")
            classes_without_video = cursor.fetchone()[0]
            print(f"📝 Aulas sem vídeo: {classes_without_video}")
            
            print("\n" + "="*50)
            print("📋 LISTA COMPLETA DE AULAS:")
            print("="*50)
            
            # Listar todas as aulas
            cursor.execute("""
                SELECT id, name, instructor, category, video_path, views, created_at
                FROM classes 
                ORDER BY id
            """)
            
            all_classes = cursor.fetchall()
            
            for i, (id, name, instructor, category, video_path, views, created_at) in enumerate(all_classes, 1):
                video_status = "✅ COM VÍDEO" if video_path else "❌ SEM VÍDEO"
                print(f"{i:2d}. ID: {id:2d} | {name[:30]:<30} | {instructor[:15]:<15} | {video_status}")
                if video_path:
                    print(f"     📁 Arquivo: {video_path}")
                print(f"     👁️  Views: {views} | 📅 Criado: {created_at}")
                print()
            
            print("="*50)
            print("🤔 POSSÍVEIS CAUSAS DA DIFERENÇA:")
            print("="*50)
            
            # Verificar se o frontend está filtrando
            print("1. O frontend pode estar filtrando apenas aulas com vídeo")
            print("2. Pode haver aulas 'ocultas' ou com status específico")
            print("3. Diferença entre ambiente de desenvolvimento e produção")
            
            print(f"\n💡 RESUMO:")
            print(f"   - Analytics mostra: {total_classes} aulas (TODAS no banco)")
            print(f"   - Gestão mostra: ? aulas (possivelmente apenas com vídeo)")
            print(f"   - Recomendação: Verificar filtros no frontend")
        
        connection.close()
        
    except Exception as e:
        print(f"❌ Erro ao verificar aulas: {e}")

if __name__ == "__main__":
    check_classes()
