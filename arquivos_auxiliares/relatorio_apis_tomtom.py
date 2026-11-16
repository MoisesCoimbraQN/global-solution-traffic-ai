# -*- coding: utf-8 -*-
"""
RESUMO DETALHADO - APIs TomTom em Uso
Global Solution (CitizenTech) - Passo 2
"""

import json
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()
TOMTOM_API_KEY = os.getenv('TOMTOM_API_KEY')

if not TOMTOM_API_KEY:
    raise ValueError("TOMTOM_API_KEY nao configurada no .env")

APIS_TOMTOM_EM_USO = {
    "1_Traffic_Flow_Tiles": {
        "tipo": "Visualizacao em Tempo Real",
        "url": f"https://api.tomtom.com/traffic/map/4/tile/Relative/{{z}}/{{x}}/{{y}}.png?key={TOMTOM_API_KEY}",
        "descricao": "Camada de trafego sobreposta no mapa - mostra congestoes com cores",
        "estilos": ["Relative", "Absolute"],
        "cores": {
            "verde": "Fluxo livre (velocidade normal)",
            "amarelo": "Lentidao moderada (60-80% velocidade normal)",
            "vermelho": "Congestionamento severe (< 60% velocidade normal)"
        },
        "atualizacao": "Em tempo real (a cada 2-5 minutos)",
        "uso_atual": "Mapa interativo do navegador",
        "arquivos": [
            "mapa_rota_real_manual.py",
            "mapa_rota_real_folium.py",
            "mapa_rota_real_osmnx.py",
            "mapa_trafego_folium.py",
            "mapa_trafego_tempo_real.html"
        ]
    },
    
    "2_Routing_API": {
        "tipo": "Calculo de Rota",
        "url": "https://api.tomtom.com/routing/1/calculateRoute/{lng},{lat}:{lng},{lat}/json",
        "descricao": "Calcula rota entre dois pontos (inicio e fim) seguindo as ruas",
        "parametros": {
            "routeType": ["fastest", "shortest"],
            "traffic": ["flow", "incident"],
            "language": "pt-BR"
        },
        "atualizacao": "Sob demanda (quando usuario solicita rota)",
        "uso_atual": "Calculo de rotas reais (Tentativa 1 - falhou por erro 400)",
        "arquivos": [
            "mapa_rota_real_folium.py",
            "coletor_transito_db.py",
            "coleta_transito.py"
        ],
        "status": "ERRO 400 - URL com parametros incorretos"
    },
    
    "3_Matrix_Route_API": {
        "tipo": "Matriz de Distancias",
        "url": "https://api.tomtom.com/routing/1/matrix",
        "descricao": "Calcula tempos de viagem entre multiplos pontos (matriz)",
        "uso_potencial": "Coordenacao entre semaforos proximos (Passo 3)",
        "arquivos": ["algoritmo_otimizacao.py"],
        "status": "Nao implementado ainda"
    },
    
    "4_Geocoding_API": {
        "tipo": "Geocodificacao",
        "url": "https://api.tomtom.com/search/2/geocode/{query}.json",
        "descricao": "Converte endereco em coordenadas (ou vice-versa)",
        "uso_potencial": "Buscar endereco de via e obter coordenadas",
        "status": "Nao implementado ainda"
    },
    
    "5_Traffic_Incidents_API": {
        "tipo": "Incidentes de Trafego",
        "url": "https://api.tomtom.com/traffic/services/4/incidentDetails",
        "descricao": "Retorna acidentes, engarrafamentos e eventos em tempo real",
        "uso_potencial": "Alertar sistema sobre problemas urgentes",
        "status": "Nao implementado ainda"
    }
}

ROTAS_SENDO_PUXADAS = {
    "rota_1": {
        "nome": "Centro (Praca Liberdade) -> Funcionarios",
        "inicio": [-19.9289, -43.9348],
        "fim": [-19.9020, -43.9100],
        "pontos_intermediarios": 7,
        "distancia_estimada": "~4.5 km",
        "tempo_livre": "~12 minutos",
        "tempo_com_trafego": "~18-25 minutos (varia com trafego)",
        "semaforos": 4,
        "avenidas": ["Afonso Pena", "Getulio Vargas", "Bahia", "Brasil", "Cristovao Colombo"],
        "tipo_via": "Urbana principal",
        "dados_coletados": ["velocidade_atual", "velocidade_livre", "tempo_percurso", "congestionamento"]
    }
}

