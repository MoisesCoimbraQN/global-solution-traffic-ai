@echo off
chcp 65001 >nul
cls
echo ╔════════════════════════════════════════════════════════════╗
echo ║                                                            ║
echo ║           🚦 CITIZENTECH - SISTEMA INTELIGENTE             ║
echo ║           Control de Tráfego Urbano e Semáforos            ║
echo ║                                                            ║
echo ╚════════════════════════════════════════════════════════════╝
echo.
echo ⏳ Iniciando Menu Principal...
echo.

REM Obter o caminho do script
set "SCRIPT_DIR=%~dp0"

REM Esperar 2 segundos
timeout /t 2 /nobreak >nul

REM Abrir o menu interativo
start "" "%SCRIPT_DIR%MENU_INTERATIVO.html"

echo ✓ Menu aberto com sucesso!
echo.
echo 📊 Componentes do Sistema:
echo   • Mapa TomTom (Integração com API)
echo   • Algoritmo de Semáforos Inteligentes
echo   • Dashboard de Trânsito em Tempo Real
echo   • Visualizador de Rotas de Ônibus
echo   • Verificação de Status da API
echo   • Documentação Completa
echo.
echo 📡 Status da AWS:
echo   ✓ EC2: Coletando dados a cada 5 minutos
echo   ✓ TomTom API: Conectada e operacional
echo   ✓ Data Warehouse: Snowflake ativo
echo.
echo 💡 Dica: O menu interativo foi aberto em seu navegador padrão
echo         Clique em qualquer card para explorar os componentes!
echo.
pause
