# 🧠 PASSO 2: Algoritmo de Otimização e Controle de Semáforos Inteligentes

## 📋 Visão Geral

O **Passo 2** implementa o "cérebro" da aplicação: um sistema inteligente que:
- ✅ **Analisa** dados de tráfego em tempo real
- ✅ **Toma decisões** automatizadas sobre ajustes de semáforo
- ✅ **Otimiza** fluxo de tráfego
- ✅ **Registra** todas as ações para análise posterior

---

## 🎯 Arquitetura do Sistema

### Fluxo de Dados

```
1. API TomTom/Banco de Dados
   ↓
2. Coletor de Dados (coletor_transito_db.py)
   ↓
3. Algoritmo de Otimização (algoritmo_otimizacao.py)
   ├─ Leitura de Métricas
   ├─ Classificação de Congestionamento
   ├─ Lógica Fuzzy (Tomada de Decisão)
   └─ Cálculo de Ajuste
   ↓
4. Persistência (fato_ciclo_semaforo)
   ↓
5. Orquestrador/Monitoramento (orquestrador_sistema.py)
```

---

## 🔍 3 Etapas Principais

### 1️⃣ LEITURA E AVALIAÇÃO (Monitoramento)

O sistema coleta métricas de tráfego:

**Métricas Calculadas:**
- `fator_atraso` = tempo_atual / tempo_livre
- `nivel_congestionamento_score` = 0-100
- `velocidade_atual` vs `velocidade_livre`

**Classificação do Congestionamento:**
| Nível | Score | Fator de Atraso | Ação Esperada |
|-------|-------|-----------------|---------------|
| **LIVRE** | 0-25 | ≤ 1.0 | Manter ciclo |
| **MODERADO** | 25-50 | 1.0-1.3 | Observar |
| **INTENSO** | 50-75 | 1.3-1.5 | Aumentar verde |
| **CRÍTICO** | 75-100 | > 1.5 | Prioridade máxima |

---

### 2️⃣ TOMADA DE DECISÃO (Heurística + Lógica Fuzzy)

O algoritmo usa **Lógica Fuzzy** para tratamento robusto de incertezas.

#### Lógica Fuzzy Explicada

A Lógica Fuzzy permite que o sistema trabalhe com conceitos "imprecisos":
- Em vez de "congestionado" vs "não congestionado"
- Trabalha com "graus de pertinência" (0-1)

**Exemplo:**
```python
# Fator 1.2 é:
# - Parcialmente "livre" (30% de certeza)
# - Parcialmente "moderado" (70% de certeza)
# - Não é "intenso" (0%)

# Regra Fuzzy:
# IF (moderado) THEN aumentar verde COM CONFIANÇA 0.7
```

#### Regras do Sistema

```
1. Se LIVRE ou MODERADO-LEVE
   → AÇÃO: MANTER ciclo padrão
   → CONFIANÇA: 0.9 (se livre), 0.4 (se moderado-leve)

2. Se MODERADO ou INTENSO
   → AÇÃO: AUMENTAR tempo de verde
   → CONFIANÇA: 0.7 (se moderado), 0.9 (se intenso)

3. Se CRÍTICO
   → AÇÃO: ATIVAR PRIORIDADE (verde máximo)
   → CONFIANÇA: 0.8 (se crítico), 0.3 (se intenso)
```

#### Defuzzificação

O sistema escolhe a ação com **MAIOR CONFIANÇA**:

```python
# Decisão = argmax(confiança para cada ação)
# Exemplo: AUMENTAR_VERDE (confiança=0.9) > MANTER (0.4) > PRIORIDADE (0.3)
# → Resultado: AUMENTAR_VERDE
```

---

### 3️⃣ APLICAÇÃO DO AJUSTE (Ação)

Após decidir a ação, o sistema calcula o ajuste específico:

#### Exemplo 1: Ação = MANTER
```
tempo_verde_anterior: 60s
tempo_verde_novo: 60s
motivo: "Tráfego normal"
eficacia: 0% (nenhuma mudança)
```

