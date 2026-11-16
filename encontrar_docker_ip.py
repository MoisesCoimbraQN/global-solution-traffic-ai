"""
Script para encontrar o IP do Docker PostgreSQL
"""

import socket
import subprocess
import os

print("="*70)
print("ENCONTRAR IP DO DOCKER")
print("="*70)

# 1. Se Docker estiver LOCAL
print("\n[1] Testando Docker Local:")
try:
    result = subprocess.run(['docker', 'ps'], capture_output=True, text=True)
    if 'postgresql' in result.stdout or 'postgres' in result.stdout:
        print("[OK] Docker PostgreSQL rodando localmente")
        print("\nContainers:")
        print(result.stdout)
        
        # Pegar IP do container
        result = subprocess.run(['docker', 'inspect', '-f', '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}', 'postgres'], 
                              capture_output=True, text=True)
        if result.stdout.strip():
            print(f"\nIP do Container: {result.stdout.strip()}")
    else:
        print("[!] PostgreSQL não encontrado nos containers locais")
except Exception as e:
    print(f"[!] Docker não está disponível: {e}")

# 2. Se estiver em servidor remoto
print("\n[2] Se PostgreSQL está em servidor remoto:")
print("   Pergunte ao administrador ou verifique em:")
print("   - Dashboard da nuvem (AWS, Azure, DigitalOcean, etc)")
print("   - Console do servidor")
print("   - Documentação da implantação Docker")

# 3. Testar conexão
print("\n[3] Testar Conexão:")
print("   Depois de encontrar o IP, use:")
print("   psql -h <IP_DO_DOCKER> -p 5432 -U admin_global -d global_solution_db")
print("   Senha: moises")

# 4. Descobrir nome do servidor
print("\n[4] Ou se usar docker-compose:")
print("   O host pode ser o nome do serviço em docker-compose.yml")
print("   Exemplo: postgres, db, postgresql-db, etc")

print("\n" + "="*70)
print("Dica: Verifique o arquivo docker-compose.yml ou docker run command")
print("="*70)
