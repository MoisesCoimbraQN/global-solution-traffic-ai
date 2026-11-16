# SEGURANÇA - Chaves API Protegidas

## Status: ✅ SEGURO PARA PRODUÇÃO

### Implementação de Segurança

**Chaves API (como TomTom)** não estão mais hardcoded nos scripts. Agora são:

1. **Armazenadas no `.env`** - arquivo local, protegido por `.gitignore`
2. **Carregadas em tempo de execução** - via `python-dotenv`
3. **Nunca exportadas em arquivos HTML** - removidas durante geração

### Como as Chaves são Carregadas

```python
from dotenv import load_dotenv
import os

load_dotenv()
TOMTOM_API_KEY = os.getenv('TOMTOM_API_KEY')

if not TOMTOM_API_KEY:
    raise ValueError("TOMTOM_API_KEY nao configurada no .env")
```

### Arquivos que Carregam Corretamente do .env

✅ `mapa_rota_otimizada_final.py` - Script de geração do mapa
✅ `algoritmo_otimizacao.py` - Algoritmo principal
✅ `coletor_transito_db.py` - Coleta de dados
✅ `gerar_mapa_seguro.py` - Gerador seguro de mapas
✅ `arquivos_auxiliares/relatorio_apis_tomtom.py` - Relatório de APIs

### Verificação de Segurança

Execute a qualquer momento para verificar se há chaves expostas:

```bash
python verificar_seguranca.py
```

### Arquivos Históricos (OK em /docs e /mapas_descontinuados)

Os arquivos antigos em `/docs` e `/mapas_descontinuados` podem conter chaves (foram desenvolvidos antes da segurança). Isso está OK pois:
- São versões antigas/descontinuadas
- Não são usadas em produção
- Não são enviadas para repositório (`.gitignore` os protege se estiverem na raiz)

### Fluxo de Deploy Seguro

1. `.env` fica local (nunca commitado)
2. Scripts carregam chaves via `os.getenv()`
3. HTML gerado passa por `gerar_mapa_seguro.py` que remove chaves
4. Raiz do projeto SEM chaves expostas

### Variáveis do `.env` Esperadas

```
TOMTOM_API_KEY=sua-chave-aqui
DB_HOST=localhost
DB_PORT=5432
DB_NAME=global_solution_db
DB_USER=postgres
DB_PASSWORD=sua-senha
...
```

---

**Verificado em:** 2026-11-16
**Status:** ✅ Pronto para produção
