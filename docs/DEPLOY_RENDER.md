# 🚀 Deploy na Render

## Passo 1: Criar repositório Git (se ainda não tiver)
```bash
git init
git add .
git commit -m "Setup deploy Render - Flask + Dashboards"
git branch -M main
```

## Passo 2: Push para GitHub
```bash
git remote add origin https://github.com/SEU_USER/global-solution.git
git push -u origin main
```

## Passo 3: Conectar com Render

1. Acesse https://dashboard.render.com
2. Clique em **"New +"** → **"Web Service"**
3. Selecione seu repositório GitHub
4. Configure:
   - **Name**: `citizen-tech-dashboard`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python app.py`
   - **Instance Type**: `Free` (ou pago se preferir)

5. Clique em **"Create Web Service"**

## Passo 4: Variáveis de Ambiente
Na aba **"Environment"** no Render, adicione:
```
TOMTOM_API_KEY=sua_chave_aqui
DATABASE_URL=sua_url_postgresql
```

## Passo 5: Acessar
Após deploy, acesse:
```
https://seu-servico.onrender.com
```

---

## 📌 URLs dos Dashboards (após deploy)
- **Home**: `https://seu-servico.onrender.com/`
- **Dashboard Completo**: `https://seu-servico.onrender.com/dashboard/completo`
- **Dashboard Principal**: `https://seu-servico.onrender.com/dashboard/principal`
- **Mapa Interativo**: `https://seu-servico.onrender.com/dashboard/mapa`

---

## ⚠️ Importante
- O Render oferece tier gratuito, mas pode hibernar se inativo
- Para produção, use tier pago
- Certifique-se de que `.env` está em `.gitignore`
- As chaves de API devem estar nas variáveis de ambiente do Render, não no código
