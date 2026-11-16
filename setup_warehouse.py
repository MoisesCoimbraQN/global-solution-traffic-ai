import psycopg2
from psycopg2 import sql
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Configurações do banco de dados
DB_CONFIG = {
    'host': 'ip-172-31-33-147.us-east-2.compute.internallocalhost',
    'port': 5432,
    'user': os.getenv('DB_USER', 'postgres'),
    'password': os.getenv('DB_PASSWORD', ''),
    'database': 'global_solution_db'
}

def conectar_banco():
    """Conecta ao banco de dados PostgreSQL"""
    try:
        conexao = psycopg2.connect(**DB_CONFIG)
        print("✓ Conectado ao banco de dados com sucesso!")
        return conexao
    except psycopg2.Error as e:
        print(f"✗ Erro ao conectar: {e}")
        return None

def criar_tabelas(conexao, arquivo_sql='criar_warehouse.sql'):
    """Executa o script SQL para criar as tabelas"""
    try:
        cursor = conexao.cursor()
        
        # Ler o arquivo SQL
        with open(arquivo_sql, 'r', encoding='utf-8') as f:
            sql_script = f.read()
        
        # Executar o script
        cursor.execute(sql_script)
        conexao.commit()
        
        print("✓ Tabelas criadas com sucesso!")
        cursor.close()
        return True
        
    except psycopg2.Error as e:
        conexao.rollback()
        print(f"✗ Erro ao criar tabelas: {e}")
        return False

def popular_dim_tempo(conexao, data_inicio='2026-11-01', data_fim='2026-12-31'):
    """Popula a dimensão de tempo"""
    try:
        cursor = conexao.cursor()
        
        query = "SELECT popular_dim_tempo(%s::DATE, %s::DATE);"
        cursor.execute(query, (data_inicio, data_fim))
        resultado = cursor.fetchall()
        
        print(f"✓ {resultado[0][0]}")
        conexao.commit()
        cursor.close()
        return True
        
    except psycopg2.Error as e:
        conexao.rollback()
        print(f"✗ Erro ao popular dim_tempo: {e}")
        return False

def inserir_dados_exemplo(conexao):
    """Insere dados de exemplo para testes"""
    try:
        cursor = conexao.cursor()
        
        # Inserir região
        cursor.execute("""
            INSERT INTO dim_regiao (nome_bairro, zona_cidade, cidade, estado, cep_principal)
            VALUES 
                ('Savassi', 'Zona Sul', 'Belo Horizonte', 'MG', '30130100'),
                ('Centro', 'Região Central', 'Belo Horizonte', 'MG', '30140100'),
                ('Lourdes', 'Zona Sul', 'Belo Horizonte', 'MG', '30170090')
            ON CONFLICT DO NOTHING;
        """)
        
        # Inserir vias
        cursor.execute("""
            INSERT INTO dim_via (nome_via, tipo_via, limite_velocidade, comprimento_metros, id_regiao, pistas)
            VALUES 
                ('Avenida Afonso Pena', 'Avenida', 60.00, 5000.00, 1, 4),
                ('Avenida Getúlio Vargas', 'Avenida', 60.00, 6000.00, 2, 4),
                ('Rua da Bahia', 'Rua', 40.00, 3000.00, 2, 2)
            ON CONFLICT DO NOTHING;
        """)
        
        # Inserir cruzamentos (semáforos)
        cursor.execute("""
            INSERT INTO dim_cruzamento (nome_cruzamento, latitude, longitude, id_via_principal, id_via_secundaria, quantidade_lotes_fiscais, tipo_cruzamento)
            VALUES 
                ('Praça da Liberdade', -19.9322, -43.9386, 1, 2, 4, 'complexo'),
                ('Av. Getúlio x Rua da Bahia', -19.9331, -43.9378, 2, 3, 2, 'normal')
            ON CONFLICT DO NOTHING;
        """)
        
        # Inserir horários de pico
        cursor.execute("""
            INSERT INTO horarios_pico (id_regiao, dia_semana, hora_inicio, hora_fim, intensidade_pico, descricao)
            VALUES 
                (1, 2, '07:00:00', '09:30:00', 2.5, 'Pico matinal - Zona Sul'),
                (1, 2, '17:00:00', '19:30:00', 3.0, 'Pico vespertino - Zona Sul'),
                (2, 2, '08:00:00', '10:00:00', 2.2, 'Pico matinal - Centro'),
                (2, 2, '17:30:00', '19:00:00', 2.8, 'Pico vespertino - Centro')
            ON CONFLICT DO NOTHING;
        """)
        
        conexao.commit()
        print("✓ Dados de exemplo inseridos com sucesso!")
        cursor.close()
        return True
        
    except psycopg2.Error as e:
        conexao.rollback()
        print(f"✗ Erro ao inserir dados de exemplo: {e}")
        return False

def verificar_tabelas(conexao):
    """Verifica as tabelas criadas"""
    try:
        cursor = conexao.cursor()
        
        query = """
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name;
        """
        
        cursor.execute(query)
        tabelas = cursor.fetchall()
        
        print("\n✓ Tabelas criadas no banco de dados:")
        print("-" * 50)
        for tabela in tabelas:
            print(f"  • {tabela[0]}")
        
        cursor.close()
        return True
        
    except psycopg2.Error as e:
        print(f"✗ Erro ao verificar tabelas: {e}")
        return False

def main():
    """Função principal"""
    print("=" * 60)
    print("DATA WAREHOUSE - GLOBAL SOLUTION (CitizenTech)")
    print("Inicialização do Banco de Dados")
    print("=" * 60 + "\n")
    
    # Conectar
    conexao = conectar_banco()
    if not conexao:
        return
    
    # Criar tabelas
    print("\n[1/4] Criando estrutura das tabelas...")
    if not criar_tabelas(conexao):
        conexao.close()
        return
    
    # Popular dimensão de tempo
    print("\n[2/4] Populando dimensão de tempo...")
    if not popular_dim_tempo(conexao):
        conexao.close()
        return
    
    # Inserir dados de exemplo
    print("\n[3/4] Inserindo dados de exemplo...")
    if not inserir_dados_exemplo(conexao):
        conexao.close()
        return
    
    # Verificar
    print("\n[4/4] Verificando tabelas criadas...")
    verificar_tabelas(conexao)
    
    # Fechar conexão
    conexao.close()
    
    print("\n" + "=" * 60)
    print("✓ Data Warehouse inicializado com sucesso!")
    print("=" * 60)

if __name__ == "__main__":
    main()
