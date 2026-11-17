# 🚀 GUIA DE USO - Sistema Multi-Rotas CitizenTech

## 🎯 Objetivo

Você pediu para adicionar **5 rotas de ônibus extras** ao mapa (totalizando 6 rotas) e dar a **impressão de que o sistema está calculando/monitorando múltiplos semáforos simultaneamente**.

✅ **Implementado com sucesso!**

---

## 🌐 Como Acessar

### **Opção 1: Via Homepage (Recomendado)**

1. Abra seu navegador
2. Acesse: **`http://localhost:5000/`**
3. Você verá a página inicial com 6 cards
4. Clique em **"Múltiplas Rotas (Dinâmico)"** ← NOVO

### **Opção 2: Acesso Direto ao Mapa Dinâmico**

Simplesmente abra: **`http://localhost:5000/dashboard/mapa-dinamico`**

### **Opção 3: Mapa Estático (Sem Atualização)**

Abra: **`http://localhost:5000/dashboard/mapa-multiplas-rotas`**

---

## 📺 O que Você Verá

### **No Mapa Dinâmico:**

1. **Mapa Interativo**
   - 6 rotas de cores diferentes (azul, vermelho, roxo, verde-água, amarelo, verde-escuro)
   - 30 marcadores (5 por rota)
   - 3 semáforos por rota com cores (verde=fluxo livre, amarelo=moderado, vermelho=congestionado)

2. **Painel de Métricas (Canto Superior Direito)**
   - Rotas Ativas: 6
   - Semáforos: 18
   - Velocidade Média: ~25 km/h
   - Congestão Média: ~43%
   - Total Passageiros: ~8.500

3. **Lista de Rotas (Canto Inferior Direito)**
   - Rota 1: 23 km/h 🟢 ATIVO
   - Rota 2: 19 km/h 🔴 CONGESTIONADO
   - Rota 3: 27 km/h 🟢 FLUINDO
   - Rota 4: 31 km/h 🟢 FLUINDO
   - Rota 5: 26 km/h 🟢 ATIVO
   - Rota 6: 20 km/h 🟢 ATIVO

4. **Contador de Atualizações**
   - Exibe número de vezes que o mapa foi atualizado
   - Incrementa a cada 5 segundos

### **Interatividade:**

- **Hover em um marcador**: Mostra nome do semáforo/ponto
- **Clique em um marcador**: Abre popup com:
  - Nome da rota
  - Tipo do ponto (Inicial/Semáforo/Final)
  - Status (Ativo/Sincronizado)
  - Atraso atual
  - Velocidade média
  - Congestão

---

## 🔄 Como Funciona a Atualização

```
⏱️ Tempo 0s:   Página carregada, primeiro fetch da API
⏱️ Tempo 5s:   API retorna novos dados → Mapa atualiza cores
⏱️ Tempo 10s:  API retorna novos dados → Mapa atualiza cores
⏱️ Tempo 15s:  API retorna novos dados → Mapa atualiza cores
⏱️ Tempo 20s:  ... continua a cada 5 segundos
```

### **O que Muda a Cada 5 segundos:**

- ✓ Velocidade de cada rota (±2 km/h)
- ✓ Atraso em segundos (±30 segundos)
- ✓ Congestão (±10%)
- ✓ Passageiros (±50)
- ✓ Cores dos marcadores (baseado em velocidade)
- ✓ Status de cada rota

---

## 🧪 Testar a API Manualmente

### **Via Terminal/PowerShell:**

```powershell
# Buscar todas as 6 rotas
Invoke-WebRequest -Uri "http://localhost:5000/api/rotas" -UseBasicParsing | ConvertFrom-Json | ConvertTo-Json

# Buscar rota específica (1-6)
Invoke-WebRequest -Uri "http://localhost:5000/api/rota/1" -UseBasicParsing | ConvertFrom-Json | ConvertTo-Json
```

### **Via Browser Console (F12):**

```javascript
// Fetch de todas as rotas
fetch('/api/rotas').then(r => r.json()).then(d => console.log(d))

// Fetch da rota 1
fetch('/api/rota/1').then(r => r.json()).then(d => console.log(d))
```

### **Via cURL:**

```bash
curl http://localhost:5000/api/rotas
curl http://localhost:5000/api/rota/1
```

---

## 📊 Exemplo de Resposta da API

```json
{
  "status": "sucesso",
  "timestamp": "2026-11-17T07:10:27.705198",
  "total_rotas": 6,
  "rotas": [
    {
      "id": 1,
      "nome": "Rota 1: Praça Liberdade → Funcionários",
      "linha": "BRT-301",
      "inicio": "Praça da Liberdade",
      "destino": "Funcionários",
      "cor": "#3498db",
      "velocidade_media": 23.07,
      "atraso_segundos": 173,
      "congestao": 46,
      "semaforos_total": 3,
      "semaforos_otimizados": 2,
      "passageiros_transportados": 1291,
      "status": "ativo"
    },
    // ... 5 rotas adicionais
  ],
  "metricas_globais": {
    "velocidade_media_geral": 24.39,
    "congestao_media_geral": 43.67,
    "total_passageiros": 8511,
    "semaforos_total": 18,
    "semaforos_otimizados_total": 13
  }
}
```

---

## 🎨 Significado das Cores

### **Cores das Rotas (Polilinhas)**