ENDPOINTS_ATIVOS = [
    {
        "nome": "Traffic Flow Tiles - Relative",
        "url_padrao": "https://api.tomtom.com/traffic/map/4/tile/Relative/{z}/{x}/{y}.png",
        "exemplo": "https://api.tomtom.com/traffic/map/4/tile/Relative/13/4096/2731.png",
        "atualizado": "A cada zoom/panorama no mapa",
        "custos": "Contagem de requisicoes (tiles) por segundo"
    },
    {
        "nome": "Traffic Flow Tiles - Absolute",
        "url_padrao": "https://api.tomtom.com/traffic/map/4/tile/Absolute/{z}/{x}/{y}.png",
        "exemplo": "https://api.tomtom.com/traffic/map/4/tile/Absolute/13/4096/2731.png",
        "atualizado": "A cada zoom/panorama no mapa",
        "custos": "Contagem de requisicoes (tiles) por segundo"
    },
    {
        "nome": "Routing API (Fallback - Nao funciona)",
        "url_padrao": "https://api.tomtom.com/routing/1/calculateRoute/{lng},{lat}:{lng},{lat}/json",
        "exemplo": "https://api.tomtom.com/routing/1/calculateRoute/-43.9348,-19.9289:-43.91,-19.902/json",
        "status": "ERRO 400 - Parametros incorretos",
        "motivo": "API key pode estar com restricoes ou formato da URL estava errado"
    }
]

DADOS_EM_TEMPO_REAL = {
    "velocidade_atual": {
        "descricao": "Velocidade media no trecho (em km/h)",
        "valor_exemplo": "32 km/h (na Av. Afonso Pena)",
        "proveniente_de": "Traffic Flow Tiles"
    },
    "velocidade_livre": {
        "descricao": "Velocidade esperada sem trafego (em km/h)",
        "valor_exemplo": "60 km/h (limite maximo)",
        "proveniente_de": "Dados estatisticos do TomTom"
    },
    "tempo_atual": {
        "descricao": "Tempo de percurso atual (em segundos)",
        "valor_exemplo": "1800 segundos (30 minutos)",
        "proveniente_de": "Calculo: distancia / velocidade_atual"
    },
    "tempo_livre": {
        "descricao": "Tempo esperado sem trafego (em segundos)",
        "valor_exemplo": "720 segundos (12 minutos)",
        "proveniente_de": "Calculo: distancia / velocidade_livre"
    },
    "fator_atraso": {
        "descricao": "Indice de congestionamento (tempo_atual / tempo_livre)",
        "valor_exemplo": "2.5 (significa 150% mais lento que o normal)",
        "proveniente_de": "Calculo do algoritmo",
        "uso": "Decisao do algoritmo de otimizacao de semaforos"
    },
    "nivel_congestionamento": {
        "descricao": "Score de 0 a 100 indicando severidade",
        "valor_exemplo": "75 (congestionamento severe)",
        "proveniente_de": "Traffic Flow Tiles"
    }
}

CUSTOS_API = {
    "Traffic_Flow_Tiles": {
        "valor": "$0.00",
        "descricao": "GRATUITO - Includido no plano padrao"
    },
    "Routing_API": {
        "valor": "$0.50 por 1000 chamadas",
        "descricao": "Pago por rota calculada"
    },
    "Matrix_Route_API": {
        "valor": "$0.50 por 100 chamadas",
        "descricao": "Mais caro que Routing (ideal para lotes)"
    },
    "Traffic_Incidents_API": {
        "valor": "$0.00",
        "descricao": "GRATUITO"
    }
}


