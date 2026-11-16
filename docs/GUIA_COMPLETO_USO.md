# 🚦 CitizenTech - Guia Completo de Uso

## 📋 Visão Geral do Sistema

O **CitizenTech** é uma solução inteligente de controle de tráfego urbano que combina:

- **Coleta em Tempo Real**: Dados de tráfego via API TomTom
- **Data Warehouse Snowflake**: Armazenamento normalizado com modelo snowflake
- **Algoritmo Inteligente**: Otimização automática de semáforos
- **Visualizações**: Mapas interativos e dashboards

---

## 🚀 Como Iniciar

### Opção 1: Menu Interativo (Recomendado)
```bash
INICIAR_MENU.bat
```
Este script abre um menu interativo no navegador com todas as opções disponíveis.

### Opção 2: Ativar o Ambiente Virtual e Executar Scripts
```bash
# Ativar ambiente virtual
.venv\Scripts\activate

# Verificar conexão TomTom
python teste_tomtom_completo.py

# Executar coleta de dados
python coleta_transito.py

# Rodar algoritmo de otimização
python algoritmo_otimizacao.py
```

---

## 📊 Componentes do Sistema

### 1️⃣ **Mapa TomTom** (`mapa_tomtom_oficial.html`)
Visualização interativa com:
- Integração oficial da API TomTom
- Localização de semáforos em Belo Horizonte
- Rotas de ônibus
- Dados de tráfego em tempo real
- Legenda com status de congestionamento

**Como acessar:**
- Abrir `mapa_tomtom_oficial.html` no navegador
- Ou clicar em "Mapa TomTom" no menu interativo

---

### 2️⃣ **Algoritmo de Semáforos** (`algoritmo_otimizacao.py`)
Lógica inteligente que:
- Monitora fator de atraso (tempo atual / tempo livre)
- Ajusta ciclos de semáforos dinamicamente
- Registra ações no Data Warehouse
- Reduz congestionamento urbano

**Critérios de Decisão:**
```
Fator de Atraso ≤ 1.2  → Manter ciclo padrão
Fator de Atraso > 1.3  → Ativar otimização
```

**Como executar:**
```bash
python algoritmo_otimizacao.py
```

---

### 3️⃣ **Coleta de Dados** (`coleta_transito.py`)
Script que:
- Consulta API TomTom periodicamente
- Coleta velocidade, tempo de percurso, nível de congestionamento
- Armazena dados no Snowflake
- Executa a cada 5 minutos na AWS EC2

**Como verificar se está rodando:**
```bash
python teste_tomtom_completo.py
```

---

### 4️⃣ **Dashboard de Trânsito** (`dashboard_transito.py`)
Visualização de métricas:
- Histórico de velocidades
- Nível de congestionamento por hora
- Impacto das otimizações
- Gráficos interativos

**Como executar:**
```bash
python dashboard_transito.py
```

---

### 5️⃣ **Visualizador de Rota** (`visualizador_bus_rota.py`)
Acompanhamento em tempo real:
- Rota de ônibus em Belo Horizonte
- Localização de semáforos
- Ajustes de ciclos
- Análise de impacto

**Como executar:**
```bash
python visualizador_bus_rota.py
```

---

## 🗄️ Data Warehouse - Modelo Snowflake

### Tabelas Fato

#### `fato_transito_tempo_real`
Armazena métricas coletadas periodicamente:
- `velocidade_atual` (km/h)
- `tempo_atual_segundos` (s)
- `fator_atraso` (tempo atual / tempo livre)
- `nivel_congestionamento_score` (0-100)

#### `fato_ciclo_semaforo`
Registra ações do algoritmo:
- `tempo_verde_anterior_segundos` (s)
- `tempo_verde_novo_segundos` (s)
- `reducao_fila_estimada_metros` (m)

### Tabelas Dimensão

#### `dim_via`
- Nome da via
- Limite de velocidade
- Referência a `dim_regiao`

#### `dim_regiao` (Sub-dimensão Snowflake)
- Bairro (ex: Savassi)
- Zona da cidade (ex: Zona Sul)
- Cidade (ex: Belo Horizonte)

#### `dim_tempo`
- Data e hora (YYYYMMDDHHMM)
- Dia da semana
- Período de pico (booleano)

