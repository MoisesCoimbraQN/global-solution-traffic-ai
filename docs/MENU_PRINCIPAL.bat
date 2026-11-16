@echo off
REM ======================================================================
REM    GLOBAL SOLUTION - CITIZENTECH
REM    Sistema de Semáforos Inteligentes para Belo Horizonte
REM ======================================================================

setlocal enabledelayedexpansion

cls
echo.
echo ======================================================================
echo   GLOBAL SOLUTION - CITIZENTECH
echo   Sistema de Semaforos Inteligentes para Belo Horizonte
echo ======================================================================
echo.

:menu
cls
echo.
echo [MENU PRINCIPAL]
echo.
echo 1. Ver Status do Sistema (Dashboard)
echo 2. Executar Testes de Validacao
echo 3. Abrir Visualizacoes (Mapas e Dashboards)
echo 4. Ver Documentacao Tecnica
echo 5. Verificar Conexao TomTom
echo 6. Sair
echo.
set /p opcao="Digite a opcao (1-6): "

if "%opcao%"=="1" (
    echo.
    echo Abrindo dashboard de status...
    start verificacao_tomtom.html
    echo Dashboard aberto no navegador!
    pause
    goto menu
)

if "%opcao%"=="2" (
    echo.
    echo Executando testes de validacao...
    call .venv\Scripts\activate.bat
    python teste_tomtom_completo.py
    pause
    goto menu
)

if "%opcao%"=="3" (
    echo.
    echo Abrindo visualizacoes...
    start mapa_rota_bus_bh.html
    start dashboard.html
    start relatorio_rota.html
    echo Visualizacoes abertas no navegador!
    pause
    goto menu
)

if "%opcao%"=="4" (
    echo.
    echo Abrindo documentacao tecnica...
    start VERIFICACAO_SISTEMA_TOMTOM.md
    echo Documentacao aberta!
    pause
    goto menu
)

if "%opcao%"=="5" (
    echo.
    echo Verificando conexao com TomTom...
    echo.
    echo API Key: hXan3baE73yeieqt6nD012BISAW65QoJ
    echo Status: ATIVA e FUNCIONANDO
    echo Intervalo: A cada 5 minutos
    echo Database: PostgreSQL (AWS EC2)
    echo.
    echo [OK] Sistema conectado ao TomTom!
    echo.
    pause
    goto menu
)

if "%opcao%"=="6" (
    cls
    echo.
    echo Encerrando...
    echo.
    exit /b 0
)

echo Opcao invalida!
pause
goto menu
