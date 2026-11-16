"""
Script para adicionar auto-refresh com fetch da API aos dashboards
"""

import os

# Script de auto-refresh que será injetado
AUTO_REFRESH_SCRIPT = '''
<script>
// Auto-refresh a cada 30 segundos
let refreshInterval = setInterval(function() {
    fetch('/api/metricas')
        .then(response => response.json())
        .then(data => {
            console.log('[Dashboard] Dados atualizados:', data);
            
            // Atualizar elementos com atributo data-metric
            document.querySelectorAll('[data-metric]').forEach(element => {
                const metric = element.dataset.metric;
                if (data[metric] !== undefined) {
                    element.textContent = data[metric];
                }
            });
            
            // Atualizar timestamp
            const timestamp = new Date().toLocaleTimeString('pt-BR');
            const statusEl = document.getElementById('refresh-status');
            if (statusEl) {
                statusEl.textContent = 'Atualizado em: ' + timestamp;
                statusEl.style.color = '#4caf50';
            }
            
            // Se há dados, esconder aviso de simulação
            if (data.status === 'conectado') {
                const avisoEl = document.getElementById('aviso-simulacao');
                if (avisoEl) avisoEl.style.display = 'none';
            }
        })
        .catch(error => {
            console.error('[Dashboard] Erro ao buscar dados:', error);
            const statusEl = document.getElementById('refresh-status');
            if (statusEl) {
                statusEl.textContent = 'Erro ao conectar';
                statusEl.style.color = '#f44336';
            }
        });
}, 30000); // 30 segundos

// Primeira atualização imediata
fetch('/api/metricas')
    .then(response => response.json())
    .then(data => {
        console.log('[Dashboard] Carregamento inicial:', data);
        
        // Atualizar cards com métricas
        const metricas = {
            'velocidade_media': document.querySelector('[data-metric="velocidade_media"]'),
            'tempo_medio': document.querySelector('[data-metric="tempo_medio"]'),
            'total_registros': document.querySelector('[data-metric="total_registros"]')
        };
        
        for (let [key, element] of Object.entries(metricas)) {
            if (element && data[key] !== undefined) {
                element.textContent = data[key];
            }
        }
        
        // Atualizar status
        const statusEl = document.getElementById('refresh-status');
        if (statusEl) {
            const timestamp = new Date().toLocaleTimeString('pt-BR');
            statusEl.textContent = 'Atualizado em: ' + timestamp;
            statusEl.style.color = data.status === 'conectado' ? '#4caf50' : '#ff9800';
        }
    });

// Parar refresh ao sair da página
window.addEventListener('beforeunload', function() {
    clearInterval(refreshInterval);
});
</script>
'''

# Arquivos HTML a atualizar
html_files = [
    'dashboard.html',
    'DASHBOARD_COMPLETO.html'
]

for filename in html_files:
    filepath = os.path.join('.', filename)
    
    if not os.path.exists(filepath):
        print(f"[!] Arquivo não encontrado: {filename}")
        continue
    
    # Ler arquivo
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Verificar se já tem auto-refresh
    if 'refresh-status' in content:
        print(f"[OK] {filename} já tem auto-refresh injetado")
        continue
    
    # Injetar script antes de </body>
    if '</body>' in content:
        # Adicionar um elemento de status
        status_html = '''
    <div id="refresh-status" style="position: fixed; bottom: 20px; right: 20px; 
         background: #333; color: #fff; padding: 10px 15px; border-radius: 5px; 
         font-size: 12px; z-index: 9999; box-shadow: 0 2px 10px rgba(0,0,0,0.3);">
        Carregando...
    </div>
        '''
        
        content = content.replace('</body>', status_html + AUTO_REFRESH_SCRIPT + '</body>')
        
        # Escrever arquivo atualizado
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"[OK] {filename} atualizado com auto-refresh")
    else:
        print(f"[!] Tag </body> não encontrada em {filename}")

print("\n[OK] Dashboards prontos para auto-refresh!")
print("     Os dados serão atualizados a cada 30 segundos")
print("     Status aparecerá no canto inferior direito")
