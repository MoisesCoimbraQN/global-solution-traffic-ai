# 🔓 PASSO A PASSO: Liberar Porta 5432 no Security Group da EC2

## Opção 1: Via AWS Console (Mais Fácil)

### Passo 1: Abrir AWS Console
1. Acesse: https://console.aws.amazon.com
2. Faça login com suas credenciais
3. Clique em "EC2" no menu à esquerda

### Passo 2: Encontrar sua Instância
1. No menu esquerdo, procure por **"Instances"**
2. Você verá uma lista de instâncias EC2
3. Procure pela instância com IP **3.16.37.215**
4. **Clique nela** para selecioná-la

### Passo 3: Encontrar o Security Group
1. Na aba inferior (Details), procure por **"Security"**
2. Você verá algo como:
   ```
   Security groups: sg-xxxxxxxx | sg-name
   ```
3. **Clique no nome do Security Group** (ex: sg-12345678)

### Passo 4: Editar Inbound Rules
1. Você entrará na página do Security Group
2. Procure pela aba **"Inbound rules"**
3. Clique no botão **"Edit inbound rules"** (lado direito)

### Passo 5: Adicionar Nova Regra
1. Clique em **"Add rule"** (botão azul)
2. Configure assim:

   | Campo | Valor |
   |-------|-------|
   | Type | **PostgreSQL** |
   | Protocol | TCP (preenchido automaticamente) |
   | Port Range | **5432** (preenchido automaticamente) |
   | Source | **0.0.0.0/0** (ou seu IP se quiser mais seguro) |
   | Description (opcional) | PostgreSQL Database |

3. Clique em **"Save rules"** (botão laranja)

### Passo 6: Pronto! ✅
Aguarde alguns segundos e a porta estará liberada.

---

## Opção 2: Via AWS CLI (Mais Rápido se já tem instalado)

```bash
# Substituir sg-xxxxxxxx pelo seu Security Group ID
aws ec2 authorize-security-group-ingress \
  --group-id sg-xxxxxxxx \
  --protocol tcp \
  --port 5432 \
  --cidr 0.0.0.0/0 \
  --region us-east-2
```

---

## Opção 3: Via SSH na EC2 (Mais Rápido se já está lá)

```bash
# 1. Conectar via SSH
ssh -i seu-pem.pem ubuntu@3.16.37.215

# 2. Abrir firewall (se usando UFW)
sudo ufw allow 5432/tcp

# 3. Ou se usando iptables
sudo iptables -A INPUT -p tcp --dport 5432 -j ACCEPT

# 4. Testar conexão local
docker exec global-solution-db psql -U admin_global -d global_solution_db -c "SELECT 1;"
```

---

## Passo Final: Testar Conexão

Após liberar a porta, teste no seu computador local:

### Windows/PowerShell:
```powershell
Test-NetConnection -ComputerName 3.16.37.215 -Port 5432 -InformationLevel Detailed
```

**Resultado esperado:**
```
TcpTestSucceeded : True
```

### Linux/Mac:
```bash
nc -zv 3.16.37.215 5432
```

**Resultado esperado:**
```
Connection to 3.16.37.215 5432 port [tcp/postgresql] succeeded!
```

---

## Se Ainda Não Conectar

### 1. Verificar se Docker está rodando
```bash
# Na EC2 via SSH
sudo docker ps | grep global-solution-db
```

Deve mostrar: `global-solution-db` com status "Up"

### 2. Verificar logs do Docker
```bash
sudo docker logs global-solution-db
```

### 3. Testar PostgreSQL dentro do container
```bash
docker exec global-solution-db psql -U admin_global -d global_solution_db -c "SELECT version();"
```

### 4. Verificar se PostgreSQL está escutando
```bash
docker exec global-solution-db netstat -tlnp | grep 5432
```

---

## ✅ Checklist Rápido

- [ ] AWS Console aberto (console.aws.amazon.com)
- [ ] Instância EC2 encontrada (3.16.37.215)
- [ ] Security Group localizado
- [ ] "Inbound rules" aberto
- [ ] Nova regra adicionada (PostgreSQL, 5432, 0.0.0.0/0)
- [ ] "Save rules" clicado
- [ ] Aguardado ~30 segundos
- [ ] Teste de conexão bem-sucedido

---

**Depois de liberar a porta, volte no PowerShell e reinicie o Flask:**

```powershell
# 1. Parar servidor
Get-Process python | ForEach-Object { Stop-Process -Id $_.Id -Force }

# 2. Reiniciar
cd "c:\Users\mcmoi\OneDrive\Área de Trabalho\GlobalSolution"
python app.py
```

Testando:
```powershell
Invoke-WebRequest -Uri "http://localhost:5000/api/metricas" -UseBasicParsing
```

Deve mostrar dados **reais** do banco! 🎉