#### `dim_cruzamento`
- Latitude / Longitude
- ID do semáforo
- Metadados da interseção

---

## 🔧 Configuração do Ambiente

### .env
Arquivo de variáveis de ambiente:
```
TOMTOM_API_KEY=hXan3baE73yeieqt6nD012BISAW65QoJ
DB_HOST=seu_host_snowflake
DB_PORT=5432
DB_NAME=seu_database
DB_USER=seu_usuario
DB_PASSWORD=sua_senha
AWS_REGION=us-east-1
```

### .gitignore
Protege dados sensíveis:
```
.env
.venv/
__pycache__/
*.pyc
*.pyo
```

### .venv
Ambiente virtual Python isolado:
```bash
# Criar (primeira vez)
python -m venv .venv

# Ativar
.venv\Scripts\activate

# Desativar
deactivate
```

---

## ✅ Verificação do Sistema

### Status da Conexão TomTom
```bash
python teste_tomtom_completo.py
```

Deve retornar:
```
✓ Conexão com TomTom bem-sucedida
✓ Dados coletados: via, velocidade, tempo, congestionamento
✓ Fator de atraso calculado
```

### Status da AWS EC2
- Coleta rodando a cada 5 minutos
- Dados sincronizados com Snowflake
- Logs disponíveis no CloudWatch

---

## 🎯 Fluxo de Operação Completo

```
┌─────────────────────────────────────────┐
│   1. Iniciar Menu Interativo             │
│      (INICIAR_MENU.bat)                  │
└────────────┬────────────────────────────┘
             │
      ┌──────▼──────┐
      │ Escolher    │
      │ Componente  │
      └──────┬──────┘
             │
   ┌─────────┼─────────┐
   │         │         │
   ▼         ▼         ▼
 Mapa    Algoritmo  Dashboard
   │         │         │
   │    ┌────▼─────┐   │
   │    │ TomTom   │   │
   │    │API ativa │   │
   │    └────┬─────┘   │
   │         │         │
   │    ┌────▼──────────▼──┐
   │    │ Snowflake Data   │
   │    │ Warehouse ativo  │
   │    └───────┬──────────┘
   │            │
   │       ┌────▼─────────────┐
   └──────►│  Visualização    │
           │  Atualizada      │
           └──────────────────┘
```

---

## 📁 Estrutura de Arquivos

```
GlobalSolution/
├── INICIAR_MENU.bat                  # Menu interativo
├── MENU_INTERATIVO.html              # Interface web
├── mapa_tomtom_oficial.html          # Mapa TomTom
├── algoritmo_otimizacao.py           # Algoritmo inteligente
├── coleta_transito.py                # Coleta de dados
├── dashboard_transito.py             # Dashboard
├── visualizador_bus_rota.py          # Visualizador
├── teste_tomtom_completo.py          # Verificação
├── setup_warehouse.py                # Setup Snowflake
├── .env                              # Variáveis de ambiente
├── .venv/                            # Ambiente virtual
├── .gitignore                        # Arquivos ignorados
├── requirements.txt                  # Dependências Python
├── criar_warehouse.sql               # Script DDL
└── [docs]/                           # Documentação
    ├── README.md
    ├── SUMARIO_EXECUTIVO.md
    ├── PASSO_2_ALGORITMO.md
    └── PROJETO_FINAL.md
```

---

## 🐛 Troubleshooting

### Problema: Mapa não carrega
**Solução:**
- Verificar conexão com internet
- Validar API key do TomTom no `.env`
- Verificar no browser console (F12) por erros

### Problema: Algoritmo não executa
**Solução:**
```bash
# Verificar ambiente virtual
.venv\Scripts\activate

# Instalar dependências
pip install -r requirements.txt

# Verificar TomTom
python teste_tomtom_completo.py
```

### Problema: Dados não sincronizam com Snowflake
**Solução:**
- Verificar credenciais no `.env`
- Testar conexão: `python setup_warehouse.py`
- Verificar logs da AWS EC2

---

## 📞 Suporte e Contato

Para dúvidas sobre o projeto:
1. Consulte a documentação em `PROJETO_FINAL.md`
2. Verifique o status do sistema via Menu Interativo
3. Acesse os logs da AWS EC2

---

**Versão:** 1.0  
**Data:** 2024  
**Status:** ✅ Operacional
