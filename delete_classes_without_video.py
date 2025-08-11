#!/usr/bin/env python3
"""
Script para deletar aulas que não têm vídeo
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

def delete_classes_without_video():
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
            print("🔍 VERIFICANDO AULAS SEM VÍDEO\n")
            
            # Listar aulas sem vídeo
            cursor.execute("""
                SELECT id, name, instructor, category, views, created_at
                FROM classes 
                WHERE video_path IS NULL OR video_path = ''
                ORDER BY id
            """)
            
            classes_without_video = cursor.fetchall()
            
            if not classes_without_video:
                print("✅ Não há aulas sem vídeo para deletar!")
                return
            
            print(f"📋 ENCONTRADAS {len(classes_without_video)} AULAS SEM VÍDEO:")
            print("="*60)
            
            for id, name, instructor, category, views, created_at in classes_without_video:
                print(f"ID: {id:2d} | {name[:30]:<30} | {instructor[:15]:<15}")
                print(f"      Categoria: {category} | Views: {views} | Criado: {created_at}")
                print()
            
            # Confirmar deleção
            print("="*60)
            print("⚠️  ATENÇÃO: Esta operação irá DELETAR permanentemente essas aulas!")
            print("   - Dados de progresso dos usuários também serão removidos")
            print("   - Esta ação NÃO pode ser desfeita")
            
            confirm = input("\n🤔 Deseja continuar? Digite 'DELETAR' para confirmar: ")
            
            if confirm != 'DELETAR':
                print("❌ Operação cancelada pelo usuário.")
                return
            
            print("\n🗑️  DELETANDO AULAS SEM VÍDEO...")
            
            # Deletar progresso relacionado primeiro (devido às foreign keys)
            for id, _, _, _, _, _ in classes_without_video:
                cursor.execute("DELETE FROM user_progress WHERE class_id = %s", (id,))
                deleted_progress = cursor.rowcount
                if deleted_progress > 0:
                    print(f"   🗑️  Removido progresso de {deleted_progress} usuários da aula ID {id}")
            
            # Deletar visualizações relacionadas
            for id, _, _, _, _, _ in classes_without_video:
                cursor.execute("DELETE FROM class_views WHERE class_id = %s", (id,))
                deleted_views = cursor.rowcount
                if deleted_views > 0:
                    print(f"   🗑️  Removidas {deleted_views} visualizações da aula ID {id}")
            
            # Deletar favoritos relacionados
            for id, _, _, _, _, _ in classes_without_video:
                cursor.execute("DELETE FROM favorites WHERE class_id = %s", (id,))
                deleted_favorites = cursor.rowcount
                if deleted_favorites > 0:
                    print(f"   🗑️  Removidos {deleted_favorites} favoritos da aula ID {id}")
            
            # Deletar as aulas
            cursor.execute("""
                DELETE FROM classes 
                WHERE video_path IS NULL OR video_path = ''
            """)
            
            deleted_classes = cursor.rowcount
            connection.commit()
            
            print(f"\n✅ OPERAÇÃO CONCLUÍDA!")
            print(f"   📊 {deleted_classes} aulas deletadas")
            print(f"   🧹 Dados relacionados também removidos")
            
            # Verificar resultado
            print("\n📋 AULAS RESTANTES:")
            cursor.execute("SELECT COUNT(*) FROM classes")
            remaining_classes = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM classes WHERE video_path IS NOT NULL AND video_path != ''")
            classes_with_video = cursor.fetchone()[0]
            
            print(f"   📚 Total de aulas: {remaining_classes}")
            print(f"   🎥 Aulas com vídeo: {classes_with_video}")
            
            if remaining_classes == classes_with_video:
                print("   ✅ Agora todas as aulas têm vídeo!")
        
        connection.close()
        
    except Exception as e:
        print(f"❌ Erro ao deletar aulas: {e}")

if __name__ == "__main__":
    delete_classes_without_video()
