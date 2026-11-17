# 🚌 Sistema de Monitoramento de Múltiplas Rotas de Ônibus - COMPLETO

## ✅ Implementação Concluída

Você agora tem **6 rotas de ônibus** monitoradas simultaneamente no CitizenTech, dando a impressão de que o sistema está calculando/monitorando múltiplos semáforos em tempo real.

---

## 📍 Rotas Implementadas

| ID | Rota | Linha | Status |
|:---:|------|-------|--------|
| 1 | Praça Liberdade → Funcionários | BRT-301 | ✓ Ativa |
| 2 | Savassi → Centro | BRT-302 | ✓ Ativa |
| 3 | Lourdes → Pampulha | BRT-303 | ✓ Ativa |
| 4 | Belvedere → Barroca | BRT-304 | ✓ Ativa |
| 5 | Santa Efigênia → Floresta | BRT-305 | ✓ Ativa |
| 6 | São Luíz → Contorno | BRT-306 | ✓ Ativa |

---

## 🎯 Funcionalidades Implementadas

### 1️⃣ **Mapa Estático com Múltiplas Rotas**
- **URL**: `/dashboard/mapa-multiplas-rotas`
- **Arquivo**: `mapa_multiplas_rotas.html`
- **Features**:
  - 6 rotas com cores diferentes
  - Marcadores para: início (verde), semáforos (coloridos), destino (vermelho)
  - Popups com informações de cada ponto
  - Tooltips ao hover
  - Layer de tráfego do TomTom
  - Legenda interativa

### 2️⃣ **Mapa Dinâmico com Atualização em Tempo Real**
- **URL**: `/dashboard/mapa-dinamico`
- **Arquivo**: `mapa_multiplas_rotas_dinamico.html`
- **Features**:
  - Atualização automática a cada **5 segundos** via API
  - Painel de métricas globais (rotas ativas, semáforos, velocidade, congestão)
  - Dados em tempo real: velocidade, atraso, congestão por rota
  - Status de cada rota (fluindo, ativo, congestionado)
  - Contador de atualizações
  - Totalizador de passageiros transportados

---

## 🔌 APIs Implementadas

### **GET `/api/rotas`**
Retorna dados de todas as 6 rotas com atualização de dados (variação aleatória simulando dados reais).

**Resposta Exemplo**:
```json
{
  "status": "sucesso",
  "timestamp": "2026-11-17T07:00:54.123456",
  "total_rotas": 6,
  "rotas": [
    {
      "id": 1,
      "nome": "Rota 1: Praça Liberdade → Funcionários",
      "linha": "BRT-301",
      "inicio": "Praça da Liberdade",
      "destino": "Funcionários",
      "cor": "#3498db",
      "velocidade_media": 23.6,
      "atraso_segundos": 158,
      "congestao": 45,
      "semaforos_total": 3,
      "semaforos_otimizados": 2,
      "passageiros_transportados": 1250,
      "status": "ativo"
    },
    // ... 5 rotas adicionais
  ],
  "metricas_globais": {
    "velocidade_media_geral": 25.13,
    "congestao_media_geral": 42.17,
    "total_passageiros": 10290,
    "semaforos_total": 18,
    "semaforos_otimizados_total": 13
  }
}
```

### **GET `/api/rota/<id>`**
Retorna detalhes específicos de uma rota com dados de semáforos individuais.

**Exemplo**: `GET /api/rota/1`

```json
{
  "status": "sucesso",
  "timestamp": "2026-11-17T07:00:54.123456",
  "rota_id": 1,
  "nome": "Rota 1: Praça Liberdade → Funcionários",
  "semaforos": [
    {
      "id": 1,
      "nome": "Semáforo Av. Afonso Pena",
      "tempo_ciclo": 90,
      "tempo_atual": 23,
      "status": "verde",
      "fluxo": "otimizado"
    },
    // ... 2 semáforos adicionais
  ],
  "total_semaforos": 3
}
```

---

## 🌐 URLs de Acesso

| Funcionalidade | URL | Descrição |
|---|---|---|
| **Home** | `http://localhost:5000/` | Página inicial com links |
| **Mapa Único** | `http://localhost:5000/dashboard/mapa` | Rota original com 1 via |
| **Múltiplas Rotas (Estático)** | `http://localhost:5000/dashboard/mapa-multiplas-rotas` | 6 rotas, sem atualização |
| **Múltiplas Rotas (Dinâmico)** | `http://localhost:5000/dashboard/mapa-dinamico` | 6 rotas com atualização em tempo real |
| **Dashboard Completo** | `http://localhost:5000/dashboard/completo` | Visão geral com métricas |
| **API de Rotas** | `http://localhost:5000/api/rotas` | JSON de todas as rotas |
| **API Rota Específica** | `http://localhost:5000/api/rota/1` | JSON de rota 1 |

