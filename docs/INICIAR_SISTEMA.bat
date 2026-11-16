@echo off
:: ╔════════════════════════════════════════════════════════════╗
:: ║   CitizenTech - Script de Inicialização do Sistema          ║
:: ║   Controle Inteligente de Tráfego Urbano                   ║
:: ╚════════════════════════════════════════════════════════════╝

chcp 65001 >nul
cls

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║                                                            ║
echo ║           🚦 CITIZENTECH - INICIALIZADOR                   ║
echo ║           Sistema Inteligente de Tráfego Urbano             ║
echo ║                                                            ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

setlocal enabledelayedexpansion

set "BASE_DIR=%~dp0"

:MENU
cls
echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║                   MENU PRINCIPAL                           ║
echo ╚════════════════════════════════════════════════════════════╝
echo.
echo   1. 🗺️  Abrir Mapa TomTom (Interativo)
echo   2. 📊 Abrir Dashboard Completo
echo   3. 🎯 Menu Principal (Todos os Componentes)
echo   4. 🧠 Executar Algoritmo de Semáforos
echo   5. 📡 Testar Conexão com TomTom API
echo   6. 📚 Ver Documentação
echo   7. 🐍 Ativar Ambiente Virtual
echo   8. 🌐 Ver Guia de Uso
echo   9. ❌ Sair
echo.

set /p CHOICE="Escolha uma opção (1-9): "

if "%CHOICE%"=="1" goto MAPA
if "%CHOICE%"=="2" goto DASHBOARD
if "%CHOICE%"=="3" goto MENU_PRINCIPAL
if "%CHOICE%"=="4" goto ALGORITMO
if "%CHOICE%"=="5" goto TESTE_API
if "%CHOICE%"=="6" goto DOCUMENTACAO
if "%CHOICE%"=="7" goto VENV
if "%CHOICE%"=="8" goto GUIA
if "%CHOICE%"=="9" goto SAIR
goto MENU

:MAPA
cls
echo.
echo ⏳ Abrindo Mapa TomTom...
echo.
start "" "%BASE_DIR%mapa_tomtom_oficial.html"
timeout /t 2 /nobreak >nul
echo ✓ Mapa aberto com sucesso!
echo.
echo 💡 Dica: Use os controles do mapa para:
echo    • Zoom e pan
echo    • Ver rotas de ônibus
echo    • Localizar semáforos
echo    • Visualizar tráfego em tempo real
echo.
pause
goto MENU

:DASHBOARD
cls
echo.
echo ⏳ Abrindo Dashboard Completo...
echo.
start "" "%BASE_DIR%DASHBOARD_COMPLETO.html"
timeout /t 2 /nobreak >nul
echo ✓ Dashboard aberto com sucesso!
echo.
echo 📊 Você pode visualizar:
echo    • Status do tráfego em tempo real
echo    • Métricas do algoritmo inteligente
echo    • Dados da API TomTom
echo    • Status do Data Warehouse
echo    • Informações da AWS EC2
echo    • Histórico de ajustes de semáforos
echo.
pause
goto MENU

:MENU_PRINCIPAL
cls
echo.
echo ⏳ Abrindo Menu Principal...
echo.
start "" "%BASE_DIR%MENU_INTERATIVO.html"
timeout /t 2 /nobreak >nul
echo ✓ Menu aberto com sucesso!
echo.
echo 🎯 Menu Principal oferece acesso a:
echo    • Todos os componentes do sistema
echo    • Informações detalhadas de cada módulo
echo    • Status do sistema
echo    • Links para documentação
echo.
pause
goto MENU

:ALGORITMO
cls
echo.
echo 🔄 Preparando ambiente para executar algoritmo...
echo.

