# 🚦 Tooltips Interativos dos Semáforos - Documentação

## ✨ Novas Funcionalidades Adicionadas

Agora quando você **passa o mouse sobre qualquer semáforo** no mapa, aparecem informações em tempo real sobre:

### 1. **Tooltip Hover (Tooltip ao passar mouse)**
   - Aparece automaticamente quando o mouse passa sobre o semáforo
   - Mostra em uma linha resumida:
     - **Estado da rota** (✅ No Horário, ⚠️ Atrasado, 🟢 Fluxo Livre, etc)
     - **Status de congestionamento** (Fluxo Livre, Congestionado, Muito Congestionado)
     - **Velocidade média em km/h**

### 2. **Popup Detalhado (Ao clicar no semáforo)**
   - Clique em qualquer semáforo para ver informações completas
   - Exibe:
     - 🚦 **Número do semáforo** na sequência da rota
     - 📍 **ID da rota e nome** da rota
     - 📊 **Posição:** percentual de onde está no percurso (0-100%)
     - 🚗 **Velocidade Média:** em km/h
     - 🚦 **Status de Fluxo:** Fluxo Livre, Moderado, Congestionado, Muito Congestionado
     - ⏱️ **Estado:** 
       - ✅ No Horário (atraso ≤ 0s)
       - 😐 Ligeiramente Atrasado (atraso 30-120s)
       - ⚠️ Atrasado (atraso 120-300s)
       - ⚠️ Muito Atrasado (atraso > 300s)
     - ⏳ **Atraso:** em minutos e segundos
     - 🛣️ **Tempo de Viagem:** tempo total estimado da rota
     - 🔄 **Ciclo de Atualização:** mostra quantas vezes foi atualizado

## 🎨 Indicadores Visuais

### Estados por Cor:
| Estado | Cor | Significado |
|--------|-----|------------|
| ✅ No Horário | Verde (#2ecc71) | Rota dentro do horário |
| 😐 Ligeiramente Atrasado | Amarelo (#f1c40f) | Pequeno atraso (30-120s) |
| ⚠️ Atrasado | Laranja (#f39c12) | Atraso considerável (120-300s) |
| ⚠️ Muito Atrasado | Vermelho (#e74c3c) | Atraso severo (> 300s) |

### Fluxo de Tráfego:
| Fluxo | Emoji | Velocidade |
|-------|-------|-----------|
| 🟢 Fluxo Livre | 🟢 | > 35 km/h |
| 🟡 Moderado | 🟡 | 25-35 km/h |
| 🟠 Congestionado | 🟠 | 15-25 km/h |
| 🔴 Muito Congestionado | 🔴 | < 15 km/h |

## 🖱️ Interações do Mouse

### Hover (Passar mouse)
1. **Tooltip aparece automaticamente** com resumo
2. O semáforo **aumenta de tamanho** (raio 8 → 10)
3. O círculo fica com **borda mais espessa**

### Click (Clicar)
1. **Popup detalhado** abre com todas as informações
2. Popup tem **barra colorida lateral** indicando o estado
3. Clique fora para fechar

## 📡 Dados em Tempo Real

Os tooltips e popups são **atualizados a cada 5 segundos** com:
- ✅ Velocidade média atual da rota
- ✅ Atraso atualizado (baseado em TomTom Traffic)
- ✅ Fluxo de tráfego recalculado
- ✅ Estado/status redesenhado

## 🔧 Implementação Técnica

### Arquivos Modificados:
- **mapa_6_rotas_reais.html**
  - Linhas 330-380: Criação de semáforos com tooltips/popups
  - Linhas 460-500: Eventos de mouse (hover effects)
  - Linhas 507-575: Atualização em tempo real de tooltips

### Métodos Leaflet Utilizados:
```javascript
marker.bindPopup(html)      // Associa popup ao marcador
marker.bindTooltip(text)    // Associa tooltip ao marcador
marker.setTooltipContent()  // Atualiza conteúdo do tooltip
marker.setPopupContent()    // Atualiza conteúdo do popup
marker.setRadius()          // Muda tamanho do círculo
marker.setStyle()           // Muda visual do marcador
```

## 📊 Exemplo de Dados Exibidos

```
🚦 Semáforo 2
Rota: 1 - Rota 1: Praça Liberdade → Funcionários
─────────────────────────────
Posição: 42% da rota
Velocidade Média: 28.5 km/h
Fluxo: 🟡 Moderado
─────────────────────────────
Estado: ⚠️ Atrasado
Atraso: 2min 45s
Tempo de Viagem: 8min
Atualizado há 12 ciclos
```

## 🎯 O Que Está Sendo Medido para Otimização

1. **Velocidade Média**: Quanto mais rápido, melhor o fluxo
2. **Atraso (delay)**: Comparação com tempo sem trânsito
3. **Fluxo de Tráfego**: Categorizado em 4 níveis
4. **Estado da Rota**: Atrasada vs No Horário
5. **Distribuição Espacial**: Semáforos cobrem 25%, 50%, 75% da rota

Esses dados serão usados para **otimizar a temporização dos semáforos** em tempo real!

## ✅ Próximas Features

- [ ] Histórico de atrasos (gráfico)
- [ ] Previsão de chegada
- [ ] Alertas automáticos
- [ ] Comparação entre rotas
- [ ] Exportação de relatórios
