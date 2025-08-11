import pymysql
import sys

def check_mysql_connection():
    try:
        # Conectar ao MySQL
        connection = pymysql.connect(
            host='localhost',
            user='root',
            password='',
            database='BS',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        
        print("✅ Conexão com MySQL estabelecida com sucesso!")
        
        with connection.cursor() as cursor:
            # Verificar tabelas
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            
            print(f"\n📊 Tabelas encontradas no banco 'BS': {len(tables)}")
            for table in tables:
                table_name = list(table.values())[0]
                print(f"  - {table_name}")
                
                # Contar registros em cada tabela
                try:
                    cursor.execute(f"SELECT COUNT(*) as count FROM {table_name}")
                    count = cursor.fetchone()['count']
                    print(f"    ({count} registros)")
                except Exception as e:
                    print(f"    (erro ao contar: {e})")
        
        connection.close()
        print("\n✅ Verificação concluída!")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao conectar com MySQL: {str(e)}")
        print("💡 Certifique-se de que o XAMPP está rodando e o MySQL está ativo")
        return False

if __name__ == "__main__":
    check_mysql_connection()
