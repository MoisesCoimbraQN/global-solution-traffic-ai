import psycopg2
from psycopg2 import sql
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Configurações do banco de dados lidas do .env
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': int(os.getenv('DB_PORT', 5432)),
    'user': os.getenv('DB_USER', 'postgres'),
    'password': os.getenv('DB_PASSWORD', ''),
    'database': os.getenv('DB_NAME', 'global_solution_db')
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

def criar_tabelas(conexao):
    """Cria as tabelas do Data Warehouse diretamente"""
    try:
        cursor = conexao.cursor()
        
        sql_script = """
        CREATE TABLE IF NOT EXISTS dim_tempo (
            tempo_id SERIAL PRIMARY KEY,
            data DATE NOT NULL,
            hora TIME NOT NULL,
            dia_semana VARCHAR(20),
            periodo_dia VARCHAR(20)
        );

        CREATE TABLE IF NOT EXISTS dim_regiao (
            regiao_id SERIAL PRIMARY KEY,
            nome_bairro VARCHAR(100) NOT NULL,
            zona_cidade VARCHAR(50),
            cidade VARCHAR(50),
            estado VARCHAR(2),
            cep_principal VARCHAR(10)
        );

        CREATE TABLE IF NOT EXISTS dim_via (
            via_id SERIAL PRIMARY KEY,
            nome_via VARCHAR(150) NOT NULL,
            tipo_via VARCHAR(50),
            limite_velocidade NUMERIC(5, 2),
            comprimento_metros NUMERIC(10, 2),
            id_regiao INT REFERENCES dim_regiao(regiao_id),
            pistas INT
        );

        CREATE TABLE IF NOT EXISTS dim_cruzamento (
            cruzamento_id SERIAL PRIMARY KEY,
            nome_cruzamento VARCHAR(150) NOT NULL,
            latitude NUMERIC(10, 8),
            longitude NUMERIC(11, 8),
            id_via_principal INT REFERENCES dim_via(via_id),
            id_via_secundaria INT REFERENCES dim_via(via_id),
            quantidade_lotes_fiscais INT,
            tipo_cruzamento VARCHAR(50)
        );

        CREATE TABLE IF NOT EXISTS horarios_pico (
            pico_id SERIAL PRIMARY KEY,
            id_regiao INT REFERENCES dim_regiao(regiao_id),
            dia_semana INT,
            hora_inicio TIME,
            hora_fim TIME,
            intensidade_pico NUMERIC(3, 2),
            descricao VARCHAR(150)
        );

CREATE TABLE IF NOT EXISTS fato_transito_tempo_real (
            fato_id SERIAL PRIMARY KEY,
            tempo_id BIGINT,
            localizacao_id INT,
            id_via INT,
            id_tempo_col BIGINT,
            tempo_atual_segundos INT,
            tempo_livre_segundos INT,
            velocidade_atual NUMERIC(5, 2),
            velocidade_livre NUMERIC(5, 2),
            tempo_viagem_segundos INT,
            indice_congestionamento NUMERIC(5, 2),
            nivel_congestionamento_score NUMERIC(5, 2),
            confiabilidade NUMERIC(3, 2)
        );
        """
        
        cursor.execute(sql_script)
        conexao.commit()
        print("✓ Tabelas criadas com sucesso!")
        cursor.close()
        return True
        
    except psycopg2.Error as e:
        conexao.rollback()
        print(f"✗ Erro ao criar tabelas: {e}")
        return False

def inserir_dados_exemplo(conexao):
    """Insere dados de exemplo para testes"""
    try:
        cursor = conexao.cursor()
        
        cursor.execute("""
            INSERT INTO dim_regiao (regiao_id, nome_bairro, zona_cidade, cidade, estado, cep_principal)
            VALUES 
                (1, 'Savassi', 'Zona Sul', 'Belo Horizonte', 'MG', '30130100'),
                (2, 'Centro', 'Região Central', 'Belo Horizonte', 'MG', '30140100'),
                (3, 'Lourdes', 'Zona Sul', 'Belo Horizonte', 'MG', '30170090')
            ON CONFLICT (regiao_id) DO NOTHING;
        """)
        
        cursor.execute("""
            INSERT INTO dim_via (via_id, nome_via, tipo_via, limite_velocidade, comprimento_metros, id_regiao, pistas)
            VALUES 
                (1, 'Avenida Afonso Pena', 'Avenida', 60.00, 5000.00, 1, 4),
                (2, 'Avenida Getúlio Vargas', 'Avenida', 60.00, 6000.00, 2, 4),
                (3, 'Rua da Bahia', 'Rua', 40.00, 3000.00, 2, 2)
            ON CONFLICT (via_id) DO NOTHING;
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
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name;
        """)
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
    print("=" * 60)
    print("DATA WAREHOUSE - GLOBAL SOLUTION (CitizenTech)")
    print("Inicialização do Banco de Dados")
    print("=" * 60 + "\n")
    
    conexao = conectar_banco()
    if not conexao:
        return
    
    print("\n[1/3] Criando estrutura das tabelas...")
    if not criar_tabelas(conexao):
        conexao.close()
        return
    
    print("\n[2/3] Inserindo dados de exemplo...")
    inserir_dados_exemplo(conexao)
    
    print("\n[3/3] Verificando tabelas criadas...")
    verificar_tabelas(conexao)
    
    conexao.close()
    print("\n" + "=" * 60)
    print("✓ Data Warehouse inicializado com sucesso!")
    print("=" * 60)

if __name__ == "__main__":
    main()