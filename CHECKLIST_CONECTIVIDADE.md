# CHECKLIST: Por que não consegue conectar ao PostgreSQL na EC2

## Problema: timeout na conexão 3.16.37.215:5432

### Causas Possíveis (em ordem de probabilidade):

1. **[MAIS PROVÁVEL] Security Group da EC2 não permite porta 5432**
   - Verifique em AWS Console → EC2 → Security Groups
   - Procure por regra de inbound com porta 5432
   - Se não existir, crie:
     - Type: PostgreSQL
     - Protocol: TCP
     - Port: 5432
     - Source: 0.0.0.0/0 (ou seu IP)

2. **Firewall da EC2 (iptables)**
   ```bash
   # Na EC2, rodar como root:
   sudo ufw allow 5432/tcp
   # ou
   sudo iptables -A INPUT -p tcp --dport 5432 -j ACCEPT
   ```

3. **PostgreSQL não está escutando em 0.0.0.0**
   - Na EC2, verifique postgresql.conf:
   ```bash
   sudo cat /var/lib/docker/volumes/*/docker-entrypoint.sh
   ```
   - Ou dentro do container:
   ```bash
   docker exec global-solution-db psql -U admin_global -d global_solution_db -c "SHOW listen_addresses;"
   ```

4. **Firewall do seu computador/ISP bloqueia conexão externa**
   - Teste em: http://www.yougetsignal.com/tools/open-ports/
   - Porta: 5432
   - IP: 3.16.37.215

### Solução Rápida:

**Na EC2 (via SSH):**
```bash
# 1. Verificar se container está rodando
sudo docker ps | grep global-solution-db

# 2. Testar conexão local
docker exec global-solution-db psql -U admin_global -d global_solution_db -c "SELECT 1"

# 3. Liberar porta no firewall
sudo ufw allow 5432/tcp

# 4. Verificar Security Group (AWS Console)
# - Vá em EC2 → Instances → Selecione sua instância
# - Aba "Security" → Clique no Security Group
# - Verifique Inbound Rules (deve ter 5432 TCP liberado)
```

### Teste Depois de Corrigir:

```powershell
# Windows/PowerShell
Test-NetConnection -ComputerName 3.16.37.215 -Port 5432 -InformationLevel Detailed
```

Deve mostrar: `TcpTestSucceeded : True`

---

**Resumo:** Muito provavelmente é o Security Group ou firewall da EC2 bloqueando a porta 5432.
