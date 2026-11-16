"""
GLOBAL SOLUTION - CITIZENTECH
Passo 2: Algoritmo de Otimização e Controle de Semáforos Inteligentes

Módulo principal que implementa a lógica de decisão para otimização de semáforos
baseada em dados de tráfego em tempo real.

Autor: Global Solution Team
Data: 2026-11-16
"""

import psycopg2
import os
from dotenv import load_dotenv
from datetime import datetime
import logging
from enum import Enum
from dataclasses import dataclass
from typing import Dict, List, Tuple

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Carregar variáveis de ambiente
load_dotenv()

# =====================================================
# ENUMERAÇÕES E CLASSES
# =====================================================

class NivelCongestionamento(Enum):
    """Classificação dos níveis de congestionamento"""
    LIVRE = "livre"              # Score: 0-25
    MODERADO = "moderado"        # Score: 25-50
    INTENSO = "intenso"          # Score: 50-75
    CRÍTICO = "crítico"          # Score: 75-100

class AcaoSemaforo(Enum):
    """Ações possíveis do sistema de semáforos"""
    MANTER = "manter"            # Mantém ciclo padrão
    AUMENTAR_VERDE = "aumentar"  # Aumenta tempo de verde
    REDUZIR_VERDE = "reduzir"    # Reduz tempo de verde
    ATIVAR_PRIORIDADE = "prioridade"  # Ativa modo prioritário

@dataclass
class MetricasVia:
    """Armazena as métricas de uma via"""
    id_via: int
    nome_via: str
    velocidade_atual: float
    velocidade_livre: float
    tempo_atual_segundos: int
    tempo_livre_segundos: int
    fator_atraso: float
    nivel_congestionamento_score: float
    id_semaforo: int
    nome_cruzamento: str
    
    def __repr__(self):
        return f"Via: {self.nome_via} | Fator: {self.fator_atraso:.2f} | Score: {self.nivel_congestionamento_score:.1f}"

@dataclass
class DecisaoSemaforo:
    """Armazena a decisão do algoritmo para um semáforo"""
    id_semaforo: int
    acao: AcaoSemaforo
    tempo_verde_anterior_segundos: int
    tempo_verde_novo_segundos: int
    reducao_fila_estimada_metros: float
    eficacia_ajuste: float
    motivo_ajuste: str
    algoritmo_utilizado: str = "heurística_adaptativa"

