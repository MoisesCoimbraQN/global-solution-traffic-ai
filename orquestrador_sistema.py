"""
GLOBAL SOLUTION - CITIZENTECH
Passo 2: Sistema de Orchestração e Monitoramento

Gerencia a execução contínua do algoritmo de otimização de semáforos
e coordena com a coleta de dados em tempo real.

Autor: Global Solution Team
Data: 2026-11-16
"""

import schedule
import time
import os
import logging
from datetime import datetime
from dotenv import load_dotenv
from algoritmo_otimizacao import OtimizadorSemaforos
from coletor_transito_db import ColecionadorTransito

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [%(levelname)s] - %(message)s',
    handlers=[
        logging.FileHandler('sistema_trafico.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Carregar ambiente
load_dotenv()

class SistemaTrafegoInteligente:
    """
    Orquestra o sistema completo de tráfego inteligente
    
    Fluxo:
    1. Coleta dados de tráfego (a cada 5 min)
    2. Otimiza semáforos (a cada 10 min)
    3. Monitora performance (a cada 30 min)
    """
    
    def __init__(self):
        """Inicializa o sistema"""
        self.coletor = None
        self.otimizador = None
        self.inicializar_componentes()
        
        logger.info("╔" + "=" * 68 + "╗")
        logger.info("║" + " " * 10 + "SISTEMA DE TRÁFEGO INTELIGENTE INICIALIZADO" + " " * 14 + "║")
        logger.info("╚" + "=" * 68 + "╝")
    
    def inicializar_componentes(self):
        """Inicializa coletor e otimizador"""
        try:
            logger.info("Inicializando componentes do sistema...")
            self.coletor = ColecionadorTransito()
            self.otimizador = OtimizadorSemaforos()
            logger.info("✓ Componentes inicializados com sucesso")
        except Exception as e:
            logger.error(f"✗ Erro ao inicializar: {str(e)}")
            raise
    
    def tarefa_coleta_dados(self):
        """Tarefa: Coleta de dados de tráfego (a cada 5 minutos)"""
        logger.info("\n" + "─" * 70)
        logger.info("TAREFA: Coleta de Dados de Tráfego")
        logger.info("─" * 70)
        
        try:
            self.coletor.coletar_e_armazenar()
            logger.info("✓ Coleta concluída com sucesso")
        except Exception as e:
            logger.error(f"✗ Erro na coleta: {str(e)}")
    
    def tarefa_otimizacao(self):
        """Tarefa: Otimização de semáforos (a cada 10 minutos)"""
        logger.info("\n" + "─" * 70)
        logger.info("TAREFA: Otimização de Semáforos")
        logger.info("─" * 70)
        
        try:
            decisoes = self.otimizador.processar_ciclo_completo()
            
            if decisoes:
                total_ajustes = sum(
                    1 for d in decisoes.values() 
                    if d.tempo_verde_novo_segundos != d.tempo_verde_anterior_segundos
                )
                logger.info(f"✓ Processados {len(decisoes)} semáforos ({total_ajustes} ajustes)")
            else:
                logger.warning("Nenhum semáforo processado")
                
        except Exception as e:
            logger.error(f"✗ Erro na otimização: {str(e)}")
    
    def tarefa_monitoramento(self):
        """Tarefa: Monitoramento de performance (a cada 30 minutos)"""
        logger.info("\n" + "─" * 70)
        logger.info("TAREFA: Monitoramento de Performance")
        logger.info("─" * 70)
        
        try:
            relatorio = self.otimizador.obter_relatorio_performance()
            
            logger.info("RELATÓRIO DE PERFORMANCE (últimas 24h):")
            logger.info(f"  • Total de ciclos: {relatorio['total_ciclos']}")
            logger.info(f"  • Ciclos com ajuste: {relatorio['ciclos_ajustados']}")
            logger.info(f"  • Eficacia média: {relatorio['eficacia_media']:.2f}%")
            logger.info(f"  • Redução média de fila: {relatorio['reducao_media_m']:.1f}m")
            logger.info(f"  • Última atuação: {relatorio['ultima_atuacao']}")
            
        except Exception as e:
            logger.error(f"✗ Erro ao monitorar: {str(e)}")
    
    def agendar_tarefas(self):
        """Agenda as tarefas periódicas"""
        logger.info("\nAgendando tarefas periódicas...")
        
        # Coleta de dados: a cada 5 minutos
        schedule.every(5).minutes.do(self.tarefa_coleta_dados)
        logger.info("  ✓ Coleta agendada (a cada 5 min)")
        
        # Otimização de semáforos: a cada 10 minutos
        schedule.every(10).minutes.do(self.tarefa_otimizacao)
        logger.info("  ✓ Otimização agendada (a cada 10 min)")
        
        # Monitoramento: a cada 30 minutos
        schedule.every(30).minutes.do(self.tarefa_monitoramento)
        logger.info("  ✓ Monitoramento agendado (a cada 30 min)")
        
        logger.info("\nAgendamento completo. Aguardando primeira execução...")
    
    def iniciar_loop_principal(self):
        """Inicia o loop principal de agendamento"""
        logger.info("\n" + "╔" + "=" * 68 + "╗")
        logger.info("║" + " " * 20 + "INICIANDO LOOP PRINCIPAL" + " " * 25 + "║")
        logger.info("║" + " " * 10 + f"Horário: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}" + " " * 40 + "║")
        logger.info("║" + " " * 15 + "Pressione Ctrl+C para parar" + " " * 27 + "║")
        logger.info("╚" + "=" * 68 + "╝" + "\n")
        
        try:
            while True:
                schedule.run_pending()
                time.sleep(30)  # Verificar agenda a cada 30 segundos
        
        except KeyboardInterrupt:
            logger.info("\n\n" + "╔" + "=" * 68 + "╗")
            logger.info("║" + " " * 20 + "ENCERRANDO SISTEMA" + " " * 31 + "║")
            logger.info("║" + " " * 10 + f"Horário: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}" + " " * 40 + "║")
            logger.info("╚" + "=" * 68 + "╝" + "\n")
            self.encerrar()
    
    def encerrar(self):
        """Encerra o sistema corretamente"""
        try:
            if self.coletor:
                self.coletor.fechar()
            if self.otimizador:
                self.otimizador.fechar()
            logger.info("✓ Sistema encerrado com sucesso")
        except Exception as e:
            logger.error(f"✗ Erro ao encerrar: {str(e)}")

def main():
    """Função principal"""
    
    # Criar sistema
    sistema = SistemaTrafegoInteligente()
    
    # Agendar tarefas
    sistema.agendar_tarefas()
    
    # Iniciar execução imediata das tarefas para primeiro teste
    logger.info("\nExecutando primeira rodada de tarefas...")
    sistema.tarefa_coleta_dados()
    time.sleep(5)
    sistema.tarefa_otimizacao()
    
    # Iniciar loop principal
    sistema.iniciar_loop_principal()

if __name__ == "__main__":
    main()
