# 🚦 Guia Rápido - Tooltips nos Semáforos

## 📍 Onde Estão os Semáforos?

Os semáforos são os **pequenos círculos na cor amarela** distribuídos ao longo de cada rota no mapa.

```
INÍCIO (🟢 Verde)
    ↓
🚦 Semáforo 1
    ↓  
🚦 Semáforo 2
    ↓
🚦 Semáforo 3
    ↓
FIM (🔴 Vermelho)
```

---

## 🖱️ Interações

### 1️⃣ **Passe o Mouse** sobre qualquer semáforo

```
┌─────────────────────────────────────────┐
│ ⚠️ Atrasado | 🟠 Congestionado | 28.9 km/h│
└─────────────────────────────────────────┘
     (Aparece automaticamente)
```

**Mostra em 1 linha:**
- 🟢 ✅ No Horário
- 🟡 😐 Ligeiramente Atrasado
- 🟠 ⚠️ Atrasado
- 🔴 ⚠️ Muito Atrasado

---

### 2️⃣ **Clique** em um semáforo

```
┌─────────────────────────────────────────┐
│ 🚦 Semáforo 2                           │
│ Rota: 1 - Praça Liberdade → Funcionários│
│ ─────────────────────────────────────── │
│ Posição: 42% da rota                    │
│ Velocidade Média: 28.5 km/h             │
│ Fluxo: 🟡 Moderado                      │
│ ─────────────────────────────────────── │
│ Estado: ⚠️ Atrasado                     │
│ Atraso: 2min 45s                        │
│ Tempo de Viagem: 8min                   │
│ Atualizado há 12 ciclos                 │
└─────────────────────────────────────────┘
```

**Exibe:**
- Número e localização do semáforo
- ID e nome da rota
- Posição percentual no trajeto
- Velocidade em tempo real
- Status de congestionamento
- Estado (atrasado/no horário)
- Tempo de atraso em minutos e segundos
- Tempo total estimado

---

## 📊 Legenda de Estados

| Emoji | Estado | Atraso |
|-------|--------|--------|
| ✅ | No Horário | 0-30 segundos |
| 😐 | Ligeiramente Atrasado | 30-120 segundos |
| ⚠️ | Atrasado | 120-300 segundos |
| ⚠️ | Muito Atrasado | > 300 segundos |

---

## 🚗 Legenda de Fluxo

| Emoji | Fluxo | Velocidade |
|-------|-------|-----------|
| 🟢 | Fluxo Livre | > 35 km/h |
| 🟡 | Moderado | 25-35 km/h |
| 🟠 | Congestionado | 15-25 km/h |
| 🔴 | Muito Congestionado | < 15 km/h |

---

## ⚙️ Animações

### Hover (Mouse Over)
- Semáforo **aumenta de tamanho** (fica maior)
- Borda fica **mais grossa**
- Tooltip aparece **automaticamente**

### Normal
- Volta ao tamanho original

---

## 🔄 Atualização em Tempo Real

Os dados são atualizados a cada **5 segundos**:
- ✅ Velocidade recalculada
- ✅ Atraso atualizado
- ✅ Fluxo reanalisado
- ✅ Estado revisado

Se você deixar o popup aberto, ele atualiza automaticamente!

---

## 🎯 Dados Monitorados

Usamos esses dados para **otimizar os semáforos em tempo real**:

1. **Velocidade Média** → Detecta congestionamento
2. **Atraso (delay)** → Compara com tempo normal
3. **Fluxo de Tráfego** → 4 categorias (livre/moderado/congestionado/crítico)
4. **Posição na Rota** → Semáforos distribuídos em 25%, 50%, 75%
5. **Tempo de Viagem** → Monitora pontuação total

---

## 💡 Dicas

✨ **Clique e deixe aberto** - O popup se atualiza sozinho!

✨ **Passe o mouse e espere** - Tooltip aparece em 1 segundo

✨ **Compare rotas** - Veja qual rota está mais congestionada passando o mouse sobre vários semáforos

✨ **Monitore em tempo real** - Observe como os dados mudam a cada atualização

---

## 🚀 Próximas Features

- 📈 Gráfico histórico de velocidade
- 🔔 Alertas de congestionamento crítico
- 📊 Comparação entre rotas
- 🎥 Animação de movimento das rotas
- 📄 Exportação de relatórios

---

## ❓ Dúvidas?

Ver arquivo: `TOOLTIPS_SEMAFOROS.md` para documentação completa!
