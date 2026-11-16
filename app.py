"""
CitizenTech - Sistema de Otimização de Tráfego
Flask API para servir dashboards e dados em tempo real
"""

from flask import Flask, jsonify
import os
import psycopg2
from dotenv import load_dotenv
from datetime import datetime
import logging

load_dotenv()

app = Flask(__name__, static_folder=None, template_folder='.')

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuração do banco de dados
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': int(os.getenv('DB_PORT', 5432)),
    'user': os.getenv('DB_USER', 'postgres'),
    'password': os.getenv('DB_PASSWORD', ''),
    'database': os.getenv('DB_NAME', 'global_solution_db')
}

def conectar_banco():
    """Tenta conectar ao banco de dados"""
    try:
        conn = psycopg2.connect(
            host=DB_CONFIG['host'],
            port=DB_CONFIG['port'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password'],
            database=DB_CONFIG['database'],
            connect_timeout=5
        )
        return conn
    except Exception as e:
        logger.error(f"Erro ao conectar ao banco: {e}")
        return None

# ============================================================================
# ROTAS PRINCIPAL
# ============================================================================

@app.route('/')
def index():
    """Página inicial com cards dos dashboards"""
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
                <p>© 2026 CitizenTech - Desenvolvido para a Global Solution</p>
            </div>
        </div>
    </body>
    </html>
    '''

# ============================================================================
# ROTAS DOS DASHBOARDS
# ============================================================================

@app.route('/dashboard/completo')
def dashboard_completo():
    """Serve o Dashboard Completo com auto-refresh a cada 5 minutos"""
    try:
        with open('DASHBOARD_COMPLETO.html', 'r', encoding='utf-8') as f:
            html = f.read()
            # Injetar script de auto-refresh se não estiver presente
            if 'setInterval' not in html:
                html = html.replace('</body>', '''
                <script>
                // Auto-refresh a cada 5 minutos (300000ms)
                setInterval(function() {
                    fetch('/api/metricas')
                        .then(response => response.json())
                        .then(data => {
                            console.log('Dados atualizados:', data);
                            // Atualizar elementos do dashboard
                            document.querySelectorAll('[data-metric]').forEach(el => {
                                const metric = el.dataset.metric;
                                if (data[metric] !== undefined) {
                                    el.textContent = data[metric];
                                }
                            });
                        })
                        .catch(error => console.error('Erro ao buscar métricas:', error));
                }, 300000); // 5 minutos
                
                // Primeira atualização imediata
                fetch('/api/metricas')
                    .then(response => response.json())
                    .then(data => console.log('Status inicial:', data));
                </script>
                </body>''')
            return html
    except FileNotFoundError:
        return "Dashboard não encontrado", 404

@app.route('/dashboard/principal')
def dashboard_principal():
    """Serve o Dashboard Principal com auto-refresh a cada 5 minutos"""
    try:
        with open('dashboard.html', 'r', encoding='utf-8') as f:
            html = f.read()
            # Injetar script de auto-refresh se não estiver presente
            if 'setInterval' not in html:
                html = html.replace('</body>', '''
                <script>
                // Auto-refresh a cada 5 minutos
                setInterval(function() {
                    fetch('/api/metricas')
                        .then(response => response.json())
                        .then(data => {
                            console.log('Dashboard atualizado:', data);
                            document.querySelectorAll('[data-metric]').forEach(el => {
                                const metric = el.dataset.metric;
                                if (data[metric] !== undefined) {
                                    el.textContent = data[metric];
                                }
                            });
                        })
                        .catch(error => console.error('Erro:', error));
                }, 300000); // 5 minutos
                </script>
                </body>''')
            return html
    except FileNotFoundError:
        return "Dashboard não encontrado", 404

@app.route('/dashboard/mapa')
def dashboard_mapa():
    """Serve o Mapa Interativo"""
    try:
        with open('mapa_rota_otimizada_final.html', 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return "Mapa não encontrado", 404

# ============================================================================
# ROTAS API
# ============================================================================

@app.route('/api/metricas', methods=['GET'])
def api_metricas():
    """
    Retorna métricas atualizadas do banco de dados
    Atualizado a cada 5 minutos pela AWS/PostgreSQL
    """
    conn = conectar_banco()
    
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT 
                    AVG(velocidade_atual) as velocidade_media,
                    AVG(tempo_viagem_segundos) as tempo_medio,
                    COUNT(*) as total_registros
                FROM fato_transito_tempo_real
            """)
            
            resultado = cursor.fetchone()
            cursor.close()
            conn.close()
            
            if resultado and resultado[0] is not None:
                return jsonify({
                    'status': 'conectado',
                    'velocidade_media': round(float(resultado[0]), 2),
                    'tempo_medio': round(float(resultado[1]), 2) if resultado[1] else 0,
                    'total_registros': int(resultado[2]),
                    'timestamp': datetime.now().isoformat(),
                    'banco': 'AWS PostgreSQL - Atualizado a cada 5 minutos'
                })
        except Exception as e:
            logger.error(f"Erro ao consultar banco: {e}")
            conn.close()
    
    # Fallback: modo simulação
    import random
    return jsonify({
        'status': 'simulacao',
        'velocidade_media': round(random.uniform(25, 45), 2),
        'tempo_medio': round(random.uniform(8, 15), 2),
        'total_registros': random.randint(50, 150),
        'timestamp': datetime.now().isoformat(),
        'aviso': 'Banco de dados em fallback. Dados simulados.'
    })

@app.route('/api/status-banco', methods=['GET'])
def api_status_banco():
    """Retorna o status da conexão com o banco de dados"""
    conn = conectar_banco()
    
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM fato_transito_tempo_real")
            count = cursor.fetchone()[0]
            cursor.close()
            conn.close()
            
            return jsonify({
                'banco_conectado': True,
                'mensagem': 'Banco de dados AWS conectado com sucesso',
                'dashboards_atualizando': True,
                'registros_total': count,
                'atualizacao': 'Automática a cada 5 minutos'
            })
        except Exception as e:
            logger.error(f"Erro ao consultar status: {e}")
            conn.close()
    
    return jsonify({
        'banco_conectado': False,
        'mensagem': 'Banco de dados não acessível. Sistema em fallback.',
        'dashboards_atualizando': False,
        'atualizacao': 'Dados simulados'
    }), 503

# ============================================================================
# INICIALIZAÇÃO
# ============================================================================

if __name__ == '__main__':
    print("\n" + "="*70)
    print("CITIZENTECH - Sistema de Otimizacao de Trafego")
    print("="*70)
    
    # Testar conexão ao iniciar
    conn = conectar_banco()
    if conn:
        print("[OK] Banco de dados AWS: CONECTADO")
        print("   Dashboards atualizarao automaticamente a cada 5 minutos")
        conn.close()
    else:
        print("[!] Banco de dados AWS: DESCONECTADO")
        print("   Sistema operando em modo fallback (dados simulados)")
    
    print("="*70)
    print("Servidor iniciando em http://0.0.0.0:5000")
    print("="*70 + "\n")
    
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
