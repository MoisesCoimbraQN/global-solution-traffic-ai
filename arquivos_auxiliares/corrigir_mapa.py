#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Corrigir mapa usando CartoDB ao invés de OpenStreetMap
"""

import folium
import os

print("[INFO] Criando novo mapa com CartoDB...")

# Coordenadas de Belo Horizonte
bh_center = [-19.9167, -43.9345]

# Criar mapa com CartoDB (funciona melhor que OSM)
mapa = folium.Map(
    location=bh_center,
    zoom_start=13,
    tiles='CartoDB positron',
    prefer_canvas=True
)

# Pontos da rota (Centro -> Savassi -> Lourdes -> Funcionários)
pontos_rota = [
    {'nome': 'Centro - Saída', 'coords': [-19.9289, -43.9348], 'status': 'INICIO'},
    {'nome': 'Semáforo 1 - Av. Afonso Pena', 'coords': [-19.9265, -43.9320], 'status': 'OTIMIZADO'},
    {'nome': 'Semáforo 2 - Av. Getúlio Vargas', 'coords': [-19.9210, -43.9280], 'status': 'OTIMIZADO'},
    {'nome': 'Semáforo 3 - Rua Bahia', 'coords': [-19.9175, -43.9250], 'status': 'OTIMIZADO'},
    {'nome': 'Savassi - Rua Inconfidentes', 'coords': [-19.9145, -43.9215], 'status': 'PASSANDO'},
    {'nome': 'Semáforo 4 - Av. Brasil', 'coords': [-19.9120, -43.9190], 'status': 'OTIMIZADO'},
    {'nome': 'Lourdes - Via Brasil', 'coords': [-19.9085, -43.9160], 'status': 'PASSANDO'},
    {'nome': 'Semáforo 5 - Av. Cristóvão Colombo', 'coords': [-19.9050, -43.9130], 'status': 'OTIMIZADO'},
    {'nome': 'Funcionários - Destino', 'coords': [-19.9020, -43.9100], 'status': 'FIM'},
]

# Adicionar marcadores
for ponto in pontos_rota:
    if ponto['status'] == 'INICIO':
        cor = 'green'
        icon = 'play'
        titulo = '[SAÍDA] ' + ponto['nome']
    elif ponto['status'] == 'FIM':
        cor = 'red'
        icon = 'stop'
        titulo = '[DESTINO] ' + ponto['nome']
    elif ponto['status'] == 'OTIMIZADO':
        cor = 'blue'
        icon = 'check'
        titulo = '[OTIMIZADO] ' + ponto['nome']
    else:
        cor = 'orange'
        icon = 'arrow-right'
        titulo = '[PASSANDO] ' + ponto['nome']
    
    popup_html = f"""
    <div style="font-family: Arial; width: 250px;">
        <h4 style="margin: 0; color: #333;">{titulo}</h4>
        <hr style="margin: 5px 0;">
        <p style="margin: 5px 0;"><b>Status:</b> {ponto['status']}</p>
        <p style="margin: 5px 0;"><b>Coordenadas:</b> {ponto['coords'][0]:.4f}, {ponto['coords'][1]:.4f}</p>
    </div>
    """
    
    folium.Marker(
        location=ponto['coords'],
        popup=folium.Popup(popup_html, max_width=300),
        tooltip=ponto['nome'],
        icon=folium.Icon(color=cor, icon=icon, prefix='fa')
    ).add_to(mapa)

# Desenhar a rota
coords_rota = [p['coords'] for p in pontos_rota]
folium.PolyLine(
    coords_rota,
    color='#FF6B6B',
    weight=4,
    opacity=0.8,
    popup='Rota do Ônibus'
).add_to(mapa)

# Adicionar legenda
legenda_html = '''
<div style="position: fixed; 
            bottom: 50px; right: 50px; width: 280px; height: auto; 
            background-color: white; border:3px solid #333; z-index:9999; 
            font-size:12px; padding: 15px; border-radius: 8px; box-shadow: 0 0 15px rgba(0,0,0,0.3);">
    <b style="font-size: 14px;">🚌 Legenda - Rota Otimizada</b>
    <hr style="margin: 8px 0;">
    
    <div style="margin: 8px 0;">
        <i style="background: #2ecc71; padding: 4px 10px; border-radius: 3px; color: white; font-weight: bold;">●</i>
        <b>Verde</b> = Ponto de Saída
    </div>
    
    <div style="margin: 8px 0;">
        <i style="background: #3498db; padding: 4px 10px; border-radius: 3px; color: white; font-weight: bold;">✓</i>
        <b>Azul</b> = Semáforo Otimizado
    </div>
    
    <div style="margin: 8px 0;">
        <i style="background: #f39c12; padding: 4px 10px; border-radius: 3px; color: white; font-weight: bold;">→</i>
        <b>Laranja</b> = Passando
    </div>
    
    <div style="margin: 8px 0;">
        <i style="background: #e74c3c; padding: 4px 10px; border-radius: 3px; color: white; font-weight: bold;">⬛</i>
        <b>Vermelho</b> = Destino
    </div>
    
    <hr style="margin: 8px 0;">
    <p style="margin: 5px 0; font-size: 11px; color: #666;">
        <b>Impacto Total:</b><br>
        • 180 segundos ganhos<br>
        • 900m fila reduzida<br>
        • ~2.1 minutos economizados
    </p>
</div>
'''

mapa.get_root().html.add_child(folium.Element(legenda_html))

# Salvar
output_file = 'mapa_rota_bus_bh_cartodb.html'
mapa.save(output_file)
print('[OK] Mapa criado com sucesso: ' + output_file)
print('[OK] Usando CartoDB ao invés de OpenStreetMap')
print('[OK] Mapa deve carregar corretamente agora!')
print('[OK] Arquivo salvo em: ' + os.path.abspath(output_file))
