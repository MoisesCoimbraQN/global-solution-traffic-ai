# -*- coding: utf-8 -*-
"""
Mapa com Rota Real usando OSMnx e Networkx - Global Solution
Folium + OpenStreetMap + TomTom Traffic
"""

import folium
from folium import plugins
import networkx as nx
import os

try:
    import osmnx as ox
except ImportError:
    print("Instalando osmnx...")
    os.system("pip install osmnx -q")
    import osmnx as ox

# Chave da TomTom
TOMTOM_API_KEY = "hXan3baE73yeieqt6nD012BISAW65QoJ"

def obter_rota_via_graph(G, ponto_inicio, ponto_fim):
    """Encontra a rota mais curta usando networkx"""
    
    try:
        # Encontrar nós mais próximos
        no_inicio = ox.nearest_nodes(G, ponto_inicio[1], ponto_inicio[0])
        no_fim = ox.nearest_nodes(G, ponto_fim[1], ponto_fim[0])
        
        # Calcular caminho mais curto
        caminho = nx.shortest_path(G, no_inicio, no_fim, weight='length')
        
        # Extrair coordenadas do caminho
        coordenadas = []
        for no in caminho:
            node = G.nodes[no]
            coordenadas.append([node['y'], node['x']])
        
        return coordenadas
        
    except Exception as e:
        print(f"    Erro ao calcular rota: {e}")
        return None


