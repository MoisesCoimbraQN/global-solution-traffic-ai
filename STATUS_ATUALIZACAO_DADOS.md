# 📊 Status de Atualização de Dados - Dashboards

## ⚠️ Situação Atual

**Banco de Dados AWS**: ❌ **NÃO CONECTADO**

```
Erro: could not translate host name "ip-172-31-33-147.us-east-2.compute.internallocalhost"
Causa: Host do banco está malformado no .env
```

## 🔄 Como os Dados São Atualizados

### Fluxo Atual (MODO SIMULAÇÃO)

```
Orquestrador (5min)  →  Coleta Dados (TomTom)  →  API Flask  →  Dashboards
Sistema roda localmente com dados fake quando banco não conecta
```

### Fluxo Quando AWS Estiver OK (MODO PRODUÇÃO)

```
Orquestrador (5min)  →  Coleta Dados (TomTom)  →  Insere no PostgreSQL AWS  →  API Flask  →  Dashboards (auto-refresh 30s)
```

---

## 🔧 O Que Precisa Ser Feito

### Passo 1: Corrigir Credenciais do Banco

Verifique o `.env` e corrija:

```env
# ERRADO (como está):
DB_HOST=ip-172-31-33-147.us-east-2.compute.internallocalhost

# CORRETO deve ser algo assim:
DB_HOST=ip-172-31-33-147.us-east-2.compute.amazonaws.com
# OU
DB_HOST=seu-banco-rds.c9akciq32.us-east-2.rds.amazonaws.com
```

### Passo 2: Verificar Segurança no RDS da AWS

No Console AWS → RDS:
1. Verifique o endpoint exato do banco
2. Verifique o Security Group (porta 5432 aberta)
3. Verifique credenciais (user/password)
4. Teste ping: `ping seu-host.amazonaws.com`

### Passo 3: Testar Conexão

```powershell
# Testar conexão local
python -c "
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
print('[OK] Banco conectado!')
conn.close()
"
```

### Passo 4: Iniciar Orquestrador

```powershell
python orquestrador_sistema.py
```

Vai coletar dados a cada 5 minutos e inserir no banco.

---

## 🌐 APIs Disponíveis no Flask

Acesse em `http://localhost:5000`:

| Endpoint | O quê |
|----------|-------|
| `GET /` | Home com cards dos dashboards |
| `GET /dashboard/completo` | Dashboard Completo (HTML estático) |
| `GET /dashboard/principal` | Dashboard Principal (HTML estático) |
| `GET /dashboard/mapa` | Mapa Interativo (HTML estático) |
| `GET /api/metricas` | JSON com métricas (atualizado a cada request) |
| `GET /api/status-banco` | Status de conexão com AWS |

### Exemplo: Verificar Status do Banco

```bash
curl http://localhost:5000/api/status-banco
```

**Resposta quando AWS conecta:**
```json
{
  "banco_conectado": true,
  "mensagem": "Banco de dados AWS conectado com sucesso",
  "dashboards_atualizando": true
}
```

**Resposta quando não conecta:**
```json
{
  "banco_conectado": false,
  "mensagem": "Banco de dados AWS não está acessível. Sistema em modo simulação.",
  "dashboards_atualizando": false
}
```

---

## 📈 Próxima Etapa: Auto-Refresh nos Dashboards

Para fazer os dashboards HTML atualizarem **automaticamente** a cada 30 segundos:

1. Adicionar JavaScript ao `dashboard.html` que:
   - Chama `/api/metricas` a cada 30s
   - Atualiza os cards com novos valores
   - Mostra "Conectado ✓" ou "Simulação ⚠️"

2. Adicionar charts.js que se atualizam em tempo real

---

## 🚀 Resumo

- ✅ **Flask API criada** com endpoints `/api/metricas` e `/api/status-banco`
- ✅ **Modo Simulação** ativo (dados fake quando sem banco)
- ✅ **Orquestrador** pronto para coletar dados (precisa banco conectado)
- ⚠️ **AWS RDS** não acessível (credenciais incorretas)
- ⏳ **Auto-refresh nos dashboards** ainda não implementado (próxima etapa)

**Próximo Passo**: Corrigir credenciais do banco e conectar!
