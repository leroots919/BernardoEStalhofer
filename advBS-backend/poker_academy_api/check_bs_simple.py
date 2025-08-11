#!/usr/bin/env python3
import pymysql

try:
    print("🔍 Conectando ao MySQL...")
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        database='BS'
    )
    
    print("✅ Conectado ao banco BS!")
    
    cursor = conn.cursor()
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    
    print(f"\n📊 Tabelas encontradas no banco BS: {len(tables)}")
    for table in tables:
        print(f"  - {table[0]}")
        
        # Contar registros
        try:
            cursor.execute(f"SELECT COUNT(*) FROM {table[0]}")
            count = cursor.fetchone()[0]
            print(f"    ({count} registros)")
        except Exception as e:
            print(f"    (erro: {e})")
    
    conn.close()
    print("\n✅ Verificação concluída!")
    
except Exception as e:
    print(f"❌ Erro: {e}")
    print("💡 Certifique-se de que o XAMPP está rodando!")
