# 🚀 GUIA COMPLETO - DEPLOY NA RENDER

## ✅ Arquivos Preparados

Criei os seguintes arquivos na raiz do projeto:
- **`app.py`** - Servidor Flask que serve os 3 dashboards
- **`Procfile`** - Configuração do Render para rodar o servidor
- **`requirements.txt`** - Atualizado com Flask e Werkzeug
- **`DEPLOY_RENDER.md`** - Instruções passo a passo

## 📋 Pré-requisitos

1. **Conta GitHub** (se ainda não tiver)
   - Crie em https://github.com/signup

2. **Conta Render** (gratuita)
   - Crie em https://dashboard.render.com
   - Faça login com GitHub

## 🔧 Passo 1: Preparar Repositório Git

```powershell
cd "c:\Users\mcmoi\OneDrive\Área de Trabalho\GlobalSolution"

# Verificar se git já está inicializado
git status

# Se não estiver, inicializar:
git init
git add .
git commit -m "Setup deploy Render - Flask + Dashboards + Mapa Interativo"
git branch -M main
```

## 🌐 Passo 2: Criar Repositório no GitHub

1. Acesse https://github.com/new
2. Preencha:
   - **Repository name**: `global-solution` (ou outro nome)
   - **Description**: `CitizenTech - Sistema de Otimização de Tráfego`
   - **Public** (para Render acessar)
3. Clique em **"Create repository"**
4. Copie o comando de push (algo como):

```powershell
git remote add origin https://github.com/SEU_USER/global-solution.git
git push -u origin main
```

## 🚀 Passo 3: Deploy no Render

### 3.1 Conectar GitHub com Render

1. Acesse https://dashboard.render.com
2. Clique em **"+ New"** → **"Web Service"**
3. Clique em **"Connect a repository"**
4. Selecione seu repositório `global-solution`
5. Authorize Render acessar GitHub

### 3.2 Configurar Web Service

Preencha com esses valores:

| Campo | Valor |
|-------|-------|
| **Name** | `citizen-tech-dashboard` |
| **Environment** | `Python 3` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `python app.py` |
| **Instance Type** | `Free` |

### 3.3 Adicionar Variáveis de Ambiente

Na aba **"Environment"**, adicione:

```
TOMTOM_API_KEY=sua_chave_aqui
PORT=5000
```

(Deixe em branco se não tiver ainda - pode adicionar depois)

### 3.4 Clique em "Create Web Service"

O Render iniciará o deploy automaticamente. Pode levar 2-5 minutos.

## ✅ Verificar Deploy

Após concluir, você verá uma URL como:
```
https://citizen-tech-dashboard.onrender.com
```

Teste os endpoints:
- Home: https://citizen-tech-dashboard.onrender.com/
- Dashboard Completo: https://citizen-tech-dashboard.onrender.com/dashboard/completo
- Dashboard Principal: https://citizen-tech-dashboard.onrender.com/dashboard/principal
- Mapa: https://citizen-tech-dashboard.onrender.com/dashboard/mapa

## 🔄 Atualizar o Deploy

Sempre que fizer mudanças:

```powershell
git add .
git commit -m "Descrição da mudança"
git push origin main
```

Render detecta automaticamente e faz novo deploy.

## ⚠️ IMPORTANTE

### Proteger Chave de API
1. Certifique-se de que `.env` está em `.gitignore`
2. **NUNCA** commit da chave de API
3. Configure `TOMTOM_API_KEY` nas variáveis do Render, não no código

### Tier Gratuito do Render
- **Vantagens**: Sem custo, fácil setup
- **Limitações**: 
  - Hiberna se inativo por 15 minutos
  - Primeira inicialização é lenta
  - 0.5 GB RAM
- **Para Produção**: Upgrade para plano pago (~$7/mês)

## 🧪 Testar Localmente Antes de Fazer Deploy

```powershell
cd "c:\Users\mcmoi\OneDrive\Área de Trabalho\GlobalSolution"
python app.py
```

Depois abra: http://localhost:5000

## 📞 Suporte

Se tiver problemas:
1. Verifique logs no Render (dashboard da aplicação)
2. Teste localmente antes de fazer push
3. Certifique-se que `requirements.txt` está atualizado
4. Verifique se todos os arquivos HTML estão na raiz

---

## 🎯 Resumo das URLs Finais

Após deploy em `citizen-tech-dashboard.onrender.com`:

| O quê | URL |
|-------|-----|
| **Home** | https://citizen-tech-dashboard.onrender.com/ |
| **Dashboard Completo** | https://citizen-tech-dashboard.onrender.com/dashboard/completo |
| **Dashboard Principal** | https://citizen-tech-dashboard.onrender.com/dashboard/principal |
| **Mapa Interativo** | https://citizen-tech-dashboard.onrender.com/dashboard/mapa |

Compartilhe essas URLs com a banca para apresentação! 🎉
