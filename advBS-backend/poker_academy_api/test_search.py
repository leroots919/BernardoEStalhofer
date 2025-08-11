#!/usr/bin/env python3
import pymysql

try:
    print("🔍 Testando busca de clientes...")
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        database='BS'
    )
    
    cursor = conn.cursor()
    
    # Buscar todos os clientes
    cursor.execute("SELECT id, name, email, type FROM users WHERE type = 'cliente'")
    all_clients = cursor.fetchall()
    
    print(f"\n👥 Total de clientes no banco: {len(all_clients)}")
    print("=" * 50)
    
    for client in all_clients:
        print(f"ID: {client[0]} | Nome: {client[1]} | Email: {client[2]}")
    
    # Buscar clientes com "vanessa"
    print(f"\n🔍 Buscando clientes com 'vanessa'...")
    cursor.execute("SELECT id, name, email FROM users WHERE type = 'cliente' AND (name LIKE '%vanessa%' OR email LIKE '%vanessa%')")
    vanessa_clients = cursor.fetchall()
    
    print(f"Encontrados: {len(vanessa_clients)}")
    for client in vanessa_clients:
        print(f"ID: {client[0]} | Nome: {client[1]} | Email: {client[2]}")
    
    conn.close()
    print("\n✅ Teste concluído!")
    
except Exception as e:
    print(f"❌ Erro: {e}")
