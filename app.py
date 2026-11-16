from flask import Flask, render_template, send_file, jsonify
import os
from pathlib import Path
import psycopg2
from dotenv import load_dotenv
from datetime import datetime
import random

load_dotenv()

app = Flask(__name__, template_folder='.', static_folder='.')

# Configuração do banco de dados
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': int(os.getenv('DB_PORT', 5432)),
    'user': os.getenv('DB_USER', 'postgres'),
    'password': os.getenv('DB_PASSWORD', ''),
    'database': os.getenv('DB_NAME', 'global_solution_db')
}

# Verificar arquivos HTML disponíveis
HTML_FILES = {
    'dashboard_completo': 'DASHBOARD_COMPLETO.html',
    'dashboard': 'dashboard.html',
    'mapa': 'mapa_rota_otimizada_final.html'
}

# Variáveis globais para controlar modo simulação
db_connected = False

def conectar_banco():
    """Tenta conectar ao banco de dados"""
    global db_connected
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        db_connected = True
        return conn
    except Exception as e:
        db_connected = False
        return None

@app.route('/')
def index():
    return '''
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>CitizenTech - Global Solution</title>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
                padding: 20px;
            }
            .container {
                max-width: 1000px;
                width: 100%;
                background: white;
                border-radius: 15px;
                box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
                overflow: hidden;
            }
            .header {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 40px;
                text-align: center;
            }
            .header h1 {
                font-size: 2.5em;
                margin-bottom: 10px;
            }
            .header p {
                font-size: 1.1em;
                opacity: 0.9;
            }
            .content {
                padding: 40px;
            }
            .grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
                gap: 25px;
                margin-top: 30px;
            }
            .card {
                background: white;
                border: 2px solid #e0e0e0;
                border-radius: 10px;
                padding: 25px;
                text-align: center;
                transition: all 0.3s ease;
                cursor: pointer;
            }
            .card:hover {
                transform: translateY(-5px);
                box-shadow: 0 15px 40px rgba(0, 0, 0, 0.1);
                border-color: #667eea;
            }
            .card-icon {
                font-size: 3em;
                margin-bottom: 15px;
            }
            .card h3 {
                color: #333;
                font-size: 1.3em;
                margin-bottom: 10px;
            }
            .card p {
                color: #666;
                font-size: 0.95em;
                margin-bottom: 20px;
                line-height: 1.4;
            }
            .btn {
                display: inline-block;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 12px 30px;
                border: none;
                border-radius: 25px;
                font-size: 1em;
                font-weight: 600;
                cursor: pointer;
                transition: transform 0.3s ease;
                text-decoration: none;
            }
            .btn:hover {
                transform: scale(1.05);
            }
            .footer {
                background: #f5f5f5;
                padding: 20px;
                text-align: center;
                color: #666;
                font-size: 0.9em;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🚦 CitizenTech</h1>
                <p>Global Solution - Sistema Inteligente de Monitoramento de Tráfego</p>
            </div>
            <div class="content">
                <p style="text-align: center; color: #666; font-size: 1.1em;">
                    Acesse os dashboards e mapas interativos do sistema de otimização de tráfego
                </p>
                <div class="grid">
                    <div class="card">
                        <div class="card-icon">📊</div>
                        <h3>Dashboard Completo</h3>
                        <p>Visão geral com métricas de tráfego, semáforos e fluxo de veículos em tempo real</p>
                        <a href="/dashboard/completo" class="btn">Abrir Dashboard</a>
                    </div>
                    <div class="card">
                        <div class="card-icon">📈</div>
                        <h3>Dashboard</h3>
                        <p>Análise de dados e performance do sistema de semáforos</p>
                        <a href="/dashboard/principal" class="btn">Abrir Dashboard</a>
                    </div>
                    <div class="card">
                        <div class="card-icon">🗺️</div>
                        <h3>Mapa Interativo</h3>
                        <p>Visualização da rota dos semáforos, vias e pontos monitorados</p>
                        <a href="/dashboard/mapa" class="btn">Abrir Mapa</a>
                    </div>
                </div>
            </div>
            <div class="footer">
                <p>© 2025 CitizenTech - Desenvolvido para a Global Solution</p>
            </div>
        </div>
    </body>
    </html>
    '''

@app.route('/dashboard/completo')
def dashboard_completo():
    with open('DASHBOARD_COMPLETO.html', 'r', encoding='utf-8') as f:
        return f.read()

@app.route('/dashboard/principal')
def dashboard_principal():
    with open('dashboard.html', 'r', encoding='utf-8') as f:
        return f.read()

@app.route('/api/metricas')
def api_metricas():
    """API que retorna métricas atualizadas do banco de dados"""
    conn = conectar_banco()
    
    if conn:
        try:
            cursor = conn.cursor()
            # Consultar dados reais do banco
            cursor.execute("""
                SELECT 
                    AVG(velocidade_atual) as velocidade_media,
                    AVG(tempo_percurso_atual) as tempo_medio,
                    COUNT(*) as total_registros,
                    MAX(data_insercao) as ultima_atualizacao
                FROM fato_transito
                WHERE data_insercao >= NOW() - INTERVAL '30 minutes'
            """)
            
            resultado = cursor.fetchone()
            cursor.close()
            conn.close()
            
            if resultado:
                return jsonify({
                    'status': 'conectado',
                    'velocidade_media': round(resultado[0] or 0, 2),
                    'tempo_medio': round(resultado[1] or 0, 2),
                    'total_registros': resultado[2] or 0,
                    'ultima_atualizacao': resultado[3].isoformat() if resultado[3] else None,
                    'timestamp': datetime.now().isoformat()
                })
        except Exception as e:
            print(f"Erro ao consultar banco: {e}")
    
    # Modo simulação - retornar dados fake
    return jsonify({
        'status': 'simulacao',
        'velocidade_media': round(random.uniform(25, 45), 2),
        'tempo_medio': round(random.uniform(8, 15), 2),
        'total_registros': random.randint(50, 150),
        'ultima_atualizacao': datetime.now().isoformat(),
        'timestamp': datetime.now().isoformat(),
        'aviso': 'Banco de dados não conectado. Dados em modo simulação.'
    })

@app.route('/api/status-banco')
def api_status_banco():
    """Retorna status da conexão com o banco de dados"""
    conn = conectar_banco()
    
    if conn:
        conn.close()
        return jsonify({
            'banco_conectado': True,
            'mensagem': 'Banco de dados AWS conectado com sucesso',
            'dashboards_atualizando': True
        })
    else:
        return jsonify({
            'banco_conectado': False,
            'mensagem': 'Banco de dados AWS não está acessível. Sistema em modo simulação.',
            'dashboards_atualizando': False,
            'dica': 'Verifique credenciais em .env e segurança do banco na AWS'
        })

if __name__ == '__main__':
    # Testar conexão ao iniciar
    print("\n" + "="*60)
    print("INICIANDO SERVIDOR FLASK - CitizenTech")
    print("="*60)
    
    conn = conectar_banco()
    if conn:
        print("[OK] Banco de dados AWS conectado!")
        print("   Os dashboards ATUALIZARAO em tempo real")
        conn.close()
    else:
        print("[AVISO] Banco de dados não conectado")
        print("   Os dashboards funcionarão em MODO SIMULACAO")
        print("   Verifique as credenciais em .env")
    
    print("="*60)
    print(f"Servidor rodando em http://0.0.0.0:5000")
    print("="*60 + "\n")
    
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