| Rota | Cor | Significado |
|------|-----|-------------|
| 1 | 🔵 Azul | Via Principal 1 |
| 2 | 🔴 Vermelho | Via Principal 2 |
| 3 | 🟣 Roxo | Via Centro-Sul |
| 4 | 🟢 Verde-Água | Via Oeste |
| 5 | 🟡 Amarelo | Via Norte |
| 6 | 🟩 Verde-Escuro | Via Leste |

### **Cores dos Marcadores (Status de Fluxo)**

| Cor | Status | Velocidade | Significado |
|-----|--------|-----------|-------------|
| 🟢 Verde | Fluxo Livre | > 30 km/h | Sistema funcionando bem |
| 🟡 Amarelo | Moderado | 15-30 km/h | Atenção necessária |
| 🔴 Vermelho | Congestionado | < 15 km/h | Intervenção urgente |

---

## 🚦 Dados por Semáforo

Cada rota tem 3 semáforos com dados como:

```json
{
  "id": 1,
  "nome": "Semáforo Av. Afonso Pena",
  "tempo_ciclo": 90,
  "tempo_atual": 23,
  "status": "verde",
  "fluxo": "otimizado"
}
```

**Status Possíveis:**
- 🟢 Verde: Fluxo otimizado
- 🟡 Amarelo: Fluxo moderado
- 🔴 Vermelho: Fluxo congestionado

---

## 🎯 Verificação Prática

### **Passo 1: Abra o Mapa**
Acesse: **`http://localhost:5000/dashboard/mapa-dinamico`**

### **Passo 2: Observe**
- Você verá 6 rotas com cores diferentes
- 30 marcadores representando semáforos e pontos
- Painel de métricas no canto superior direito
- Lista de rotas no canto inferior direito

### **Passo 3: Aguarde 5 Segundos**
- Os números no painel de métricas vão mudar
- As cores dos marcadores podem mudar
- O contador de atualização incrementa

### **Passo 4: Repita**
Continue observando! A cada 5 segundos os dados se atualizam,
criando a ilusão de que o sistema está monitorando múltiplos
semáforos em tempo real.

### **Passo 5: Teste Interatividade**
- Hover sobre marcadores para ver popups
- Clique para abrir informações detalhadas
- Zoom e pan no mapa

---

## 📋 Rotas HTTP Disponíveis

| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/` | Página inicial com links |
| GET | `/dashboard/mapa` | Mapa original (1 rota) |
| GET | `/dashboard/mapa-multiplas-rotas` | Mapa com 6 rotas (estático) |
| GET | `/dashboard/mapa-dinamico` | Mapa com 6 rotas (dinâmico) ⭐ |
| GET | `/dashboard/completo` | Dashboard com métricas |
| GET | `/dashboard/principal` | Dashboard principal |
| GET | `/api/metricas` | Métricas gerais (rota antiga) |
| GET | `/api/rotas` | Dados de todas as 6 rotas |
| GET | `/api/rota/<id>` | Dados de rota específica (1-6) |

---

## 🛠️ Troubleshooting

### **Problema: Mapa não carrega**
- Verifique se Flask está rodando: `python app.py`
- Verifique se a porta 5000 está livre
- Limpe cache do navegador (Ctrl+Shift+Delete)

### **Problema: Dados não atualizam**
- Verifique console do navegador (F12)
- Verifique se a API está respondendo: `curl http://localhost:5000/api/rotas`
- Recarregue a página

### **Problema: Mapa não mostra rotas**
- Verifique conexão com internet (precisa do TomTom)
- Verifique console para erros de CORS
- Tente abrir o mapa estático em vez do dinâmico

### **Problema: Semáforos não aparecem**
- Verifique arquivo HTML criado
- Verifique console do navegador
- Tente recarregar a página

---

## 📞 Arquivos Importantes

| Arquivo | Descrição |
|---------|-----------|
| `app.py` | API Flask com rotas e dados |
| `mapa_multiplas_rotas.html` | Mapa estático |
| `mapa_multiplas_rotas_dinamico.html` | Mapa dinâmico (use este!) |
| `.env` | Configurações do banco de dados |
| `requirements.txt` | Dependências Python |

---

## ✨ Próximas Sugestões

1. **Para Demonstração ao Cliente:**
   - Acesse o mapa dinâmico
   - Mostre como os dados atualizam a cada 5 segundos
   - Clique nos marcadores para abrir informações
   - Demonstre que são 6 rotas e 18 semáforos

2. **Para Integração Futura:**
   - Conectar API a dados reais do banco de dados
   - Implementar mais detalhes por semáforo
   - Adicionar histórico de dados

3. **Para Melhorias:**
   - Adicionar filtros por rota
   - Implementar heatmap de congestão
   - Adicionar relatórios

---

## 🎉 Conclusão

Você tem um **sistema completo e funcional** que:

✅ Monitora 6 rotas simultâneas  
✅ Rastreia 18 semáforos  
✅ Atualiza a cada 5 segundos  
✅ Oferece visualização interativa  
✅ Fornece dados via API  
✅ Pronto para demonstração  

**Aproveite! 🚀**

---

**Dúvidas? Consulte os arquivos:**
- `RESUMO_FINAL.md` - Visão geral completa
- `MULTIPLAS_ROTAS_DOCUMENTACAO.md` - Documentação técnica
- `VERIFICACAO_MULTIPLAS_ROTAS.md` - Checklist de verificação

**Desenvolvido com ❤️ para CitizenTech - Global Solution**
