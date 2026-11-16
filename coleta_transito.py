import requests
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()
API_KEY = os.getenv("TOMTOM_API_KEY")

if not API_KEY:
    raise ValueError("TOMTOM_API_KEY nao encontrada no arquivo .env")

# Exemplo de rota em Belo Horizonte (Origem: Praça da Liberdade -> Destino: Savassi)
# Formato: lat_origem,lon_origem:lat_destino,lon_destino
coordenadas = "-19.9322,-43.9386:-19.9331,-43.9378"

url = f"https://api.tomtom.com/routing/1/calculateRoute/{coordenadas}/json"

params = {
    "key": API_KEY,
    "sectionType": "traffic",
    "travelMode": "car"
}

print("Consultando a Routing API da TomTom com transito em tempo real...")
print(f"URL: {url}")
print(f"Parametros: {params}\n")

try:
    response = requests.get(url, params=params, timeout=10)
    
    print(f"Status Code retornado: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print("\nResposta completa da API:")
        print(data)
        
        if "routes" in data and len(data["routes"]) > 0:
            summary = data["routes"][0].get("summary", {})
            
            print("\nSUCESSO! Rota e Transito obtidos:")
            print(f"  - Distancia do trecho: {summary.get('lengthInMeters', 'N/A')} metros")
            
            if "travelTimeInSeconds" in summary:
                print(f"  - Tempo estimado COM transito: {summary['travelTimeInSeconds'] / 60:.1f} minutos")
            
            if "noTrafficTravelTimeInSeconds" in summary:
                print(f"  - Tempo estimado SEM transito: {summary['noTrafficTravelTimeInSeconds'] / 60:.1f} minutos")
                atraso = summary.get("travelTimeInSeconds", 0) - summary.get("noTrafficTravelTimeInSeconds", 0)
                if atraso > 0:
                    print(f"  - Atraso por congestionamento: {atraso:.0f} segundos")
        else:
            print("AVISO: Nenhuma rota encontrada na resposta")
    else:
        print("\nERRO NA RESPOSTA:")
        print(f"Status: {response.status_code}")
        print(f"Mensagem: {response.text}")
        
except requests.exceptions.Timeout:
    print("ERRO: Tempo limite de conexao excedido (timeout)")
except requests.exceptions.ConnectionError:
    print("ERRO: Nao foi possivel conectar a API do TomTom")
except Exception as e:
    print(f"ERRO inesperado: {str(e)}")
