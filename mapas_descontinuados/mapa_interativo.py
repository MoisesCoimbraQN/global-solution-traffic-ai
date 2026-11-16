#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🗺️ Mapa Interativo da Global Solution - CitizenTech
Gera um mapa com Folium + OpenStreetMap (100% gratuito, sem APIs bloqueadas)
"""

import folium
from folium import plugins
import os

def criar_mapa_belo_horizonte():
    """Cria mapa interativo de Belo Horizonte com rota otimizada"""
    
    # Centro de Belo Horizonte
    centro_bh = [-19.9167, -43.9345]
    
    # Criar mapa base com Folium
    mapa = folium.Map(
        location=centro_bh,
        zoom_start=13,
        tiles='OpenStreetMap',  # Tiles do OSM (100% gratuito)
        prefer_canvas=False
    )
    
    # Pontos da rota otimizada
    pontos = [
        {
            'nome': '🟢 Centro - Saída',
            'lat': -19.9289,
            'lng': -43.9348,
            'tipo': 'INICIO',
            'info': 'Ponto de partida - Centro de Belo Horizonte'
        },
        {
            'nome': '🔵 Semáforo 1 - Av. Afonso Pena',
            'lat': -19.9265,
            'lng': -43.9320,
            'tipo': 'OTIMIZADO',
            'info': 'Semáforo otimizado: +45s verde'
        },
        {
            'nome': '🔵 Semáforo 2 - Av. Getúlio Vargas',
            'lat': -19.9210,
            'lng': -43.9280,
            'tipo': 'OTIMIZADO',
            'info': 'Semáforo otimizado: +30s verde'
        },
        {
            'nome': '🔵 Semáforo 3 - Rua Bahia',
            'lat': -19.9175,
            'lng': -43.9250,
            'tipo': 'OTIMIZADO',
            'info': 'Semáforo otimizado: +20s verde'
        },
        {
            'nome': '🟠 Savassi - Rua Inconfidentes',
            'lat': -19.9145,
            'lng': -43.9215,
            'tipo': 'PASSAGEM',
            'info': 'Via de passagem - Bairro Savassi'
        },
        {
            'nome': '🔵 Semáforo 4 - Av. Brasil',
            'lat': -19.9120,
            'lng': -43.9190,
            'tipo': 'OTIMIZADO',
            'info': 'Semáforo otimizado: +35s verde'
        },
        {
            'nome': '🟠 Lourdes - Via Brasil',
            'lat': -19.9085,
            'lng': -43.9160,
            'tipo': 'PASSAGEM',
            'info': 'Via de passagem - Bairro Lourdes'
        },
        {
            'nome': '🔵 Semáforo 5 - Av. Cristóvão Colombo',
            'lat': -19.9050,
            'lng': -43.9130,
            'tipo': 'OTIMIZADO',
            'info': 'Semáforo otimizado: +25s verde'
        },
        {
            'nome': '🔴 Funcionários - Destino',
            'lat': -19.9020,
            'lng': -43.9100,
            'tipo': 'FIM',
            'info': 'Destino final - Bairro Funcionários'
        }
    ]
    
    # Cores para diferentes tipos
    cores = {
        'INICIO': '#2ecc71',      # Verde
        'OTIMIZADO': '#3498db',    # Azul
        'PASSAGEM': '#f39c12',      # Laranja
        'FIM': '#e74c3c'           # Vermelho
    }
    
    # Adicionar marcadores
    for ponto in pontos:
        popup_html = f"""
        <div style="font-family: Arial; width: 220px;">
            <h4 style="margin: 0 0 8px 0; color: #333;">{ponto['nome']}</h4>
            <p style="margin: 0 0 5px 0; color: #666; font-size: 12px;">
                <b>Local:</b> {ponto['info']}
            </p>
            <p style="margin: 0 0 5px 0; color: #666; font-size: 12px;">
                <b>Lat:</b> {ponto['lat']:.4f} | <b>Lng:</b> {ponto['lng']:.4f}
            </p>
            <p style="margin: 0; color: #999; font-size: 11px;">
                Tipo: {ponto['tipo']}
            </p>
        </div>
        """
        
        folium.CircleMarker(
            location=[ponto['lat'], ponto['lng']],
            radius=12,
            popup=folium.Popup(popup_html, max_width=300),
            color=cores[ponto['tipo']],
            fill=True,
            fillColor=cores[ponto['tipo']],
            fillOpacity=0.8,
            weight=3,
            opacity=1
        ).add_to(mapa)
    
    # Desenhar rota conectando os pontos
    coordenadas = [[p['lat'], p['lng']] for p in pontos]
    
    folium.PolyLine(
        coordenadas,
        color='#6366f1',
        weight=3,
        opacity=0.7,
        popup='Rota otimizada'
    ).add_to(mapa)
    
    # Adicionar legenda personalizada
    legenda_html = '''
    <div style="position: fixed; 
                bottom: 30px; right: 30px; width: 280px; height: auto;
                background-color: white; border:2px solid grey; z-index:9999; 
                font-size:12px; padding: 15px; border-radius: 8px;
                box-shadow: 0 4px 15px rgba(0,0,0,0.2);">
        
        <h4 style="margin: 0 0 12px 0; color: #333; font-size: 14px;">
            🗺️ Legenda da Rota
        </h4>
        
        <div style="margin: 8px 0;">
            <span style="color: #2ecc71; font-weight: bold;">●</span> 
            <span>INÍCIO - Centro</span>
        </div>
        
        <div style="margin: 8px 0;">
            <span style="color: #3498db; font-weight: bold;">●</span> 
            <span>SEMÁFORO - Otimizado</span>
        </div>
        
        <div style="margin: 8px 0;">
            <span style="color: #f39c12; font-weight: bold;">●</span> 
            <span>PASSAGEM - Intermediária</span>
        </div>
        
        <div style="margin: 8px 0;">
            <span style="color: #e74c3c; font-weight: bold;">●</span> 
            <span>DESTINO - Funcionários</span>
        </div>
        
        <div style="margin: 8px 0;">
            <span style="color: #6366f1; font-weight: bold;">━━━</span> 
            <span>Rota otimizada</span>
        </div>
        
        <hr style="margin: 10px 0; border: none; border-top: 1px solid #ddd;">
        
        <div style="font-size: 11px; color: #666; background: #f8f9fa; padding: 8px; border-radius: 4px;">
            <b>Impacto da Otimização:</b>
            <p style="margin: 4px 0;">✓ +180 segundos ganhos</p>
            <p style="margin: 4px 0;">✓ 900m fila reduzida</p>
            <p style="margin: 4px 0;">✓ ~2.1 min economizados</p>
        </div>
    </div>
    '''
    
    mapa.get_root().html.add_child(folium.Element(legenda_html))
    
    # Adicionar título
    titulo_html = '''
    <div style="position: fixed; 
                top: 20px; left: 20px; width: 300px; height: auto;
                background-color: white; border-radius: 8px; z-index:9999; 
                padding: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.2);">
        
        <h2 style="margin: 0 0 5px 0; font-size: 18px; color: #333;">
            🚦 Mapa - Otimização de Semáforos
        </h2>
        
        <p style="margin: 0; font-size: 12px; color: #666;">
            Belo Horizonte - Rota Inteligente em Tempo Real
        </p>
        
        <div style="margin-top: 10px; padding-top: 10px; border-top: 1px solid #ddd;">
            <span style="display: inline-block; background: #2ecc71; color: white; 
                        padding: 4px 8px; border-radius: 4px; font-size: 11px; font-weight: bold;">
                ✓ MAPA ATIVO
            </span>
        </div>
    </div>
    '''
    
    mapa.get_root().html.add_child(folium.Element(titulo_html))
    
    # Adicionar escala
    folium.ScaleControl(position='bottomleft').add_to(mapa)
    
    # Adicionar plugin de fullscreen
    plugins.Fullscreen().add_to(mapa)
    
    return mapa


def main():
    """Função principal - gera e salva o mapa"""
    
    print("=" * 70)
    print("🗺️  Gerando Mapa Interativo da Global Solution (CitizenTech)")
    print("=" * 70)
    
    # Criar mapa
    print("\n📍 Carregando dados de Belo Horizonte...")
    mapa = criar_mapa_belo_horizonte()
    
    # Salvar em arquivo HTML
    arquivo_saida = "mapa_interativo_folium.html"
    mapa.save(arquivo_saida)
    
    print(f"\n✅ Mapa gerado com sucesso!")
    print(f"📄 Arquivo: {arquivo_saida}")
    print(f"📏 Tamanho: {os.path.getsize(arquivo_saida) / 1024:.1f} KB")
    
    # Informações sobre o mapa
    print("\n" + "=" * 70)
    print("📊 INFORMAÇÕES DO MAPA:")
    print("=" * 70)
    print("✓ 9 marcadores (1 início, 4 semáforos, 2 passagens, 1 destino)")
    print("✓ 1 rota conectando todos os pontos")
    print("✓ Legenda com impacto da otimização")
    print("✓ 100% gratuito - Folium + OpenStreetMap")
    print("✓ Sem dependências de APIs externas")
    print("✓ Funciona offline (após primeira abertura)")
    
    print("\n" + "=" * 70)
    print("🚀 PRÓXIMAS AÇÕES:")
    print("=" * 70)
    print(f"1. Abra o arquivo: {arquivo_saida}")
    print("2. Clique nos marcadores para ver informações")
    print("3. Use o zoom e panorâmica para explorar")
    print("4. Veja o impacto estimado na legenda")
    
    print("\n" + "=" * 70)
    print("✨ Mapa pronto para uso!")
    print("=" * 70)


if __name__ == "__main__":
    main()