#### Exemplo 2: Ação = AUMENTAR_VERDE
```
fator_atraso: 1.5
incremento = (1.5 - 1.0) * 10 = 5 segundos

tempo_verde_anterior: 60s
tempo_verde_novo: 65s (60 + 5)

redução_fila_estimada: 5 * 5 = 25 metros
eficacia: (5 / 120) * 30% = 1.25%

motivo: "Verde estendido em +5s | Redução: 25m"
```

#### Exemplo 3: Ação = ATIVAR_PRIORIDADE
```
tempo_verde_anterior: 60s
tempo_verde_novo: 120s (máximo)

redução_fila_estimada: 60 * 7 = 420 metros
eficacia: 40% (alta eficacia esperada)

motivo: "MODO PRIORITÁRIO | Verde: 120s | Redução: 420m"
```

#### Limites do Sistema
```python
TEMPO_VERDE_MINIMO = 30s      # Nunca abaixo
TEMPO_VERDE_MAXIMO = 120s     # Nunca acima
INCREMENTO_AJUSTE = 10s       # Unidade de ajuste
MUDANCA_MINIMA = 5s           # Rejeitar mudanças < 5s
```

---

## 🔧 Componentes do Código

### 1. `algoritmo_otimizacao.py` (20KB - Principal)

**Classe: OtimizadorSemaforos**

```python
# Inicializar
otimizador = OtimizadorSemaforos()

# Processar ciclo completo
decisoes = otimizador.processar_ciclo_completo()
# Retorna: Dict[id_semaforo → DecisaoSemaforo]

# Obter relatório de performance
relatorio = otimizador.obter_relatorio_performance()
```

**Métodos Principais:**
- `obter_metricas_atuais()` - Coleta dados do banco
- `classificar_congestionamento(score)` - Classifica nível
- `aplicar_logica_fuzzy(fator, score)` - Toma decisão
- `calcular_ajuste_tempo_verde(metricas, acao)` - Calcula ajuste
- `tomar_decisao(metricas)` - Orquestra etapas 1-3
- `registrar_decisao(decisao)` - Persiste em DB
- `processar_ciclo_completo()` - Executa tudo

### 2. `orquestrador_sistema.py` (7KB - Orchestração)

**Classe: SistemaTrafegoInteligente**

Gerencia execução contínua com agendamento:

```python
# Agendar tarefas
- Coleta a cada 5 minutos
- Otimização a cada 10 minutos
- Monitoramento a cada 30 minutos

# Iniciar loop
sistema = SistemaTrafegoInteligente()
sistema.iniciar_loop_principal()
```

### 3. `teste_algoritmo.py` (16KB - Testes)

**Suite de Testes Unitários**

```
✅ Testes de Classificação (4 testes)
✅ Testes de Lógica Fuzzy (4 testes)
✅ Testes de Cálculo de Ajuste (3 testes)
✅ Testes de Decisão (3 testes)
✅ Testes de Limites (3 testes)
✅ Testes de Consistência (2 testes)
✅ Testes de Estimativas (1 teste)
✅ Testes de Cenários Reais (3 testes)

TOTAL: 23 TESTES UNITÁRIOS
```

---

## 📊 Como Usar

### Pré-requisito
Ter completado o **Passo 1** (Data Warehouse e Coleta)

### Opção 1: Execução Única

```bash
python algoritmo_otimizacao.py
```

