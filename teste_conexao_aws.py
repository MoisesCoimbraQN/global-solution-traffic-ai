import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

print('Testando conexao com AWS...')
print(f'Host: {os.getenv("DB_HOST")}')
print(f'Port: {os.getenv("DB_PORT")}')
print(f'Database: {os.getenv("DB_NAME")}')
print(f'User: {os.getenv("DB_USER")}')
print()

try:
    conn = psycopg2.connect(
        host=os.getenv('DB_HOST'),
        port=int(os.getenv('DB_PORT')),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME'),
        connect_timeout=10
    )
    print('[OK] Conectado ao banco AWS com sucesso!')
    
    cursor = conn.cursor()
    cursor.execute('SELECT version();')
    version = cursor.fetchone()
    print(f'PostgreSQL: {version[0][:50]}...')
    
    cursor.execute('SELECT COUNT(*) FROM fato_transito;')
    count = cursor.fetchone()[0]
    print(f'Total de registros em fato_transito: {count}')
    
    cursor.close()
    conn.close()
except Exception as e:
    print(f'[ERRO] {str(e)}')

