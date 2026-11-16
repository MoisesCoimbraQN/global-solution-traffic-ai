import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

conn = psycopg2.connect(
    host=os.getenv('DB_HOST'),
    port=int(os.getenv('DB_PORT')),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
    database=os.getenv('DB_NAME')
)

cursor = conn.cursor()

# Listar colunas
cursor.execute("""
    SELECT column_name, data_type 
    FROM information_schema.columns 
    WHERE table_name='fato_transito_tempo_real'
    ORDER BY ordinal_position
""")

print("[Colunas da tabela fato_transito_tempo_real]")
for col in cursor.fetchall():
    print(f"  - {col[0]}: {col[1]}")

# Testar query
print("\n[Testando query]")
cursor.execute("SELECT * FROM fato_transito_tempo_real LIMIT 1")
row = cursor.fetchone()
if row:
    print(f"Primeira linha encontrada: {len(row)} colunas")
    print(f"Dados: {row}")

cursor.close()
conn.close()