**Saída:**
```
==================================================
INICIANDO CICLO DE OTIMIZAÇÃO DE SEMÁFOROS
==================================================

Analisando: Praça da Liberdade
  Via: Avenida Afonso Pena | Fator: 1.3 | Score: 52.1
  Decisão: AUMENTAR_VERDE
  Verde: 60s → 70s
  Motivo: Congestionamento moderado | Verde estendido +10s
  Eficacia: 8.3%
  ✓ Registrado com sucesso

Analisando: Av. Getúlio x Rua da Bahia
  Via: Avenida Getúlio Vargas | Fator: 0.95 | Score: 12.3
  Decisão: MANTER
  Verde: 60s → 60s
  Motivo: Tráfego normal
  Eficacia: 0.0%
  ✓ Registrado com sucesso

==================================================
CICLO CONCLUÍDO
==================================================
Semáforos processados: 2
Ajustes realizados: 1
Redução total estimada: 50 metros
Eficacia média: 8.3%
```

### Opção 2: Monitoramento Contínuo

```bash
python orquestrador_sistema.py
```

**Fluxo:**
- Executa coleta de dados (a cada 5 min)
- Otimiza semáforos (a cada 10 min)
- Monitora performance (a cada 30 min)
- Logs em `sistema_trafico.log`

### Opção 3: Testes

```bash
python teste_algoritmo.py
```

**Resultado:**
```
test_ajuste_acao_aumentar ... ok
test_ajuste_acao_manter ... ok
test_ajuste_acao_prioridade ... ok
test_ajuste_mudanca_minima_rejeitada ... ok
test_cenario_acidente ... ok
test_cenario_madrugada ... ok
test_cenario_pico_matinal ... ok
test_classificacao_via_critica ... ok
test_classificacao_via_intenso ... ok
test_classificacao_via_livre ... ok
test_classificacao_via_moderada ... ok
...

Ran 23 tests in 0.234s
OK ✅ TODOS OS TESTES PASSARAM!
```

---

## 📈 Exemplos de Decisões Reais

### Cenário 1: Via Livre (Madrugada)

```
INPUT:
  Via: Avenida Noturna
  Velocidade: 80 km/h (normal: 80 km/h)
  Tempo: 30s (esperado: 30s)
  Fator Atraso: 1.0
  Score: 2/100

PROCESSAMENTO:
  Classificação: LIVRE
  Fuzzy: degree_livre=0.9, degree_moderado=0.1
  Ação Selecionada: MANTER (confiança: 0.9)

DECISION:
  Verde: 60s → 60s (SEM MUDANÇA)
  Eficacia: 0%
  Motivo: "Tráfego normal"
```

### Cenário 2: Pico Matinal

```
INPUT:
  Via: Avenida Pico
  Velocidade: 25 km/h (normal: 60 km/h)
  Tempo: 150s (esperado: 60s)
  Fator Atraso: 2.5
  Score: 75/100

PROCESSAMENTO:
  Classificação: INTENSO (quase crítico)
  Fuzzy: degree_intenso=0.6, degree_critico=0.4
  Ação Selecionada: AUMENTAR_VERDE (confiança: 0.85)

DECISION:
  Verde: 60s → 95s (+35s)
  Redução: 35 * 5 = 175 metros
  Eficacia: 29.2%
  Motivo: "Verde estendido em +35s | Redução: 175m"
```

### Cenário 3: Acidente (Crítico)

```
INPUT:
  Via: Avenida com Acidente
  Velocidade: 3 km/h (normal: 60 km/h)
  Tempo: 600s (esperado: 60s)
  Fator Atraso: 10.0
  Score: 99/100

PROCESSAMENTO:
  Classificação: CRÍTICO
  Fuzzy: degree_critico=0.95
  Ação Selecionada: ATIVAR_PRIORIDADE (confiança: 0.95)

DECISION:
  Verde: 60s → 120s (MÁXIMO)
  Redução: 60 * 7 = 420 metros
  Eficacia: 40%
  Motivo: "MODO PRIORITÁRIO | Verde: 120s | Redução: 420m"
```

---

## 📊 Persistência em Banco de Dados

Cada decisão é registrada em `fato_ciclo_semaforo`:

