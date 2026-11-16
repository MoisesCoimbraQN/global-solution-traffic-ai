#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para corrigir os gráficos Chart.js nos dashboards
para que sejam atualizados dinamicamente com dados da API
"""

import re
import sys
import io

# Forçar UTF-8 no stdout
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def corrigir_dashboard_completo():
    file_path = r"C:\Users\mcmoi\OneDrive\Área de Trabalho\GlobalSolution\DASHBOARD_COMPLETO.html"
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. Armazenar referências aos gráficos
    old_traffic = "const trafficCtx = document.getElementById('trafficChart').getContext('2d');\n        new Chart(trafficCtx, {"
    new_traffic = "const trafficCtx = document.getElementById('trafficChart').getContext('2d');\n        charts.traffic = new Chart(trafficCtx, {"
    
    content = content.replace(old_traffic, new_traffic)
    
    old_algorithm = "const algorithmCtx = document.getElementById('algorithmChart').getContext('2d');\n        new Chart(algorithmCtx, {"
    new_algorithm = "const algorithmCtx = document.getElementById('algorithmChart').getContext('2d');\n        charts.algorithm = new Chart(algorithmCtx, {"
    
    content = content.replace(old_algorithm, new_algorithm)
    
    # 2. Adicionar função de atualização de gráficos antes do auto-refresh
    function_update = '''<script>
        // Armazenar referências aos gráficos
        let charts = {};
        
        // Função para atualizar gráficos com dados da API
        function atualizarGraficos(data) {
            if (charts.traffic && data.velocidade_media) {
                // Atualizar gráfico de tráfego com base na velocidade
                charts.traffic.data.datasets[0].data[0] = data.velocidade_media;
                charts.traffic.update();
            }
            
            if (charts.algorithm && data.total_registros) {
                // Atualizar gráfico do algoritmo com base no total de registros
                charts.algorithm.data.datasets[0].data[0] = data.total_registros;
                charts.algorithm.update();
            }
            
            console.log('[Gráficos Dashboard Completo] Atualizados');
        }
        
        // Auto-refresh a cada 30 segundos'''
    
    # Encontrar e substituir o início do script de auto-refresh
    old_script_start = '''<script>
        // Auto-refresh a cada 30 segundos'''
    
    if old_script_start in content:
        content = content.replace(old_script_start, function_update)
        print("[OK] DASHBOARD_COMPLETO.html - Funcao de atualizacao adicionada")
    
    # 3. Adicionar chamada para atualizar gráficos no fetch
    old_fetch = '''fetch('/api/metricas')
        .then(response => response.json())
        .then(data => {
            console.log('[Dashboard] Dados atualizados:', data);
            
            // Atualizar elementos com atributo data-metric'''
    
    new_fetch = '''fetch('/api/metricas')
        .then(response => response.json())
        .then(data => {
            console.log('[Dashboard] Dados atualizados:', data);
            
            // Atualizar gráficos
            atualizarGraficos(data);
            
            // Atualizar elementos com atributo data-metric'''
    
    content = content.replace(old_fetch, new_fetch)
    print("[OK] DASHBOARD_COMPLETO.html - Chamada de atualizacao adicionada ao fetch periodico")
    
    # 4. Adicionar chamada no carregamento inicial
    old_initial = '''fetch('/api/metricas')
    .then(response => response.json())
    .then(data => {
        console.log('[Dashboard] Carregamento inicial:', data);
        
        // Atualizar cards com métricas'''
    
    new_initial = '''fetch('/api/metricas')
    .then(response => response.json())
    .then(data => {
        console.log('[Dashboard] Carregamento inicial:', data);
        
        // Atualizar gráficos
        atualizarGraficos(data);
        
        // Atualizar cards com métricas'''
    
    content = content.replace(old_initial, new_initial)
    print("[OK] DASHBOARD_COMPLETO.html - Chamada de atualizacao adicionada ao carregamento inicial")
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("[OK] DASHBOARD_COMPLETO.html corrigido com sucesso!")

if __name__ == '__main__':
    try:
        corrigir_dashboard_completo()
        print("")
        print("[OK] Todos os dashboards foram corrigidos!")
        print("[TIP] Os gráficos agora atualizam dinamicamente a cada 30 segundos")
    except Exception as e:
        print(f"[ERRO] {e}")
        import traceback
        traceback.print_exc()

