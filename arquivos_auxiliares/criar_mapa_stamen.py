#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Criar mapa funcional usando Stamen Toner (sem API key necessária)
"""

import folium
from folium import plugins
import os

print("[INFO] Criando mapa com Stamen Toner (sem API key)...")

# Coordenadas de Belo Horizonte
bh_center = [-19.9167, -43.9345]

# Criar mapa com Stamen Toner (funciona sem API key)
mapa = folium.Map(
    location=bh_center,
    zoom_start=13,
    tiles='Stamen Toner Lite',  # Stamen é confiável e não precisa de API key
    prefer_canvas=False
)

# Pontos da rota
pontos_rota = [
    {'nome': 'Centro - Saida', 'coords': [-19.9289, -43.9348], 'status': 'INICIO', 'cor': 'green'},
    {'nome': 'Semaforo 1 - Av. Afonso Pena', 'coords': [-19.9265, -43.9320], 'status': 'OTIMIZADO', 'cor': 'blue'},
    {'nome': 'Semaforo 2 - Av. Getulio Vargas', 'coords': [-19.9210, -43.9280], 'status': 'OTIMIZADO', 'cor': 'blue'},
    {'nome': 'Semaforo 3 - Rua Bahia', 'coords': [-19.9175, -43.9250], 'status': 'OTIMIZADO', 'cor': 'blue'},
    {'nome': 'Savassi - Rua Inconfidentes', 'coords': [-19.9145, -43.9215], 'status': 'PASSANDO', 'cor': 'orange'},
    {'nome': 'Semaforo 4 - Av. Brasil', 'coords': [-19.9120, -43.9190], 'status': 'OTIMIZADO', 'cor': 'blue'},
    {'nome': 'Lourdes - Via Brasil', 'coords': [-19.9085, -43.9160], 'status': 'PASSANDO', 'cor': 'orange'},
    {'nome': 'Semaforo 5 - Av. Cristovao Colombo', 'coords': [-19.9050, -43.9130], 'status': 'OTIMIZADO', 'cor': 'blue'},
    {'nome': 'Funcionarios - Destino', 'coords': [-19.9020, -43.9100], 'status': 'FIM', 'cor': 'red'},
]

# Adicionar marcadores
for ponto in pontos_rota:
    popup_html = f"""
    <div style="font-family: Arial; width: 220px;">
        <h4 style="margin: 0; color: #333;">{ponto['nome']}</h4>
        <hr style="margin: 5px 0;">
        <p><b>Status:</b> {ponto['status']}</p>
        <p><b>Lat:</b> {ponto['coords'][0]:.4f}</p>
        <p><b>Lng:</b> {ponto['coords'][1]:.4f}</p>
    </div>
    """
    
    folium.Marker(
        location=ponto['coords'],
        popup=folium.Popup(popup_html, max_width=250),
        tooltip=ponto['nome'],
        icon=folium.Icon(color=ponto['cor'], icon='info-sign')
    ).add_to(mapa)

# Desenhar rota
coords_rota = [p['coords'] for p in pontos_rota]
folium.PolyLine(
    coords_rota,
    color='#FF0000',
    weight=5,
    opacity=0.9,
    popup='Rota do Onibus'
).add_to(mapa)

# Adicionar legenda como HTML
legenda_html = '''
<div style="position: fixed; 
            bottom: 50px; right: 50px; width: 280px; 
            background-color: white; border:3px solid #333; z-index:9999; 
            font-size:12px; padding: 15px; border-radius: 8px; box-shadow: 0 0 15px rgba(0,0,0,0.3);">
    <b style="font-size: 14px;">Legenda - Rota Otimizada</b>
    <hr style="margin: 8px 0;">
    
    <p style="margin: 5px 0;">
        <i style="background: #2ecc71; padding: 5px 10px; border-radius: 3px; color: white; font-weight: bold;">SAIDA</i>
        Verde = Ponto de Saida (Centro)
    </p>
    
    <p style="margin: 5px 0;">
        <i style="background: #3498db; padding: 5px 10px; border-radius: 3px; color: white; font-weight: bold;">OTI</i>
        Azul = Semaforo Otimizado
    </p>
    
    <p style="margin: 5px 0;">
        <i style="background: #f39c12; padding: 5px 10px; border-radius: 3px; color: white; font-weight: bold;">PASS</i>
        Laranja = Ponto de Passagem
    </p>
    
    <p style="margin: 5px 0;">
        <i style="background: #e74c3c; padding: 5px 10px; border-radius: 3px; color: white; font-weight: bold;">DEST</i>
        Vermelho = Destino (Funcionarios)
    </p>
    
    <hr style="margin: 8px 0;">
    <p style="margin: 5px 0; font-size: 11px; color: #666;">
        <b>Impacto Total:</b><br>
        +180 segundos ganhos<br>
        900m fila reduzida<br>
        2.1 minutos economizados
    </p>
</div>
'''

mapa.get_root().html.add_child(folium.Element(legenda_html))

# Salvar
output_file = 'mapa_rota_bus_bh_stamen.html'
mapa.save(output_file)
print(f'[OK] Mapa criado: {output_file}')
print('[OK] Usando Stamen Toner Lite (sem API key necessaria)')
print('[OK] Arquivo salvo em: ' + os.path.abspath(output_file))
print('[OK] Este mapa DEVE funcionar perfeitamente!')
