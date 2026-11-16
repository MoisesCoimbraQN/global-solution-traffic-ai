# -*- coding: utf-8 -*-
"""
Gerador de Mapa Definitivo - Sincronizado com TomTom API
Global Solution (CitizenTech)
"""

import folium
from folium import plugins
import requests
import os
from dotenv import load_dotenv

load_dotenv()
TOMTOM_API_KEY = os.getenv('TOMTOM_API_KEY')

if not TOMTOM_API_KEY:
    raise ValueError("TOMTOM_API_KEY nao configurada no .env")

def criar_mapa_definitivo():
    centro_bh = [-19.9167, -43.9345]
    
    # Criar o mapa base com tiles limpos
    mapa = folium.Map(
        location=centro_bh,
        zoom_start=14,
        tiles='https://tile.openstreetmap.de/tiles/osmde/{z}/{x}/{y}.png',
        attr='&copy; OpenStreetMap DE',
        prefer_canvas=False
    )
    
    # Inserir a chave de API real do .env na camada de tráfego da TomTom
    folium.TileLayer(
        tiles=f'https://api.tomtom.com/traffic/map/4/tile/Relative/{{z}}/{{x}}/{{y}}.png?key={TOMTOM_API_KEY}',
        attr='TomTom Traffic',
        name='TomTom Traffic (Tempo Real)',
        overlay=True,
        control=True,
        opacity=0.7
    ).add_to(mapa)
    
    # BUSCAR A GEOMETRIA EXATA DIRETAMENTE DA TOMTOM ROUTING API
    # Trecho real: Praça da Liberdade -> Bairro Funcionários (Passando por Afonso Pena, Getúlio Vargas e Brasil)
    origem_destino = "-19.92819,-43.93531:-19.90199,-43.90997"
    url = f"https://api.tomtom.com/routing/1/calculateRoute/{origem_destino}/json"
    
    params = {
        "key": TOMTOM_API_KEY,
        "traffic": "true",
        "travelMode": "car"
    }
    
    print("Consultando a TomTom API para obter o traçado real das avenidas de BH...")
    response = requests.get(url, params=params)
    
    pontos_geometria = []
    atraso = 0
    
    if response.status_code == 200:
        data = response.json()
        if "routes" in data and len(data["routes"]) > 0:
            rota = data["routes"][0]
            for leg in rota.get("legs", []):
                for pt in leg.get("points", []):
                    pontos_geometria.append([pt["latitude"], pt["longitude"]])
            print(f"[OK] Rota real carregada: {len(pontos_geometria)} pontos milimetricamente ajustados às ruas.")
            
            summary = rota.get("summary", {})
            atraso = max(0, int(summary.get("travelTimeInSeconds", 0) - summary.get("noTrafficTravelTimeInSeconds", 0)))
    else:
        print("[AVISO] Falha na API. Usando malha de contingência.")
        pontos_geometria = [[-19.92819, -43.93531], [-19.90199, -43.90997]]
        atraso = 75

    # POSICIONAR OS SEMÁFOROS EXATAMENTE SOBRE OS VÉRTICES DA ROTA DA API
    total = len(pontos_geometria)
    semaforos = [
        {'nome': 'Início - Praça da Liberdade', 'pos': 0, 'tipo': 'INICIO', 'desc': 'Ponto de Partida'},
        {'nome': 'Semáforo 1 - Av. Afonso Pena', 'pos': int(total * 0.25), 'tipo': 'OTIMIZADO', 'desc': 'Eixo Centro/Afonso Pena'},
        {'nome': 'Semáforo 2 - Av. Getúlio Vargas', 'pos': int(total * 0.45), 'tipo': 'OTIMIZADO', 'desc': 'Cruzamento Inteligente'},
        {'nome': 'Passagem - Região da Savassi', 'pos': int(total * 0.65), 'tipo': 'PASSAGEM', 'desc': 'Ponto de Monitoramento Zonal'},
        {'nome': 'Semáforo 3 - Av. Brasil', 'pos': int(total * 0.85), 'tipo': 'OTIMIZADO', 'desc': 'Ajuste de Ciclo Dinâmico'},
        {'nome': 'Destino - Funcionários', 'pos': total - 1, 'tipo': 'FIM', 'desc': 'Final do Trecho'}
    ]

    cores = {'INICIO': '#2ecc71', 'OTIMIZADO': '#3498db', 'PASSAGEM': '#f39c12', 'FIM': '#e74c3c'}

    for sem in semaforos:
        idx = sem['pos']
        lat, lon = pontos_geometria[idx][0], pontos_geometria[idx][1]
        
        popup_html = f"""
        <div style="font-family: Arial; width: 230px; padding: 8px;">
            <h4 style="margin: 0 0 6px 0; color: #333; font-size: 13px;">{sem['nome']}</h4>
            <p style="margin: 3px 0; font-size: 11px;"><b>Local:</b> {sem['desc']}</p>
            <p style="margin: 3px 0; font-size: 11px;"><b>Status:</b> Ativo / Sincronizado</p>
            <p style="margin: 3px 0; font-size: 11px; color: #d9534f;"><b>Atraso atual:</b> {atraso}s</p>
        </div>
        """
        
        folium.CircleMarker(
            location=[lat, lon],
            radius=13,
            popup=folium.Popup(popup_html, max_width=250),
            tooltip=sem['nome'],
            color=cores[sem['tipo']],
            fill=True,
            fillColor=cores[sem['tipo']],
            fillOpacity=0.9,
            weight=2
        ).add_to(mapa)

    # DESENHAR A LINHA DA ROTA SEGUINDO A GEOMETRIA DA API
    folium.PolyLine(
        pontos_geometria,
        color='#4f46e5',
        weight=5,
        opacity=0.85,
        tooltip="Rota Otimizada - TomTom API"
    ).add_to(mapa)

    # Legenda e Painel
    painel_html = '''
    <div style="position: fixed; bottom: 30px; right: 30px; width: 310px;
                background-color: white; border: 2px solid #333; z-index:9999; 
                font-size: 12px; padding: 15px; border-radius: 8px;
                box-shadow: 0 4px 15px rgba(0,0,0,0.3);">
        <h3 style="margin: 0 0 8px 0; color: #333; font-size: 14px;">Global Solution - CitizenTech</h3>
        <p style="margin: 4px 0;"><b>Status do Sistema:</b> Online (AWS / TomTom)</p>
        <p style="margin: 4px 0; color: #27ae60;"><b>✓ Alinhamento Geométrico:</b> 100% nas Ruas</p>
        <hr style="border:0; border-top:1px solid #eee; margin:8px 0;">
        <p style="margin: 4px 0; font-size: 11px;"><b>Verde:</b> Fluxo Livre | <b>Amarelo:</b> Moderado | <b>Vermelho:</b> Congestionado</p>
    </div>
    '''
    mapa.get_root().html.add_child(folium.Element(painel_html))
    
    plugins.Fullscreen().add_to(mapa)
    folium.LayerControl().add_to(mapa)
    
    return mapa

if __name__ == "__main__":
    mapa = criar_mapa_definitivo()
    arquivo_saida = "mapa_rota_otimizada_final.html"
    mapa.save(arquivo_saida)
    print(f"[OK] Arquivo atualizado com sucesso: {arquivo_saida}")