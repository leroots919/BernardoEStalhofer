import pymysql

conn = pymysql.connect(
    host='localhost',
    user='root',
    password='',
    database='BS'
)

cursor = conn.cursor()
cursor.execute("SELECT id, name, email, type FROM users ORDER BY type, id")
users = cursor.fetchall()

print("=== USUÁRIOS DO SISTEMA ===")
for user in users:
    print(f"ID: {user[0]} | Nome: {user[1]} | Email: {user[2]} | Tipo: {user[3]}")

conn.close()
