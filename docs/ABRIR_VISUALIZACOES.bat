@echo off
REM Abre as visualizacoes HTML em navegador
REM Desenvolvido para Global Solution - CitizenTech

echo.
echo ============================================================================
echo  VISUALIZACOES - ROTA DE ONIBUS EM BELO HORIZONTE
echo ============================================================================
echo.

setlocal enabledelayedexpansion

REM Diretorio do script
set "DIR=%~dp0"

echo [*] Abrindo visualizacoes...
echo.

REM Abre mapa interativo
if exist "%DIR%mapa_rota_bus_bh.html" (
    echo [+] Abrindo Mapa Interativo...
    start "" "%DIR%mapa_rota_bus_bh.html"
    timeout /t 2 /nobreak > nul
) else (
    echo [-] ERRO: mapa_rota_bus_bh.html nao encontrado
)

REM Abre relatorio
if exist "%DIR%relatorio_rota.html" (
    echo [+] Abrindo Relatorio Detalhado...
    start "" "%DIR%relatorio_rota.html"
    timeout /t 2 /nobreak > nul
) else (
    echo [-] ERRO: relatorio_rota.html nao encontrado
)

REM Abre dashboard
if exist "%DIR%dashboard.html" (
    echo [+] Abrindo Dashboard com Graficos...
    start "" "%DIR%dashboard.html"
    timeout /t 2 /nobreak > nul
) else (
    echo [-] ERRO: dashboard.html nao encontrado
)

echo.
echo ============================================================================
echo VISUALIZACOES ABERTAS COM SUCESSO!
echo ============================================================================
echo.
echo [1] MAPA INTERATIVO
echo     - Clique em cada semaforo para ver detalhes
echo     - Visualize a rota completa em Belo Horizonte
echo.
echo [2] RELATORIO DETALHADO
echo     - Tabelas com metricas por semaforo
echo     - Analise de impacto
echo.
echo [3] DASHBOARD
echo     - 4 graficos interativos
echo     - Metricas agregadas
echo.
echo ============================================================================
echo Global Solution - CitizenTech
echo ============================================================================
echo.

pause
