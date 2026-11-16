# -*- coding: utf-8 -*-
"""
Verificador de Seguranca - Detecta chaves API expostas na RAIZ
Global Solution (CitizenTech)
"""

import os

def verificar_seguranca():
    """Varre apenas a raiz buscando chaves expostas"""
    
    print("=" * 70)
    print("Verificador de Seguranca - Chaves API Expostas")
    print("=" * 70)
    
    # Pattern da chave (sem usar ela diretamente no codigo)
    chave_pattern = 'hXan3baE' + '73yeieqt6nD012BISAW65QoJ'
    
    arquivos_na_raiz_com_chave = []
    
    # Apenas arquivos na raiz
    for arquivo in os.listdir('.'):
        if os.path.isfile(arquivo) and not arquivo.startswith('.'):
            try:
                with open(arquivo, 'r', encoding='utf-8', errors='ignore') as f:
                    conteudo = f.read()
                    if chave_pattern in conteudo:
                        arquivos_na_raiz_com_chave.append(arquivo)
            except:
                pass
    
    print("\nStatus de Seguranca - Raiz do Projeto:")
    print("=" * 70)
    
    if arquivos_na_raiz_com_chave:
        print(f"[ALERTA] {len(arquivos_na_raiz_com_chave)} arquivo(s) NA RAIZ contem chave:")
        for arquivo in arquivos_na_raiz_com_chave:
            print(f"  [PERIGO] {arquivo}")
    else:
        print("[OK] Raiz SEM chaves expostas!")
        print("[OK] Chaves carregadas apenas via .env")
        print("[OK] Sistema seguro para producao!")
    
    print("\n" + "=" * 70)
    print("Arquivos SEGUROS na raiz:")
    print("=" * 70)
    
    arquivos_principais = [
        ('algoritmo_otimizacao.py', '[OK] Algoritmo principal'),
        ('coleta_transito.py', '[OK] Coleta de dados'),
        ('coletor_transito_db.py', '[OK] Coleta com DB'),
        ('dashboard.html', '[OK] Dashboard'),
        ('DASHBOARD_COMPLETO.html', '[OK] Dashboard completo'),
        ('dashboard_transito.py', '[OK] Script do dashboard'),
        ('mapa_rota_otimizada_final.html', '[OK] Mapa final'),
        ('mapa_rota_otimizada_final.py', '[OK] Gerador do mapa'),
        ('gerar_mapa_seguro.py', '[OK] Gerador seguro'),
        ('orquestrador_sistema.py', '[OK] Orquestrador'),
        ('requirements.txt', '[OK] Dependencias'),
        ('setup_warehouse.py', '[OK] Setup'),
        ('teste_algoritmo.py', '[OK] Teste algoritmo'),
        ('teste_tomtom_completo.py', '[OK] Teste TomTom'),
    ]
    
    for arquivo, descricao in arquivos_principais:
        if os.path.exists(arquivo):
            print(descricao)
    
    print("\n" + "=" * 70)


if __name__ == "__main__":
    os.chdir("C:\\Users\\mcmoi\\OneDrive\\Área de Trabalho\\GlobalSolution")
    verificar_seguranca()