if exist "%BASE_DIR%.venv\Scripts\activate.bat" (
    echo ✓ Ambiente virtual encontrado
    echo.
    echo ⏳ Ativando ambiente virtual...
    call "%BASE_DIR%.venv\Scripts\activate.bat"
    
    echo.
    echo ⏳ Executando algoritmo_otimizacao.py...
    python "%BASE_DIR%algoritmo_otimizacao.py"
    
    echo.
    echo ✓ Algoritmo executado!
) else (
    echo ✗ Ambiente virtual não encontrado!
    echo.
    echo Execute primeiro:
    echo   python -m venv .venv
    echo.
    echo Depois reabra este script.
)

echo.
pause
goto MENU

:TESTE_API
cls
echo.
echo 📡 Testando conexão com TomTom API...
echo.

if exist "%BASE_DIR%.venv\Scripts\activate.bat" (
    echo ✓ Ambiente virtual encontrado
    echo.
    echo ⏳ Ativando ambiente virtual...
    call "%BASE_DIR%.venv\Scripts\activate.bat"
    
    echo.
    echo ⏳ Executando teste...
    python "%BASE_DIR%teste_tomtom_completo.py"
    
    echo.
    echo ✓ Teste concluído!
) else (
    echo ✗ Ambiente virtual não encontrado!
)

echo.
pause
goto MENU

:DOCUMENTACAO
cls
echo.
echo 📚 Abrindo Documentação...
echo.

echo Arquivos de documentação disponíveis:
echo.
echo 1. README.md
echo 2. SUMARIO_EXECUTIVO.md
echo 3. PASSO_2_ALGORITMO.md
echo 4. PROJETO_FINAL.md
echo 5. VISUALIZACAO_COMPLETA.md
echo 6. GUIA_COMPLETO_USO.md
echo.
echo Qual arquivo deseja abrir? (1-6, ou Enter para cancelar)
set /p DOC_CHOICE=": "

if "%DOC_CHOICE%"=="1" start "" "%BASE_DIR%README.md"
if "%DOC_CHOICE%"=="2" start "" "%BASE_DIR%SUMARIO_EXECUTIVO.md"
if "%DOC_CHOICE%"=="3" start "" "%BASE_DIR%PASSO_2_ALGORITMO.md"
if "%DOC_CHOICE%"=="4" start "" "%BASE_DIR%PROJETO_FINAL.md"
if "%DOC_CHOICE%"=="5" start "" "%BASE_DIR%VISUALIZACAO_COMPLETA.md"
if "%DOC_CHOICE%"=="6" start "" "%BASE_DIR%GUIA_COMPLETO_USO.md"

timeout /t 2 /nobreak >nul
goto MENU

:VENV
cls
echo.
echo 🐍 Ativando Ambiente Virtual Python...
echo.

if exist "%BASE_DIR%.venv\Scripts\activate.bat" (
    echo ✓ Ambiente virtual encontrado
    echo.
    echo ⏳ Ativando...
    call "%BASE_DIR%.venv\Scripts\activate.bat"
    
    echo.
    echo ✓ Ambiente virtual ativado!
    echo.
    echo Você pode agora executar comandos Python:
    echo.
    echo   python algoritmo_otimizacao.py
    echo   python teste_tomtom_completo.py
    echo   python coleta_transito.py
    echo   python dashboard_transito.py
    echo.
    echo Digite 'deactivate' para sair do ambiente virtual
    echo.
    cmd /k
) else (
    echo ✗ Ambiente virtual não encontrado!
    echo.
    echo Para criar um novo ambiente virtual, execute:
    echo.
    echo   python -m venv .venv
    echo.
)

goto MENU

:GUIA
cls
echo.
echo 📖 Abrindo Guia de Uso...
echo.
start "" "%BASE_DIR%GUIA_COMPLETO_USO.md"
timeout /t 2 /nobreak >nul
goto MENU

:SAIR
cls
echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║                                                            ║
echo ║              👋 Obrigado por usar CitizenTech!              ║
echo ║                                                            ║
echo ║           🌐 Sistema em execução na AWS EC2                ║
echo ║           📊 Dados sincronizados com Snowflake              ║
echo ║                                                            ║
echo ╚════════════════════════════════════════════════════════════╝
echo.
exit /b 0