```sql
-- Ver todas as decisões do último dia
SELECT 
    c.nome_cruzamento,
    f.tempo_verde_anterior_segundos,
    f.tempo_verde_novo_segundos,
    f.ajuste_realizado,
    f.eficacia_ajuste,
    f.motivo_ajuste,
    f.data_criacao
FROM fato_ciclo_semaforo f
JOIN dim_cruzamento c ON f.id_semaforo = c.id_semaforo
WHERE f.data_criacao >= NOW() - INTERVAL '24 hours'
ORDER BY f.data_criacao DESC;
```

---

## 🎓 Conceitos Implementados

### Lógica Fuzzy

Trata incertezas naturais em dados de tráfego:
- Métrica imprecisa (sensor, GPS)
- Comportamento imprevisível (semáforo, peatões)
- Decisão "macia" em vez de rígida

### Heurística Adaptativa

Ajustes proporcionais ao problema:
- Quanto maior fator de atraso, maior ajuste
- Mas sempre respeitando limites físicos
- Rejeita mudanças insignificantes

### Orchestração com Agendamento

Execução coordenada de múltiplas tarefas:
- Coleta, análise e decisão em ciclos
- Monitoramento de performance
- Logs estruturados para auditoria

---

## 🔐 Segurança e Robustez

✅ **Validação de Dados**
- Limites de tempo verde respeitados
- Mudanças mínimas rejeitadas

✅ **Tratamento de Erros**
- Try-except em operações críticas
- Logs de falhas

✅ **Auditoria**
- Cada decisão registrada em banco
- Rastreamento completo de ações

✅ **Performance**
- Índices otimizados em queries
- Processamento rápido

---

## 📈 Métricas de Sucesso

**Que dados analisar:**

```sql
-- Taxa de ajustes
SELECT 
    COUNT(*) AS total_ciclos,
    SUM(CASE WHEN ajuste_realizado THEN 1 ELSE 0 END) AS ajustes,
    ROUND(100.0 * SUM(CASE WHEN ajuste_realizado THEN 1 ELSE 0 END) / COUNT(*), 2) AS taxa_ajuste
FROM fato_ciclo_semaforo
WHERE data_criacao >= NOW() - INTERVAL '7 days';

-- Eficacia média
SELECT 
    ROUND(AVG(eficacia_ajuste), 2) AS eficacia_media,
    MAX(eficacia_ajuste) AS eficacia_maxima,
    ROUND(AVG(reducao_fila_estimada_metros), 2) AS reducao_media
FROM fato_ciclo_semaforo
WHERE data_criacao >= NOW() - INTERVAL '7 days';

-- Impacto por via
SELECT 
    v.nome_via,
    COUNT(*) AS ciclos,
    ROUND(AVG(f.eficacia_ajuste), 2) AS eficacia,
    SUM(f.reducao_fila_estimada_metros) AS reducao_total
FROM fato_ciclo_semaforo f
JOIN dim_cruzamento c ON f.id_semaforo = c.id_semaforo
JOIN dim_via v ON c.id_via_principal = v.id_via
WHERE f.data_criacao >= NOW() - INTERVAL '7 days'
GROUP BY v.id_via, v.nome_via
ORDER BY eficacia DESC;
```

---

## 🚀 Próximas Melhorias

- [ ] Machine Learning para aprender padrões históricos
- [ ] Integração com dados de eventos (shows, jogos)
- [ ] Comunicação com semáforos reais (via API/MQTT)
- [ ] Dashboard de visualização em tempo real
- [ ] Alertas para situações críticas
- [ ] Análise preditiva de congestionamento

---

## 📞 Suporte

**Arquivos Principais:**
- `algoritmo_otimizacao.py` - Algoritmo core
- `orquestrador_sistema.py` - Orchestração
- `teste_algoritmo.py` - Testes
- `queries_uteis.sql` - Análises SQL

**Executar:**
```bash
# Teste rápido
python teste_algoritmo.py

# Execução única
python algoritmo_otimizacao.py

# Monitoramento contínuo
python orquestrador_sistema.py
```

---

**Global Solution - CitizenTech Passo 2**  
*Inteligência para Tráfego Urbano*
