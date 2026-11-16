from flask import Flask, render_template, send_file
import os
from pathlib import Path

app = Flask(__name__, template_folder='.', static_folder='.')

# Verificar arquivos HTML disponíveis
HTML_FILES = {
    'dashboard_completo': 'DASHBOARD_COMPLETO.html',
    'dashboard': 'dashboard.html',
    'mapa': 'mapa_rota_otimizada_final.html'
}

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

@app.route('/dashboard/mapa')
def mapa():
    with open('mapa_rota_otimizada_final.html', 'r', encoding='utf-8') as f:
        return f.read()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