class OtimizadorSemaforos:
    """Classe principal que orquestra o algoritmo de otimização"""
    
    def __init__(self):
        """Inicializa o otimizador e conecta ao banco de dados"""
        self.conexao = None
        self.metricas_atuais = {}
        self.conectar_banco()
        
        # Parâmetros do algoritmo (podem ser ajustados)
        self.FATOR_LIMIAR_BAIXO = 1.0      # Transição para "moderado"
        self.FATOR_LIMIAR_MEDIO = 1.2      # Transição para "intenso"
        self.FATOR_LIMIAR_ALTO = 1.5       # Transição para "crítico"
        
        self.TEMPO_VERDE_PADRAO = 60       # segundos
        self.TEMPO_VERDE_MINIMO = 30       # segundos
        self.TEMPO_VERDE_MAXIMO = 120      # segundos
        self.INCREMENTO_AJUSTE = 10        # segundos
        
        logger.info("Otimizador de Semáforos inicializado")
    
    def conectar_banco(self):
        """Conecta ao banco de dados PostgreSQL"""
        try:
            self.conexao = psycopg2.connect(
                host=os.getenv('DB_HOST'),
                port=int(os.getenv('DB_PORT', 5432)),
                user=os.getenv('DB_USER'),
                password=os.getenv('DB_PASSWORD'),
                database=os.getenv('DB_NAME')
            )
            logger.info("[OK] Conectado ao banco")
        except psycopg2.Error as e:
            logger.warning(f"[AVISO] Nao pode conectar ao banco")
            logger.warning("[INFO] Sistema rodara em modo simulacao")
            self.conexao = None
    
    def obter_metricas_atuais(self) -> Dict[int, MetricasVia]:
        """
        Obtém as métricas de trânsito mais recentes do banco de dados
        
        Returns:
            Dict mapeando id_semaforo → MetricasVia
        """
        if not self.conexao:
            # Modo simulacao: retornar dados fake
            self.metricas_atuais = {
                1: MetricasVia(
                    id_via=1, nome_via="Av. Afonso Pena",
                    velocidade_atual=35.0, velocidade_livre=50.0,
                    tempo_atual_segundos=180, tempo_livre_segundos=120,
                    id_semaforo=1, nome_cruzamento="Liberdade",
                    fator_atraso=1.5, nivel_congestionamento_score=65
                )
            }
            return self.metricas_atuais
        
        try:
            cursor = self.conexao.cursor()
            
            query = """
                SELECT DISTINCT ON (c.id_semaforo)
                    f.id_via,
                    v.nome_via,
                    f.velocidade_atual,
                    f.velocidade_livre,
                    f.tempo_atual_segundos,
                    f.tempo_livre_segundos,
                    f.fator_atraso,
                    f.nivel_congestionamento_score,
                    c.id_semaforo,
                    c.nome_cruzamento
                FROM fato_transito_tempo_real f
                JOIN dim_via v ON f.id_via = v.id_via
                JOIN dim_cruzamento c ON v.id_via = c.id_via_principal
                WHERE f.data_criacao >= NOW() - INTERVAL '15 minutes'
                ORDER BY c.id_semaforo, f.data_criacao DESC;
            """
            
            cursor.execute(query)
            resultados = cursor.fetchall()
            cursor.close()
            
            self.metricas_atuais = {}
            for row in resultados:
                metricas = MetricasVia(
                    id_via=row[0],
                    nome_via=row[1],
                    velocidade_atual=row[2],
                    velocidade_livre=row[3],
                    tempo_atual_segundos=row[4],
                    tempo_livre_segundos=row[5],
                    fator_atraso=row[6],
                    nivel_congestionamento_score=row[7],
                    id_semaforo=row[8],
                    nome_cruzamento=row[9]
                )
                self.metricas_atuais[row[8]] = metricas
            
            logger.info(f"[OK] {len(self.metricas_atuais)} semaforos processados")
            return self.metricas_atuais
            
        except psycopg2.Error as e:
            logger.warning(f"[AVISO] Nao pode obter metricas: {str(e)}")
            return {}
    
    def classificar_congestionamento(self, score: float) -> NivelCongestionamento:
        """
        Classifica o nível de congestionamento baseado no score
        
        Args:
            score: Score de congestionamento (0-100)
            
        Returns:
            NivelCongestionamento correspondente
        """
        if score < 25:
            return NivelCongestionamento.LIVRE
        elif score < 50:
            return NivelCongestionamento.MODERADO
        elif score < 75:
            return NivelCongestionamento.INTENSO
        else:
            return NivelCongestionamento.CRÍTICO
    
    def aplicar_logica_fuzzy(self, fator_atraso: float, score: float) -> Tuple[AcaoSemaforo, str]:
        """
        Aplica lógica fuzzy para tomar decisão sobre ajuste de semáforo
        
        A lógica fuzzy fornece um mecanismo mais natural e robusto para lidar
        com incertezas nas métricas de tráfego.
        
        Args:
            fator_atraso: Razão entre tempo atual e tempo livre
            score: Score de congestionamento (0-100)
            
        Returns:
            Tupla (AcaoSemaforo, motivo_descritivo)
        """
        
        # Fuzzy Sets para fator_atraso
        # Quanto maior o fator, mais congestionado está
        degree_livre = max(0, min(1, (1.0 - fator_atraso) / 0.2)) if fator_atraso < 1.0 else 0
        degree_moderado = 1 - abs(fator_atraso - 1.2) / 0.4 if 0.8 < fator_atraso < 1.6 else 0
        degree_intenso = 1 - abs(fator_atraso - 1.5) / 0.5 if 1.2 < fator_atraso < 2.0 else 0
        degree_critico = max(0, min(1, (fator_atraso - 1.5) / 0.5)) if fator_atraso > 1.5 else 0
        
        # Normalizar
        total = degree_livre + degree_moderado + degree_intenso + degree_critico
        if total > 0:
            degree_livre /= total
            degree_moderado /= total
            degree_intenso /= total
            degree_critico /= total
        
        # Regras Fuzzy
        # Regra 1: Se livre ou moderado → Manter
        confianca_manter = degree_livre * 0.9 + degree_moderado * 0.4
        
        # Regra 2: Se moderado/intenso → Aumentar verde (prioridade)
        confianca_aumentar = degree_moderado * 0.7 + degree_intenso * 0.9 + degree_critico * 0.95
        
        # Regra 3: Se crítico → Ativar prioridade total
        confianca_prioridade = degree_critico * 0.8 + degree_intenso * 0.3
        
        # Defuzzificação: Escolher ação com maior confiança
        accoes_confianca = [
            (AcaoSemaforo.MANTER, confianca_manter, "Tráfego normal"),
            (AcaoSemaforo.AUMENTAR_VERDE, confianca_aumentar, f"Congestionamento moderado/intenso (fator: {fator_atraso:.2f})"),
            (AcaoSemaforo.ATIVAR_PRIORIDADE, confianca_prioridade, f"Congestionamento crítico (score: {score:.1f})")
        ]
        
        acao, confianca, motivo = max(accoes_confianca, key=lambda x: x[1])
        
        return acao, motivo
    
    def calcular_ajuste_tempo_verde(self, 
                                    metricas: MetricasVia, 
                                    acao: AcaoSemaforo) -> DecisaoSemaforo:
        """
        Calcula o ajuste específico de tempo de verde baseado na ação
        
        Args:
            metricas: Métricas da via
            acao: Ação a ser tomada
            
        Returns:
            DecisaoSemaforo com os valores calculados
        """
        
        tempo_anterior = self.TEMPO_VERDE_PADRAO
        tempo_novo = tempo_anterior
        reducao_fila_estimada = 0
        eficacia = 0
        
        if acao == AcaoSemaforo.MANTER:
            tempo_novo = tempo_anterior
            eficacia = 0
            motivo = "Ciclo mantido - tráfego normal"
            
        elif acao == AcaoSemaforo.AUMENTAR_VERDE:
            # Aumentar proporcionalmente ao fator de atraso
            incremento = min(
                int(self.INCREMENTO_AJUSTE * (metricas.fator_atraso - 1.0)),
                self.TEMPO_VERDE_MAXIMO - tempo_anterior
            )
            tempo_novo = tempo_anterior + incremento
            
            # Estimar redução de fila (heurística: 1 segundo extra = 5 metros menos de fila)
            reducao_fila_estimada = incremento * 5
            
            # Eficacia estimada: quanto mais incremento, mais eficaz (até 30% melhoria esperada)
            eficacia = min(30, (incremento / self.TEMPO_VERDE_MAXIMO) * 30)
            motivo = f"Verde estendido em +{incremento}s | Redução estimada: {reducao_fila_estimada:.0f}m"
            
        elif acao == AcaoSemaforo.ATIVAR_PRIORIDADE:
            # Modo prioritário: máximo tempo possível
            tempo_novo = self.TEMPO_VERDE_MAXIMO
            incremento = tempo_novo - tempo_anterior
            reducao_fila_estimada = incremento * 7  # Maior potencial
            eficacia = 40  # Alta eficacia esperada
            motivo = f"MODO PRIORITÁRIO ATIVADO | Verde: {tempo_novo}s | Redução estimada: {reducao_fila_estimada:.0f}m"
        
        elif acao == AcaoSemaforo.REDUZIR_VERDE:
            # Reduzir (menos comum, quando há alternativas melhores)
            reducao = min(self.INCREMENTO_AJUSTE // 2, tempo_anterior - self.TEMPO_VERDE_MINIMO)
            tempo_novo = tempo_anterior - reducao
            eficacia = -5  # Pequena redução
            motivo = "Verde reduzido para balancear rede"
        
        # Não ajustar se mudança é mínima (<5 segundos)
        if abs(tempo_novo - tempo_anterior) < 5:
            tempo_novo = tempo_anterior
            eficacia = 0
            motivo = "Ajuste rejeitado (mudança < 5s)"
        
        decisao = DecisaoSemaforo(
            id_semaforo=metricas.id_semaforo,
            acao=acao,
            tempo_verde_anterior_segundos=tempo_anterior,
            tempo_verde_novo_segundos=tempo_novo,
            reducao_fila_estimada_metros=reducao_fila_estimada,
            eficacia_ajuste=eficacia,
            motivo_ajuste=motivo
        )
        
        return decisao
    
    def tomar_decisao(self, metricas: MetricasVia) -> DecisaoSemaforo:
        """
        Orquestra a tomada de decisão para um semáforo
        
        Pipeline:
        1. Classificar congestionamento
        2. Aplicar lógica fuzzy
        3. Calcular ajuste específico
        
        Args:
            metricas: Métricas da via
            
        Returns:
            DecisaoSemaforo com todos os detalhes
        """
        
        # Etapa 1: Classificar
        nivel = self.classificar_congestionamento(metricas.nivel_congestionamento_score)
        
        # Etapa 2: Aplicar fuzzy
        acao, motivo_fuzzy = self.aplicar_logica_fuzzy(
            metricas.fator_atraso, 
            metricas.nivel_congestionamento_score
        )
        
        # Etapa 3: Calcular ajuste
        decisao = self.calcular_ajuste_tempo_verde(metricas, acao)
        decisao.motivo_ajuste = motivo_fuzzy + " | " + decisao.motivo_ajuste
        
        return decisao
    
    def registrar_decisao(self, decisao: DecisaoSemaforo) -> bool:
        """
        Persiste a decisão na tabela fato_ciclo_semaforo
        
        Args:
            decisao: DecisaoSemaforo a ser registrada
            
        Returns:
            True se sucesso, False se erro
        """
        if not self.conexao:
            return True  # Simulacao: sempre retorna True
        
        try:
            cursor = self.conexao.cursor()
            
            agora = datetime.now()
            minuto = (agora.minute // 15) * 15
            id_tempo = agora.strftime('%Y%m%d%H') + f"{minuto:02d}"
            
            query = """
                INSERT INTO fato_ciclo_semaforo 
                (id_semaforo, id_tempo, tempo_verde_anterior_segundos, 
                 tempo_verde_novo_segundos, ajuste_realizado, 
                 reducao_fila_estimada_metros, motivo_ajuste, 
                 algoritmo_utilizado, eficacia_ajuste)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            
            ajuste_realizado = (
                decisao.tempo_verde_novo_segundos != decisao.tempo_verde_anterior_segundos
            )
            
            cursor.execute(query, (
                decisao.id_semaforo,
                id_tempo,
                decisao.tempo_verde_anterior_segundos,
                decisao.tempo_verde_novo_segundos,
                ajuste_realizado,
                decisao.reducao_fila_estimada_metros,
                decisao.motivo_ajuste[:200],
                decisao.algoritmo_utilizado,
                decisao.eficacia_ajuste
            ))
            
            self.conexao.commit()
            cursor.close()
            
            return True
            
        except psycopg2.Error as e:
            self.conexao.rollback()
            logger.error(f"[ERRO] Falha ao registrar: {str(e)}")
            return False
    
    def processar_ciclo_completo(self) -> Dict[int, DecisaoSemaforo]:
        """
        Executa um ciclo completo de otimização
        
        1. Coleta dados atuais
        2. Toma decisões para cada semáforo
        3. Registra decisões no banco
        4. Retorna sumário
        
        Returns:
            Dict mapeando id_semaforo → DecisaoSemaforo
        """
        
        logger.info("=" * 70)
        logger.info("INICIANDO CICLO DE OTIMIZAÇÃO DE SEMÁFOROS")
        logger.info("=" * 70)
        
        # Etapa 1: Coletar dados
        self.obter_metricas_atuais()
        if not self.metricas_atuais:
            logger.warning("Nenhuma métrica disponível para análise")
            return {}
        
        decisoes = {}
        total_ajustes = 0
        reducao_total = 0
        eficacia_total = 0
        
        # Etapa 2: Tomar decisões
        for id_semaforo, metricas in self.metricas_atuais.items():
            logger.info(f"\nAnalisando: {metricas.nome_cruzamento}")
            logger.info(f"  Via: {metricas}")
            
            # Tomar decisão
            decisao = self.tomar_decisao(metricas)
            decisoes[id_semaforo] = decisao
            
            # Log da decisão
            logger.info(f"  Decisão: {decisao.acao.value.upper()}")
            logger.info(f"  Verde: {decisao.tempo_verde_anterior_segundos}s → {decisao.tempo_verde_novo_segundos}s")
            logger.info(f"  Motivo: {decisao.motivo_ajuste}")
            logger.info(f"  Eficacia esperada: {decisao.eficacia_ajuste:.1f}%")
            
            # Etapa 3: Registrar
            if self.registrar_decisao(decisao):
                if decisao.tempo_verde_novo_segundos != decisao.tempo_verde_anterior_segundos:
                    total_ajustes += 1
                    reducao_total += decisao.reducao_fila_estimada_metros
                    eficacia_total += decisao.eficacia_ajuste
                logger.info(f"  ✓ Registrado com sucesso")
            else:
                logger.warning(f"  ✗ Falha ao registrar")
        
        # Sumário
        logger.info("\n" + "=" * 70)
        logger.info("CICLO CONCLUÍDO")
        logger.info("=" * 70)
        logger.info(f"Semáforos processados: {len(decisoes)}")
        logger.info(f"Ajustes realizados: {total_ajustes}")
        logger.info(f"Redução total estimada de fila: {reducao_total:.0f} metros")
        logger.info(f"Eficacia média esperada: {eficacia_total / len(decisoes) if decisoes else 0:.1f}%")
        logger.info("=" * 70 + "\n")
        
        return decisoes
    
    def obter_relatorio_performance(self) -> Dict:
        """
        Gera relatório de performance do sistema
        
        Returns:
            Dicionário com métricas de performance
        """
        try:
            cursor = self.conexao.cursor()
            
            query = """
                SELECT 
                    COUNT(*) AS total_ciclos,
                    SUM(CASE WHEN ajuste_realizado THEN 1 ELSE 0 END) AS ciclos_ajustados,
                    ROUND(AVG(eficacia_ajuste)::NUMERIC, 2) AS eficacia_media,
                    ROUND(AVG(reducao_fila_estimada_metros)::NUMERIC, 2) AS reducao_media,
                    MAX(data_criacao) AS ultima_atuacao
                FROM fato_ciclo_semaforo
                WHERE data_criacao >= NOW() - INTERVAL '24 hours';
            """
            
            cursor.execute(query)
            row = cursor.fetchone()
            cursor.close()
            
            return {
                'total_ciclos': row[0] or 0,
                'ciclos_ajustados': row[1] or 0,
                'eficacia_media': row[2] or 0,
                'reducao_media_m': row[3] or 0,
                'ultima_atuacao': row[4]
            }
            
        except psycopg2.Error as e:
            logger.error(f"Erro ao gerar relatório: {e}")
            return {}
    
    def fechar(self):
        """Fecha a conexão com o banco de dados"""
        if self.conexao:
            self.conexao.close()
            logger.info("✓ Conexão fechada")

# =====================================================
# FUNÇÃO PRINCIPAL
# =====================================================

def main():
    """Executa a otimização de semáforos"""
    
    otimizador = None
    try:
        otimizador = OtimizadorSemaforos()
        
        # Executar ciclo de otimização
        decisoes = otimizador.processar_ciclo_completo()
        
        # Mostrar relatório de performance
        relatorio = otimizador.obter_relatorio_performance()
        
        print("\n" + "=" * 70)
        print("RELATÓRIO DE PERFORMANCE (últimas 24h)")
        print("=" * 70)
        print(f"Total de ciclos processados: {relatorio['total_ciclos']}")
        print(f"Ciclos com ajuste: {relatorio['ciclos_ajustados']}")
        print(f"Eficacia média: {relatorio['eficacia_media']:.2f}%")
        print(f"Redução média de fila: {relatorio['reducao_media_m']:.1f} metros")
        print(f"Última atuação: {relatorio['ultima_atuacao']}")
        print("=" * 70 + "\n")
        
    except Exception as e:
        logger.error(f"Erro fatal: {str(e)}")
    finally:
        if otimizador:
            otimizador.fechar()

if __name__ == "__main__":
    main()