def gerar_relatorio():
    """Gera relatorio detalhado sobre APIs TomTom"""
    
    print("=" * 80)
    print(" " * 15 + "RELATORIO DETALHADO - APIs TomTom em Uso")
    print(" " * 20 + "Global Solution (CitizenTech)")
    print("=" * 80)
    
    print("\n" + "█" * 80)
    print("1. APIs TOMTOM DISPONIVEIS E SEUS USOS")
    print("█" * 80 + "\n")
    
    for chave, api in APIS_TOMTOM_EM_USO.items():
        print(f"\n{chave.upper().replace('_', ' ')}")
        print("-" * 80)
        print(f"  Tipo: {api['tipo']}")
        print(f"  Descricao: {api['descricao']}")
        print(f"  URL Base: {api['url']}")
        print(f"  Status: {api.get('status', 'ATIVO')}")
        if 'arquivos' in api:
            print(f"  Arquivos usando: {', '.join(api['arquivos'][:2])}{'...' if len(api['arquivos']) > 2 else ''}")
        
        if 'cores' in api:
            print(f"  Cores de Trafego:")
            for cor, desc in api['cores'].items():
                print(f"    - {cor.upper()}: {desc}")
    
    print("\n" + "█" * 80)
    print("2. ENDPOINTS ATIVOS AGORA")
    print("█" * 80 + "\n")
    
    for endpoint in ENDPOINTS_ATIVOS:
        print(f"\n📍 {endpoint['nome']}")
        print(f"   URL Padrao: {endpoint['url_padrao']}")
        if 'exemplo' in endpoint:
            print(f"   Exemplo: {endpoint['exemplo']}")
        if 'atualizado' in endpoint:
            print(f"   Atualizacao: {endpoint['atualizado']}")
        if 'status' in endpoint:
            print(f"   Status: {endpoint['status']}")
        if 'motivo' in endpoint:
            print(f"   Motivo: {endpoint['motivo']}")
    
    print("\n" + "█" * 80)
    print("3. ROTA PRINCIPAL SENDO MONITORADA")
    print("█" * 80 + "\n")
    
    for chave, rota in ROTAS_SENDO_PUXADAS.items():
        print(f"\nRota: {rota['nome']}")
        print(f"  Inicio: {rota['inicio']}")
        print(f"  Fim: {rota['fim']}")
        print(f"  Distancia: {rota['distancia_estimada']}")
        print(f"  Tempo livre: {rota['tempo_livre']}")
        print(f"  Tempo com trafego: {rota['tempo_com_trafego']}")
        print(f"  Semaforos otimizaveis: {rota['semaforos']}")
        print(f"  Avenidas: {', '.join(rota['avenidas'])}")
        print(f"  Dados coletados: {', '.join(rota['dados_coletados'])}")
    
    print("\n" + "█" * 80)
    print("4. DADOS COLETADOS EM TEMPO REAL")
    print("█" * 80 + "\n")
    
    for chave, dado in DADOS_EM_TEMPO_REAL.items():
        print(f"\n📊 {chave.upper().replace('_', ' ')}")
        print(f"   Descricao: {dado['descricao']}")
        print(f"   Valor Exemplo: {dado['valor_exemplo']}")
        print(f"   Proveniente de: {dado['proveniente_de']}")
        if 'uso' in dado:
            print(f"   Uso: {dado['uso']}")
    
    print("\n" + "█" * 80)
    print("5. CUSTOS DE API")
    print("█" * 80 + "\n")
    
    for api, custo in CUSTOS_API.items():
        print(f"\n💰 {api.replace('_', ' ')}")
        print(f"   Custo: {custo['valor']}")
        print(f"   Descricao: {custo['descricao']}")
    
    print("\n" + "█" * 80)
    print("6. RESUMO DE USO ATUAL")
    print("█" * 80 + "\n")
    
    resumo = f"""
    ✓ API de Trafego (Traffic Flow Tiles): ATIVA
      - Funcao: Exibir mapa com cores de congestionamento
      - Atualizacao: Em tempo real (2-5 minutos)
      - Custo: GRATUITO
      
    ✗ API de Roteamento (Routing): INATIVA (erro 400)
      - Funcao: Calcular rotas reais (estava tentando)
      - Motivo do erro: Parametros da URL incorretos
      - Alternativa: Rota manual com 33 pontos de coordenadas
      
    ⚙ Algoritmo de Otimizacao: ATIVO
      - Entrada: Fator de atraso (tempo_atual / tempo_livre)
      - Logica: Se fator > 1.3, aumenta tempo verde do semaforo
      - Saida: Novo tempo de semaforo para reduzir fila
      
    📊 Coleta de Dados: ATIVA (a cada 5 minutos na AWS EC2)
      - Ponto de coleta: Via Centro -> Funcionarios
      - Dados coletados: Velocidade, tempo, congestionamento
      - Armazenamento: Snowflake Data Warehouse
    """
    
    print(resumo)
    
    print("\n" + "█" * 80)
    print("7. PROXIMOS PASSOS (Passo 3 - Fase Futura)")
    print("█" * 80 + "\n")
    
    proximos = """
    1. CORRIGIR API de Roteamento
       - Validar chave da API
       - Testar com curl para diagnosticar erro 400
       - Implementar calculo de rotas reais dinamicas
    
    2. ADICIONAR Traffic Incidents API
       - Alertar sistema sobre acidentes
       - Desviar trafego automaticamente
    
    3. IMPLEMENTAR Matrix Route API
       - Coordenacao entre semaforos proximos
       - Sincronizacao de fases
    
    4. MACHINE LEARNING
       - Prever congestionamento futuro
       - Otimizar baseado em historico
    """
    
    print(proximos)
    
    print("\n" + "=" * 80)
    print(" " * 25 + f"Relatorio gerado em {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    gerar_relatorio()