---

## 📊 Dados Monitorados por Rota

Cada rota fornece:
- ✓ **Velocidade Média** (km/h)
- ✓ **Atraso** (segundos)
- ✓ **Congestão** (%)
- ✓ **Semáforos Totais** e **Otimizados**
- ✓ **Passageiros Transportados**
- ✓ **Status** (fluindo/ativo/congestionado)

**Dados por Rota**:
- Rota 1: 23.6 km/h, 158s atraso, 45% congestão, 1250 passageiros
- Rota 2: 18.4 km/h, 345s atraso, 72% congestão, 2100 passageiros
- Rota 3: 28.9 km/h, 72s atraso, 28% congestão, 980 passageiros
- Rota 4: 32.1 km/h, 45s atraso, 15% congestão, 750 passageiros
- Rota 5: 26.5 km/h, 128s atraso, 38% congestão, 1620 passageiros
- Rota 6: 21.3 km/h, 203s atraso, 55% congestão, 1890 passageiros

---

## 🔄 Atualização de Dados

### **Mapa Dinâmico**
- Atualiza **a cada 5 segundos**
- Busca dados da API `/api/rotas`
- Atualiza cores dos marcadores baseado em velocidade
- Atualiza painel de métricas globais
- Atualiza lista de rotas com status

### **Semáforos**
Cada rota tem **3 semáforos**:
- **Semáforo 1** (início da rota)
- **Semáforo 2** (intermediário)
- **Semáforo 3** (fim/entrada para destino)

Total: **18 semáforos** sendo monitorados em tempo real

---

## 📋 Arquivos Criados/Modificados

| Arquivo | Tipo | Descrição |
|---------|------|-----------|
| `mapa_multiplas_rotas.html` | ✨ Novo | Mapa estático com 6 rotas |
| `mapa_multiplas_rotas_dinamico.html` | ✨ Novo | Mapa dinâmico com atualização a cada 5s |
| `app.py` | 📝 Modificado | Adicionadas rotas de dashboard e APIs |

---

## 🚀 Como Usar

### **1. Iniciar o Servidor**
```bash
cd c:\Users\mcmoi\OneDrive\Área de Trabalho\GlobalSolution
python app.py
```

### **2. Acessar a Página Inicial**
Abra no navegador: **`http://localhost:5000/`**

Você verá cards com links para:
- Dashboard Completo
- Dashboard Principal
- Mapa Interativo (original)
- **Múltiplas Rotas (Estático)** ← NOVO
- **Múltiplas Rotas (Dinâmico)** ← NOVO

### **3. Testar a API**
```bash
# Todas as rotas
curl http://localhost:5000/api/rotas

# Rota específica (1-6)
curl http://localhost:5000/api/rota/1
```

---

## 🎨 Cores das Rotas

| Rota | Cor | Hexadecimal |
|------|-----|-------------|
| 1 | Azul | #3498db |
| 2 | Vermelho | #e74c3c |
| 3 | Roxo | #9b59b6 |
| 4 | Verde-Água | #1abc9c |
| 5 | Amarelo | #f1c40f |
| 6 | Verde-Escuro | #16a085 |

---

## 📊 Legenda do Mapa

| Cor | Status | Velocidade |
|-----|--------|-----------|
| 🟢 Verde | Fluxo Livre | > 30 km/h |
| 🟡 Amarelo | Fluxo Moderado | 15-30 km/h |
| 🔴 Vermelho | Congestionado | < 15 km/h |

---

## ✨ Próximos Passos (Opcional)

1. **Expandir o Banco de Dados**
   - Adicionar tabelas para múltiplas vias (via_id 1-6)
   - Associar dados reais de tráfego a cada rota

2. **Integração com AWS DynamoDB**
   - Armazenar histórico de dados por rota
   - Dashboard com gráficos históricos

3. **Notificações em Tempo Real**
   - Alertas quando congestão ultrapassa limite
   - WebSockets para atualização instantânea

4. **Mobile App**
   - Aplicativo React Native
   - Acesso às rotas e semáforos em tempo real

---

## 🎯 Demonstração

A implementação atual **simula perfeitamente** o monitoramento de múltiplos semáforos simultâneos:

✅ 6 rotas de ônibus  
✅ 18 semáforos (3 por rota)  
✅ Dados independentes por rota  
✅ Atualização a cada 5 segundos  
✅ Painel de métricas globais  
✅ Mapa interativo com TomTom Traffic  
✅ API REST para integração  
✅ Cores e status dinâmicos  

---

**Desenvolvido com ❤️ para CitizenTech - Global Solution**
