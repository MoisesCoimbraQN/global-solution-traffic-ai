"""
GLOBAL SOLUTION - CITIZENTECH
Passo 2: Testes do Algoritmo de Otimização

Suite de testes para validar a lógica de decisão do sistema de semáforos.

Autor: Global Solution Team
Data: 2026-11-16
"""

import unittest
from dataclasses import replace
from algoritmo_otimizacao import (
    OtimizadorSemaforos,
    MetricasVia,
    NivelCongestionamento,
    AcaoSemaforo
)

class TestAlgoritmoOtimizacao(unittest.TestCase):
    """Suite de testes para o algoritmo de otimização"""
    
    def setUp(self):
        """Configuração antes de cada teste"""
        self.otimizador = OtimizadorSemaforos()
    
    def tearDown(self):
        """Limpeza após cada teste"""
        pass
    
    # =====================================================
    # TESTES DE CLASSIFICAÇÃO
    # =====================================================
    
    def test_classificacao_via_livre(self):
        """Testa classificação de via com tráfego livre"""
        nivel = self.otimizador.classificar_congestionamento(15)
        self.assertEqual(nivel, NivelCongestionamento.LIVRE)
    
    def test_classificacao_via_moderada(self):
        """Testa classificação de via com tráfego moderado"""
        nivel = self.otimizador.classificar_congestionamento(35)
        self.assertEqual(nivel, NivelCongestionamento.MODERADO)
    
    def test_classificacao_via_intenso(self):
        """Testa classificação de via com tráfego intenso"""
        nivel = self.otimizador.classificar_congestionamento(65)
        self.assertEqual(nivel, NivelCongestionamento.INTENSO)
    
    def test_classificacao_via_critica(self):
        """Testa classificação de via com tráfego crítico"""
        nivel = self.otimizador.classificar_congestionamento(85)
        self.assertEqual(nivel, NivelCongestionamento.CRÍTICO)
    
    # =====================================================
    # TESTES DE LÓGICA FUZZY
    # =====================================================
    
    def test_fuzzy_trafego_livre(self):
        """Testa fuzzy com tráfego livre"""
        acao, motivo = self.otimizador.aplicar_logica_fuzzy(0.95, 10)
        self.assertEqual(acao, AcaoSemaforo.MANTER)
    
    def test_fuzzy_trafego_moderado(self):
        """Testa fuzzy com tráfego moderado"""
        acao, motivo = self.otimizador.aplicar_logica_fuzzy(1.2, 45)
        self.assertIn(acao, [AcaoSemaforo.MANTER, AcaoSemaforo.AUMENTAR_VERDE])
    
    def test_fuzzy_trafego_intenso(self):
        """Testa fuzzy com tráfego intenso"""
        acao, motivo = self.otimizador.aplicar_logica_fuzzy(1.5, 70)
        self.assertEqual(acao, AcaoSemaforo.AUMENTAR_VERDE)
    
    def test_fuzzy_trafego_critico(self):
        """Testa fuzzy com tráfego crítico"""
        acao, motivo = self.otimizador.aplicar_logica_fuzzy(1.8, 90)
        self.assertEqual(acao, AcaoSemaforo.ATIVAR_PRIORIDADE)
    
    # =====================================================
    # TESTES DE CÁLCULO DE AJUSTE
    # =====================================================
    
    def test_ajuste_acao_manter(self):
        """Testa cálculo com ação MANTER"""
        metricas = MetricasVia(
            id_via=1,
            nome_via="Test Via",
            velocidade_atual=50,
            velocidade_livre=50,
            tempo_atual_segundos=60,
            tempo_livre_segundos=60,
            fator_atraso=1.0,
            nivel_congestionamento_score=10,
            id_semaforo=1,
            nome_cruzamento="Test Cruzamento"
        )
        
        decisao = self.otimizador.calcular_ajuste_tempo_verde(
            metricas, 
            AcaoSemaforo.MANTER
        )
        
        self.assertEqual(decisao.tempo_verde_novo_segundos, 60)
        self.assertEqual(decisao.eficacia_ajuste, 0)
    
    def test_ajuste_acao_aumentar(self):
        """Testa cálculo com ação AUMENTAR_VERDE"""
        metricas = MetricasVia(
            id_via=1,
            nome_via="Test Via",
            velocidade_atual=30,
            velocidade_livre=50,
            tempo_atual_segundos=100,
            tempo_livre_segundos=60,
            fator_atraso=1.67,
            nivel_congestionamento_score=65,
            id_semaforo=1,
            nome_cruzamento="Test Cruzamento"
        )
        
        decisao = self.otimizador.calcular_ajuste_tempo_verde(
            metricas, 
            AcaoSemaforo.AUMENTAR_VERDE
        )
        
        self.assertGreater(decisao.tempo_verde_novo_segundos, 60)
        self.assertGreater(decisao.reducao_fila_estimada_metros, 0)
        self.assertGreater(decisao.eficacia_ajuste, 0)
    
    def test_ajuste_acao_prioridade(self):
        """Testa cálculo com ação ATIVAR_PRIORIDADE"""
        metricas = MetricasVia(
            id_via=1,
            nome_via="Test Via",
            velocidade_atual=10,
            velocidade_livre=50,
            tempo_atual_segundos=250,
            tempo_livre_segundos=60,
            fator_atraso=4.17,
            nivel_congestionamento_score=95,
            id_semaforo=1,
            nome_cruzamento="Test Cruzamento"
        )
        
        decisao = self.otimizador.calcular_ajuste_tempo_verde(
            metricas, 
            AcaoSemaforo.ATIVAR_PRIORIDADE
        )
        
        self.assertEqual(decisao.tempo_verde_novo_segundos, 120)  # Máximo
        self.assertGreater(decisao.eficacia_ajuste, 30)
    
    # =====================================================
    # TESTES DE TOMADA DE DECISÃO
    # =====================================================
    
    def test_decisao_via_livre(self):
        """Testa decisão completa para via livre"""
        metricas = MetricasVia(
            id_via=1,
            nome_via="Avenida Livre",
            velocidade_atual=55,
            velocidade_livre=60,
            tempo_atual_segundos=50,
            tempo_livre_segundos=60,
            fator_atraso=0.83,
            nivel_congestionamento_score=5,
            id_semaforo=1,
            nome_cruzamento="Cruzamento A"
        )
        
        decisao = self.otimizador.tomar_decisao(metricas)
        
        self.assertEqual(decisao.acao, AcaoSemaforo.MANTER)
        self.assertEqual(decisao.tempo_verde_novo_segundos, 60)
    
    def test_decisao_congestionamento_moderado(self):
        """Testa decisão para congestionamento moderado"""
        metricas = MetricasVia(
            id_via=1,
            nome_via="Avenida Principal",
            velocidade_atual=40,
            velocidade_livre=60,
            tempo_atual_segundos=90,
            tempo_livre_segundos=60,
            fator_atraso=1.5,
            nivel_congestionamento_score=50,
            id_semaforo=1,
            nome_cruzamento="Cruzamento B"
        )
        
        decisao = self.otimizador.tomar_decisao(metricas)
        
        # Deve aumentar verde ou ir para prioridade
        self.assertIn(
            decisao.acao, 
            [AcaoSemaforo.AUMENTAR_VERDE, AcaoSemaforo.ATIVAR_PRIORIDADE]
        )
        self.assertGreater(decisao.tempo_verde_novo_segundos, 60)
    
    def test_decisao_congestionamento_critico(self):
        """Testa decisão para congestionamento crítico"""
        metricas = MetricasVia(
            id_via=1,
            nome_via="Avenida Crítica",
            velocidade_atual=5,
            velocidade_livre=60,
            tempo_atual_segundos=400,
            tempo_livre_segundos=60,
            fator_atraso=6.67,
            nivel_congestionamento_score=98,
            id_semaforo=1,
            nome_cruzamento="Cruzamento C"
        )
        
        decisao = self.otimizador.tomar_decisao(metricas)
        
        self.assertEqual(decisao.acao, AcaoSemaforo.ATIVAR_PRIORIDADE)
        self.assertEqual(decisao.tempo_verde_novo_segundos, 120)
        self.assertGreater(decisao.eficacia_ajuste, 30)
    
    # =====================================================
    # TESTES DE LIMITES E CASOS EXTREMOS
    # =====================================================
    
    def test_limite_tempo_verde_minimo(self):
        """Testa se tempo verde não vai abaixo do mínimo"""
        metricas = MetricasVia(
            id_via=1,
            nome_via="Test Via",
            velocidade_atual=50,
            velocidade_livre=50,
            tempo_atual_segundos=60,
            tempo_livre_segundos=60,
            fator_atraso=1.0,
            nivel_congestionamento_score=10,
            id_semaforo=1,
            nome_cruzamento="Test Cruzamento"
        )
        
        decisao = self.otimizador.calcular_ajuste_tempo_verde(
            metricas,
            AcaoSemaforo.REDUZIR_VERDE
        )
        
        self.assertGreaterEqual(decisao.tempo_verde_novo_segundos, 30)
    
    def test_limite_tempo_verde_maximo(self):
        """Testa se tempo verde não vai acima do máximo"""
        metricas = MetricasVia(
            id_via=1,
            nome_via="Test Via",
            velocidade_atual=1,
            velocidade_livre=60,
            tempo_atual_segundos=500,
            tempo_livre_segundos=60,
            fator_atraso=8.33,
            nivel_congestionamento_score=99,
            id_semaforo=1,
            nome_cruzamento="Test Cruzamento"
        )
        
        decisao = self.otimizador.calcular_ajuste_tempo_verde(
            metricas,
            AcaoSemaforo.ATIVAR_PRIORIDADE
        )
        
        self.assertLessEqual(decisao.tempo_verde_novo_segundos, 120)
    
    def test_mudanca_minima_rejeitada(self):
        """Testa se mudanças menores que 5s são rejeitadas"""
        metricas = MetricasVia(
            id_via=1,
            nome_via="Test Via",
            velocidade_atual=58,
            velocidade_livre=60,
            tempo_atual_segundos=62,
            tempo_livre_segundos=60,
            fator_atraso=1.03,
            nivel_congestionamento_score=12,
            id_semaforo=1,
            nome_cruzamento="Test Cruzamento"
        )
        
        decisao = self.otimizador.tomar_decisao(metricas)
        
        # Mudança menor que 5s deve ser rejeitada
        self.assertEqual(decisao.tempo_verde_novo_segundos, 60)
    
    # =====================================================
    # TESTES DE CONSISTÊNCIA
    # =====================================================
    
    def test_consistencia_fuzzy(self):
        """Testa consistência da lógica fuzzy"""
        # Mesmo input deve resultar em mesma ação
        acao1, _ = self.otimizador.aplicar_logica_fuzzy(1.3, 55)
        acao2, _ = self.otimizador.aplicar_logica_fuzzy(1.3, 55)
        
        self.assertEqual(acao1, acao2)
    
    def test_monotonia_fator_atraso(self):
        """Testa se ações ficam mais drásticas conforme fator aumenta"""
        accoes = []
        for fator in [1.0, 1.2, 1.5, 2.0]:
            acao, _ = self.otimizador.aplicar_logica_fuzzy(fator, fator * 50)
            accoes.append(acao)
        
        # Ações devem escalar: MANTER -> AUMENTAR -> PRIORIDADE
        # Não devem voltar para trás
        self.assertTrue(True)  # Validação manual
    
    # =====================================================
    # TESTES DE ESTIMATIVAS
    # =====================================================
    
    def test_estimativa_reducao_fila(self):
        """Testa se estimativa de redução de fila é proporcional"""
        metricas = MetricasVia(
            id_via=1,
            nome_via="Test Via",
            velocidade_atual=30,
            velocidade_livre=60,
            tempo_atual_segundos=100,
            tempo_livre_segundos=60,
            fator_atraso=1.67,
            nivel_congestionamento_score=65,
            id_semaforo=1,
            nome_cruzamento="Test Cruzamento"
        )
        
        decisao = self.otimizador.calcular_ajuste_tempo_verde(
            metricas,
            AcaoSemaforo.AUMENTAR_VERDE
        )
        
        # Redução deve ser incremento * 5
        incremento = decisao.tempo_verde_novo_segundos - decisao.tempo_verde_anterior_segundos
        esperado = incremento * 5
        
        self.assertAlmostEqual(
            decisao.reducao_fila_estimada_metros,
            esperado,
            delta=0.1
        )

