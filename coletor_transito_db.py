import requests
import psycopg2
import os
from dotenv import load_dotenv
from datetime import datetime
import time
import json

# Carregar variáveis de ambiente
load_dotenv()

# Configurações
TOMTOM_API_KEY = os.getenv("TOMTOM_API_KEY")
DB_CONFIG = {
    'host': os.getenv('DB_HOST'),
    'port': int(os.getenv('DB_PORT', 5432)),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME')
}

# Dados das vias a monitorar
VIAS_MONITORAMENTO = [
    {
        'id_via': 1,
        'nome': 'Avenida Afonso Pena',
        'coordenadas': '-19.9322,-43.9386:-19.9331,-43.9378'
    },
    {
        'id_via': 2,
        'nome': 'Avenida Getúlio Vargas',
        'coordenadas': '-19.9340,-43.9400:-19.9350,-43.9390'
    }
]

class ColecionadorTransito:
    """Classe responsável por coletar e armazenar dados de tráfego"""
    
    def __init__(self):
        self.conexao = None
        self.conectar_banco()
    
    def conectar_banco(self):
        """Conecta ao banco de dados PostgreSQL"""
        try:
            self.conexao = psycopg2.connect(**DB_CONFIG)
            print("✓ Conectado ao banco de dados")
        except psycopg2.Error as e:
            print(f"✗ Erro ao conectar ao banco: {e}")
            raise
    
    def gerar_id_tempo(self):
        """Gera o id_tempo no formato YYYYMMDDHHMM"""
        agora = datetime.now()
        minuto = (agora.minute // 15) * 15  # Arredondar para 15 minutos
        id_tempo = agora.strftime('%Y%m%d%H') + f"{minuto:02d}"
        return id_tempo
    
    def calcular_score_congestionamento(self, velocidade_atual, velocidade_livre, tempo_atual, tempo_livre):
        """Calcula o score de congestionamento (0-100)"""
        if velocidade_livre == 0 or tempo_livre == 0:
            return 0
        
        # Score baseado no fator de atraso
        fator_atraso = tempo_atual / tempo_livre if tempo_livre > 0 else 1
        score = min(100, (fator_atraso - 1) * 100)  # 0% de atraso = 0 pontos, 2x de atraso = 100 pontos
        
        return round(max(0, score), 2)
    
    def coletar_dados_via(self, via):
        """Coleta dados de tráfego para uma via usando a API TomTom"""
        try:
            url = f"https://api.tomtom.com/routing/1/calculateRoute/{via['coordenadas']}/json"
            
            params = {
                'key': TOMTOM_API_KEY,
                'sectionType': 'traffic',
                'travelMode': 'car'
            }
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                if "routes" in data and len(data["routes"]) > 0:
                    route = data["routes"][0]
                    summary = route["summary"]
                    
                    tempo_atual = summary.get("travelTimeInSeconds", 0)
                    tempo_livre = summary.get("travelTimeInSeconds", tempo_atual)  # TomTom não retorna sem trânsito
                    
                    # Estimativa: velocidade = distância / tempo
                    distancia_km = summary.get("lengthInMeters", 0) / 1000
                    velocidade_atual = (distancia_km / tempo_atual * 3600) if tempo_atual > 0 else 0
                    velocidade_livre = (distancia_km / tempo_livre * 3600) if tempo_livre > 0 else velocidade_atual
                    
                    score = self.calcular_score_congestionamento(
                        velocidade_atual, velocidade_livre, tempo_atual, tempo_livre
                    )
                    
                    return {
                        'velocidade_atual': round(velocidade_atual, 2),
                        'velocidade_livre': round(velocidade_livre, 2),
                        'tempo_atual_segundos': tempo_atual,
                        'tempo_livre_segundos': tempo_livre,
                        'nivel_congestionamento_score': score,
                        'atraso_segundos': summary.get("trafficDelayInSeconds", 0),
                        'sucesso': True
                    }
            else:
                print(f"✗ Erro na resposta da API: {response.status_code}")
                return {'sucesso': False}
        
        except requests.exceptions.Timeout:
            print(f"✗ Timeout ao conectar à API TomTom para {via['nome']}")
            return {'sucesso': False}
        except Exception as e:
            print(f"✗ Erro ao coletar dados de {via['nome']}: {str(e)}")
            return {'sucesso': False}
    
    def inserir_dados_fato(self, id_via, id_tempo, dados):
        """Insere dados coletados na tabela fato_transito_tempo_real"""
        try:
            cursor = self.conexao.cursor()
            
            query = """
                INSERT INTO fato_transito_tempo_real 
                (id_via, id_tempo, velocidade_atual, velocidade_livre, 
                 tempo_atual_segundos, tempo_livre_segundos, nivel_congestionamento_score)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            
            cursor.execute(query, (
                id_via,
                id_tempo,
                dados['velocidade_atual'],
                dados['velocidade_livre'],
                dados['tempo_atual_segundos'],
                dados['tempo_livre_segundos'],
                dados['nivel_congestionamento_score']
            ))
            
            self.conexao.commit()
            cursor.close()
            
            return True
        
        except psycopg2.Error as e:
            self.conexao.rollback()
            print(f"✗ Erro ao inserir dados: {e}")
            return False
    
    def coletar_e_armazenar(self):
        """Coleta dados de todas as vias e armazena no banco"""
        print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Iniciando coleta de dados...")
        
        id_tempo = self.gerar_id_tempo()
        total_sucesso = 0
        
        for via in VIAS_MONITORAMENTO:
            print(f"\n  Coletando dados de: {via['nome']}")
            
            dados = self.coletar_dados_via(via)
            
            if dados['sucesso']:
                if self.inserir_dados_fato(via['id_via'], id_tempo, dados):
                    print(f"    ✓ Velocidade: {dados['velocidade_atual']} km/h")
                    print(f"    ✓ Score congestionamento: {dados['nivel_congestionamento_score']}/100")
                    total_sucesso += 1
                else:
                    print(f"    ✗ Falha ao inserir no banco de dados")
        
        print(f"\n✓ Coleta concluída: {total_sucesso}/{len(VIAS_MONITORAMENTO)} vias com sucesso")
    
    def iniciar_monitoramento_continuo(self, intervalo_segundos=300):
        """Inicia monitoramento contínuo a cada intervalo especificado (padrão: 5 minutos)"""
        print("=" * 60)
        print("MONITORAMENTO CONTÍNUO DE TRÁFEGO")
        print(f"Intervalo: {intervalo_segundos} segundos")
        print("Pressione Ctrl+C para parar")
        print("=" * 60)
        
        try:
            while True:
                self.coletar_e_armazenar()
                print(f"\nProxima coleta em {intervalo_segundos} segundos...")
                time.sleep(intervalo_segundos)
        
        except KeyboardInterrupt:
            print("\n\nMonitoramento interrompido pelo usuário")
        finally:
            self.fechar()
    
    def fechar(self):
        """Fecha a conexão com o banco de dados"""
        if self.conexao:
            self.conexao.close()
            print("✓ Conexão fechada")

def main():
    """Função principal"""
    print("=" * 60)
    print("COLETOR DE DADOS DE TRÁFEGO EM TEMPO REAL")
    print("Global Solution - CitizenTech")
    print("=" * 60)
    
    try:
        coletor = ColecionadorTransito()
        
        # Executar coleta única
        coletor.coletar_e_armazenar()
        
        # Descomente a linha abaixo para monitoramento contínuo
        # coletor.iniciar_monitoramento_continuo(intervalo_segundos=300)
        
    except Exception as e:
        print(f"✗ Erro fatal: {str(e)}")
    finally:
        if 'coletor' in locals():
            coletor.fechar()

if __name__ == "__main__":
    main()