def criar_mapa_com_rota_osmnx():
    """Cria mapa com rota real usando OSMnx"""
    
    # Centro de Belo Horizonte
    centro_bh = [-19.9167, -43.9345]
    
    print("Baixando malha de ruas de Belo Horizonte...")
    
    # Baixar grafo de ruas (raio de 3km)
    try:
        G = ox.graph_from_point(
            center_point=(centro_bh[0], centro_bh[1]),
            dist=3000,
            simplify=True,
            network_type='drive'
        )
        print(f"OK - {len(G.nodes)} pontos de rua obtidos")
    except Exception as e:
        print(f"Erro ao baixar grafo: {e}")
        print("Usando fallback com rota simplificada...")
        G = None
    
    # Criar mapa base
    mapa = folium.Map(
        location=centro_bh,
        zoom_start=13,
        tiles='https://tile.openstreetmap.de/tiles/osmde/{z}/{x}/{y}.png',
        attr='&copy; OpenStreetMap DE',
        prefer_canvas=False
    )
    
    # Adicionar camada de Trafego em Tempo Real
    folium.TileLayer(
        tiles=f'https://api.tomtom.com/traffic/map/4/tile/Relative/{{z}}/{{x}}/{{y}}.png?key={TOMTOM_API_KEY}',
        attr='TomTom Traffic',
        name='TomTom Traffic (Tempo Real)',
        overlay=True,
        control=True,
        opacity=0.7
    ).add_to(mapa)
    
    # Pontos da rota
    pontos = [
        {'nome': 'Centro - Saida', 'lat': -19.9289, 'lng': -43.9348, 'tipo': 'INICIO'},
        {'nome': 'Semaforo 1', 'lat': -19.9265, 'lng': -43.9320, 'tipo': 'OTIMIZADO'},
        {'nome': 'Semaforo 2', 'lat': -19.9210, 'lng': -43.9280, 'tipo': 'OTIMIZADO'},
        {'nome': 'Semaforo 3', 'lat': -19.9175, 'lng': -43.9250, 'tipo': 'OTIMIZADO'},
        {'nome': 'Savassi', 'lat': -19.9145, 'lng': -43.9215, 'tipo': 'PASSAGEM'},
        {'nome': 'Semaforo 4', 'lat': -19.9120, 'lng': -43.9190, 'tipo': 'OTIMIZADO'},
        {'nome': 'Lourdes', 'lat': -19.9085, 'lng': -43.9160, 'tipo': 'PASSAGEM'},
        {'nome': 'Semaforo 5', 'lat': -19.9050, 'lng': -43.9130, 'tipo': 'OTIMIZADO'},
        {'nome': 'Funcionarios', 'lat': -19.9020, 'lng': -43.9100, 'tipo': 'FIM'}
    ]
    
    cores = {
        'INICIO': '#2ecc71',
        'OTIMIZADO': '#3498db',
        'PASSAGEM': '#f39c12',
        'FIM': '#e74c3c'
    }
    
    # Adicionar marcadores
    for ponto in pontos:
        folium.CircleMarker(
            location=[ponto['lat'], ponto['lng']],
            radius=12,
            popup=ponto['nome'],
            color=cores[ponto['tipo']],
            fill=True,
            fillColor=cores[ponto['tipo']],
            fillOpacity=0.8,
            weight=3,
            opacity=1
        ).add_to(mapa)
    
    # Desenhar rotas
    print("Calculando rotas reais entre os pontos...")
    
    todas_as_coordenadas = []
    
    for i in range(len(pontos) - 1):
        ponto_atual = [pontos[i]['lat'], pontos[i]['lng']]
        ponto_proximo = [pontos[i + 1]['lat'], pontos[i + 1]['lng']]
        
        print(f"  {i + 1}. {pontos[i]['nome']} -> {pontos[i + 1]['nome']}")
        
        if G:
            rota = obter_rota_via_graph(G, ponto_atual, ponto_proximo)
            if rota and len(rota) > 2:
                todas_as_coordenadas.extend(rota)
                print(f"     OK - {len(rota)} pontos")
            else:
                print(f"     Linha reta (fallback)")
                todas_as_coordenadas.append(ponto_atual)
                todas_as_coordenadas.append(ponto_proximo)
        else:
            todas_as_coordenadas.append(ponto_atual)
            todas_as_coordenadas.append(ponto_proximo)
    
    # Desenhar a rota
    if todas_as_coordenadas:
        folium.PolyLine(
            todas_as_coordenadas,
            color='#6366f1',
            weight=4,
            opacity=0.8,
            popup='Rota otimizada'
        ).add_to(mapa)
        print(f"\nRota desenhada com {len(todas_as_coordenadas)} pontos\n")
    
    # Legenda
    legenda_html = '''
    <div style="position: fixed; bottom: 30px; right: 30px; width: 300px;
                background-color: white; border:2px solid grey; z-index:9999; 
                font-size:12px; padding: 15px; border-radius: 8px;
                box-shadow: 0 4px 15px rgba(0,0,0,0.2);">
        
        <h4 style="margin: 0 0 12px 0; color: #333;">Legenda - Rota Real</h4>
        
        <div style="margin: 8px 0;">
            <span style="color: #2ecc71; font-weight: bold;">●</span> INICIO
        </div>
        <div style="margin: 8px 0;">
            <span style="color: #3498db; font-weight: bold;">●</span> SEMAFORO
        </div>
        <div style="margin: 8px 0;">
            <span style="color: #f39c12; font-weight: bold;">●</span> PASSAGEM
        </div>
        <div style="margin: 8px 0;">
            <span style="color: #e74c3c; font-weight: bold;">●</span> DESTINO
        </div>
        <div style="margin: 8px 0;">
            <span style="color: #6366f1; font-weight: bold;">━━━</span> Rota real
        </div>
        
        <hr style="margin: 10px 0; border: none; border-top: 1px solid #ddd;">
        
        <div style="font-size: 11px; background: #e8f4f8; padding: 8px; border-radius: 4px;">
            <b>Trafego (TomTom):</b>
            <p>Verde = Fluxo livre</p>
            <p>Amarelo = Lentidao</p>
            <p>Vermelho = Congestion</p>
        </div>
    </div>
    '''
    
    mapa.get_root().html.add_child(folium.Element(legenda_html))
    
    # Titulo
    titulo_html = '''
    <div style="position: fixed; top: 20px; left: 20px; width: 320px;
                background-color: white; border-radius: 8px; z-index:9999; 
                padding: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.2);">
        <h2 style="margin: 0 0 5px 0; font-size: 18px; color: #333;">
            Mapa com Trafego Real
        </h2>
        <p style="margin: 0 0 8px 0; font-size: 12px; color: #666;">
            Belo Horizonte - Rota Real pelas Ruas
        </p>
        <div style="margin-top: 10px; padding-top: 10px; border-top: 1px solid #ddd; font-size: 11px; color: #666;">
            <p style="margin: 2px 0;"><b>Dados:</b> OSMnx + TomTom Traffic</p>
            <span style="background: #2ecc71; color: white; padding: 4px 8px; border-radius: 4px; font-size: 10px; font-weight: bold;">
                MAPA ATIVO
            </span>
        </div>
    </div>
    '''
    
    mapa.get_root().html.add_child(folium.Element(titulo_html))
    
    # Controles
    plugins.Fullscreen().add_to(mapa)
    folium.LayerControl().add_to(mapa)
    
    return mapa


def main():
    print("=" * 70)
    print("Gerando Mapa com Rota Real (OSMnx + Networkx)")
    print("=" * 70)
    print()
    
    mapa = criar_mapa_com_rota_osmnx()
    
    arquivo_saida = "mapa_rota_real.html"
    mapa.save(arquivo_saida)
    
    print("=" * 70)
    print(f"Mapa gerado: {arquivo_saida}")
    print(f"Tamanho: {os.path.getsize(arquivo_saida) / 1024:.1f} KB")
    print("=" * 70)
    print("\nAbra o arquivo para visualizar a rota real!")


if __name__ == "__main__":
    main()
