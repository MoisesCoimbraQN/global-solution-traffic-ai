#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Criar múltiplas versões do mapa com diferentes provedores de tiles
"""

import folium
import os

print("[INFO] Criando mapas com diferentes provedores...")

# Coordenadas de Belo Horizonte
bh_center = [-19.9167, -43.9345]

# Pontos da rota
pontos_rota = [
    {'nome': 'Centro - Saida', 'coords': [-19.9289, -43.9348], 'status': 'INICIO'},
    {'nome': 'Semaforo 1 - Av. Afonso Pena', 'coords': [-19.9265, -43.9320], 'status': 'OTIMIZADO'},
    {'nome': 'Semaforo 2 - Av. Getulio Vargas', 'coords': [-19.9210, -43.9280], 'status': 'OTIMIZADO'},
    {'nome': 'Semaforo 3 - Rua Bahia', 'coords': [-19.9175, -43.9250], 'status': 'OTIMIZADO'},
    {'nome': 'Savassi - Rua Inconfidentes', 'coords': [-19.9145, -43.9215], 'status': 'PASSANDO'},
    {'nome': 'Semaforo 4 - Av. Brasil', 'coords': [-19.9120, -43.9190], 'status': 'OTIMIZADO'},
    {'nome': 'Lourdes - Via Brasil', 'coords': [-19.9085, -43.9160], 'status': 'PASSANDO'},
    {'nome': 'Semaforo 5 - Av. Cristovao Colombo', 'coords': [-19.9050, -43.9130], 'status': 'OTIMIZADO'},
    {'nome': 'Funcionarios - Destino', 'coords': [-19.9020, -43.9100], 'status': 'FIM'},
]

# Provedores de tiles para testar
provedores = {
    'CartoDB Positron': 'CartoDB positron',
    'CartoDB Voyager': 'CartoDB voyager',
    'OpenTopoMap': 'OpenTopoMap',
    'Stamen Terrain': 'Stamen Terrain',
}

def criar_mapa(provedor_nome, provedor_tiles):
    """Criar mapa com provedor especificado"""
    
    mapa = folium.Map(
        location=bh_center,
        zoom_start=13,
        tiles=provedor_tiles,
        prefer_canvas=True
    )
    
    # Adicionar marcadores
    for ponto in pontos_rota:
        if ponto['status'] == 'INICIO':
            cor = 'green'
            icon = 'play'
        elif ponto['status'] == 'FIM':
            cor = 'red'
            icon = 'stop'
        elif ponto['status'] == 'OTIMIZADO':
            cor = 'blue'
            icon = 'check'
        else:
            cor = 'orange'
            icon = 'arrow-right'
        
        popup_html = f"""
        <div style="font-family: Arial; width: 250px;">
            <h4 style="margin: 0; color: #333;">{ponto['nome']}</h4>
            <hr style="margin: 5px 0;">
            <p style="margin: 5px 0;"><b>Status:</b> {ponto['status']}</p>
            <p style="margin: 5px 0;"><b>Provedor:</b> {provedor_nome}</p>
        </div>
        """
        
        folium.Marker(
            location=ponto['coords'],
            popup=folium.Popup(popup_html, max_width=300),
            tooltip=ponto['nome'],
            icon=folium.Icon(color=cor, icon=icon, prefix='fa')
        ).add_to(mapa)
    
    # Desenhar rota
    coords_rota = [p['coords'] for p in pontos_rota]
    folium.PolyLine(
        coords_rota,
        color='#FF6B6B',
        weight=4,
        opacity=0.8
    ).add_to(mapa)
    
    # Legenda
    legenda_html = f'''
    <div style="position: fixed; 
                bottom: 50px; right: 50px; width: 280px; height: auto; 
                background-color: white; border:3px solid #333; z-index:9999; 
                font-size:12px; padding: 15px; border-radius: 8px; box-shadow: 0 0 15px rgba(0,0,0,0.3);">
        <b style="font-size: 14px;">Mapa - {provedor_nome}</b>
        <hr style="margin: 8px 0;">
        
        <div style="margin: 8px 0;">
            <i style="background: #2ecc71; padding: 4px 10px; border-radius: 3px; color: white; font-weight: bold;">SAIDA</i>
        </div>
        
        <div style="margin: 8px 0;">
            <i style="background: #3498db; padding: 4px 10px; border-radius: 3px; color: white; font-weight: bold;">OTIMIZADO</i>
        </div>
        
        <div style="margin: 8px 0;">
            <i style="background: #f39c12; padding: 4px 10px; border-radius: 3px; color: white; font-weight: bold;">PASSANDO</i>
        </div>
        
        <div style="margin: 8px 0;">
            <i style="background: #e74c3c; padding: 4px 10px; border-radius: 3px; color: white; font-weight: bold;">DESTINO</i>
        </div>
        
        <hr style="margin: 8px 0;">
        <p style="margin: 5px 0; font-size: 11px; color: #666;">
            Provedor: {provedor_nome}
        </p>
    </div>
    '''
    
    mapa.get_root().html.add_child(folium.Element(legenda_html))
    
    return mapa

# Criar mapas
print("\n[INFO] Criando mapas com diferentes provedores...")
for nome, tiles in provedores.items():
    try:
        mapa = criar_mapa(nome, tiles)
        filename = f'mapa_{nome.lower().replace(" ", "_")}.html'
        mapa.save(filename)
        print(f"[OK] {nome}: {filename}")
    except Exception as e:
        print(f"[ERRO] {nome}: {str(e)}")

print("\n[INFO] Todos os mapas foram criados!")
print("[INFO] Teste cada um para ver qual funciona melhor no seu navegador")
