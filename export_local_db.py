#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import mysql.connector
import json
from datetime import datetime
from decimal import Decimal
from dotenv import load_dotenv
import os

# Carregar variáveis de ambiente
load_dotenv()

# Configuração do banco local
LOCAL_DB_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': '',
    'database': 'BS',
    'charset': 'utf8mb4'
}

def export_table_data(cursor, table_name):
    """Exportar dados de uma tabela"""
    try:
        cursor.execute(f"SELECT * FROM {table_name}")
        columns = [desc[0] for desc in cursor.description]
        rows = cursor.fetchall()
        
        data = []
        for row in rows:
            row_dict = {}
            for i, value in enumerate(row):
                if isinstance(value, datetime):
                    row_dict[columns[i]] = value.isoformat()
                elif isinstance(value, Decimal):
                    row_dict[columns[i]] = float(value)
                else:
                    row_dict[columns[i]] = value
            data.append(row_dict)
        
        return {
            'columns': columns,
            'data': data,
            'count': len(data)
        }
    except Exception as e:
        print(f"❌ Erro ao exportar tabela {table_name}: {e}")
        return None

def export_database():
    """Exportar todo o banco de dados"""
    try:
        print("🔗 Conectando ao banco local...")
        connection = mysql.connector.connect(**LOCAL_DB_CONFIG)
        cursor = connection.cursor()
        
        # Listar todas as tabelas
        cursor.execute("SHOW TABLES")
        tables = [table[0] for table in cursor.fetchall()]
        print(f"📋 Tabelas encontradas: {tables}")
        
        export_data = {
            'database': 'BS',
            'export_date': datetime.now().isoformat(),
            'tables': {}
        }
        
        # Exportar cada tabela
        for table in tables:
            print(f"📤 Exportando tabela: {table}")
            table_data = export_table_data(cursor, table)
            if table_data:
                export_data['tables'][table] = table_data
                print(f"   ✅ {table_data['count']} registros exportados")
            else:
                print(f"   ❌ Falha ao exportar {table}")
        
        # Salvar em arquivo JSON
        with open('database_export.json', 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)
        
        print(f"\n🎉 Exportação concluída!")
        print(f"📁 Arquivo salvo: database_export.json")
        print(f"📊 Total de tabelas: {len(export_data['tables'])}")
        
        # Mostrar resumo
        for table, data in export_data['tables'].items():
            print(f"   - {table}: {data['count']} registros")
        
        return True
        
    except mysql.connector.Error as e:
        print(f"❌ Erro MySQL: {e}")
        return False
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("🔌 Conexão fechada")

def export_schema():
    """Exportar estrutura das tabelas"""
    try:
        print("🔗 Conectando para exportar schema...")
        connection = mysql.connector.connect(**LOCAL_DB_CONFIG)
        cursor = connection.cursor()
        
        # Listar tabelas
        cursor.execute("SHOW TABLES")
        tables = [table[0] for table in cursor.fetchall()]
        
        schema_sql = []
        schema_sql.append("-- =====================================================")
        schema_sql.append("-- EXPORT DO SCHEMA DO BANCO BS")
        schema_sql.append(f"-- Data: {datetime.now().isoformat()}")
        schema_sql.append("-- =====================================================")
        schema_sql.append("")
        schema_sql.append("CREATE DATABASE IF NOT EXISTS BS;")
        schema_sql.append("USE BS;")
        schema_sql.append("")
        
        for table in tables:
            print(f"📋 Exportando schema da tabela: {table}")
            cursor.execute(f"SHOW CREATE TABLE {table}")
            create_table = cursor.fetchone()[1]
            schema_sql.append(f"-- Tabela: {table}")
            schema_sql.append(f"DROP TABLE IF EXISTS {table};")
            schema_sql.append(create_table + ";")
            schema_sql.append("")
        
        # Salvar schema
        with open('database_schema.sql', 'w', encoding='utf-8') as f:
            f.write('\n'.join(schema_sql))
        
        print("✅ Schema exportado para: database_schema.sql")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao exportar schema: {e}")
        return False
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()

if __name__ == "__main__":
    print("🚀 Iniciando exportação do banco de dados BS...")
    
    # Exportar schema
    print("\n1️⃣ Exportando estrutura das tabelas...")
    export_schema()
    
    # Exportar dados
    print("\n2️⃣ Exportando dados...")
    success = export_database()
    
    if success:
        print("\n🎉 Exportação completa!")
        print("📁 Arquivos gerados:")
        print("   - database_schema.sql (estrutura)")
        print("   - database_export.json (dados)")
    else:
        print("\n❌ Falha na exportação")