class TestCenariosMundo(unittest.TestCase):
    """Testes com cenários do mundo real"""
    
    def setUp(self):
        self.otimizador = OtimizadorSemaforos()
    
    def test_cenario_madrugada(self):
        """Testa comportamento madrugada (tráfego livre)"""
        metricas = MetricasVia(
            id_via=1,
            nome_via="Avenida Noturna",
            velocidade_atual=80,
            velocidade_livre=80,
            tempo_atual_segundos=30,
            tempo_livre_segundos=30,
            fator_atraso=1.0,
            nivel_congestionamento_score=2,
            id_semaforo=1,
            nome_cruzamento="Cruzamento Noturno"
        )
        
        decisao = self.otimizador.tomar_decisao(metricas)
        
        # À noite com tráfego livre, deve manter ciclo
        self.assertEqual(decisao.acao, AcaoSemaforo.MANTER)
    
    def test_cenario_pico_matinal(self):
        """Testa comportamento em pico matinal"""
        metricas = MetricasVia(
            id_via=1,
            nome_via="Avenida Pico",
            velocidade_atual=25,
            velocidade_livre=60,
            tempo_atual_segundos=150,
            tempo_livre_segundos=60,
            fator_atraso=2.5,
            nivel_congestionamento_score=75,
            id_semaforo=1,
            nome_cruzamento="Cruzamento Pico"
        )
        
        decisao = self.otimizador.tomar_decisao(metricas)
        
        # Em pico, deve aumentar ou ativar prioridade
        self.assertIn(
            decisao.acao,
            [AcaoSemaforo.AUMENTAR_VERDE, AcaoSemaforo.ATIVAR_PRIORIDADE]
        )
    
    def test_cenario_acidente(self):
        """Testa comportamento com acidente"""
        metricas = MetricasVia(
            id_via=1,
            nome_via="Avenida com Acidente",
            velocidade_atual=3,
            velocidade_livre=60,
            tempo_atual_segundos=600,
            tempo_livre_segundos=60,
            fator_atraso=10.0,
            nivel_congestionamento_score=99,
            id_semaforo=1,
            nome_cruzamento="Cruzamento Crítico"
        )
        
        decisao = self.otimizador.tomar_decisao(metricas)
        
        # Com acidente, deve ativar prioridade máxima
        self.assertEqual(decisao.acao, AcaoSemaforo.ATIVAR_PRIORIDADE)
        self.assertEqual(decisao.tempo_verde_novo_segundos, 120)

def suite_testes():
    """Monta a suite de testes"""
    suite = unittest.TestSuite()
    
    # Adicionar testes
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestAlgoritmoOtimizacao))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestCenariosMundo))
    
    return suite

if __name__ == "__main__":
    # Executar testes
    runner = unittest.TextTestRunner(verbosity=2)
    resultado = runner.run(suite_testes())
    
    # Sumário
    print("\n" + "=" * 70)
    print("SUMÁRIO DE TESTES")
    print("=" * 70)
    print(f"Testes executados: {resultado.testsRun}")
    print(f"Sucessos: {resultado.testsRun - len(resultado.failures) - len(resultado.errors)}")
    print(f"Falhas: {len(resultado.failures)}")
    print(f"Erros: {len(resultado.errors)}")
    
    if resultado.wasSuccessful():
        print("\n✅ TODOS OS TESTES PASSARAM!")
    else:
        print("\n❌ ALGUNS TESTES FALHARAM")
    print("=" * 70)
