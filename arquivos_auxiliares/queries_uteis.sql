-- =====================================================
-- GLOBAL SOLUTION - CITIZENTECH
-- Exemplos de Consultas SQL Úteis
-- =====================================================

-- =====================================================
-- 1. RESUMO DE TRÁFEGO EM TEMPO REAL
-- =====================================================

-- Consulta 1.1: Vias com Maior Congestionamento (últimas 24h)
SELECT 
    v.nome_via,
    r.nome_bairro,
    ROUND(AVG(f.nivel_congestionamento_score)::NUMERIC, 2) AS score_medio,
    ROUND(AVG(f.velocidade_atual)::NUMERIC, 2) AS velocidade_media,
    MAX(f.nivel_congestionamento_score) AS score_maximo,
    COUNT(*) AS total_medicoes,
    MAX(f.data_criacao) AS ultima_medicao
FROM fato_transito_tempo_real f
JOIN dim_via v ON f.id_via = v.id_via
JOIN dim_regiao r ON v.id_regiao = r.id_regiao
WHERE f.data_criacao >= NOW() - INTERVAL '24 hours'
GROUP BY v.id_via, v.nome_via, r.nome_bairro
ORDER BY score_medio DESC;

-- Consulta 1.2: Resumo Atual (View Pré-processada)
SELECT * FROM vw_transito_resumido;

-- =====================================================
-- 2. ANÁLISE DE HORÁRIOS DE PICO
-- =====================================================

-- Consulta 2.1: Congestionamento por Hora do Dia
SELECT 
    EXTRACT(HOUR FROM f.data_criacao)::INTEGER AS hora,
    TO_CHAR(EXTRACT(HOUR FROM f.data_criacao)::INTEGER || ':00', '00:00') AS horario,
    COUNT(*) AS medicoes,
    ROUND(AVG(f.nivel_congestionamento_score)::NUMERIC, 2) AS score_medio,
    ROUND(AVG(f.velocidade_atual)::NUMERIC, 2) AS velocidade_media,
    ROUND(MAX(f.nivel_congestionamento_score)::NUMERIC, 2) AS score_maximo
FROM fato_transito_tempo_real f
WHERE f.data_criacao >= NOW() - INTERVAL '7 days'
GROUP BY EXTRACT(HOUR FROM f.data_criacao)
ORDER BY hora;

-- Consulta 2.2: Comparar Dias da Semana
SELECT 
    CASE WHEN EXTRACT(DOW FROM f.data_criacao) = 0 THEN 'Domingo'
         WHEN EXTRACT(DOW FROM f.data_criacao) = 1 THEN 'Segunda'
         WHEN EXTRACT(DOW FROM f.data_criacao) = 2 THEN 'Terça'
         WHEN EXTRACT(DOW FROM f.data_criacao) = 3 THEN 'Quarta'
         WHEN EXTRACT(DOW FROM f.data_criacao) = 4 THEN 'Quinta'
         WHEN EXTRACT(DOW FROM f.data_criacao) = 5 THEN 'Sexta'
         WHEN EXTRACT(DOW FROM f.data_criacao) = 6 THEN 'Sábado'
    END AS dia_semana,
    EXTRACT(HOUR FROM f.data_criacao)::INTEGER AS hora,
    ROUND(AVG(f.nivel_congestionamento_score)::NUMERIC, 2) AS score_medio,
    COUNT(*) AS medicoes
FROM fato_transito_tempo_real f
WHERE f.data_criacao >= NOW() - INTERVAL '30 days'
GROUP BY EXTRACT(DOW FROM f.data_criacao), EXTRACT(HOUR FROM f.data_criacao)
ORDER BY dia_semana, hora;

-- =====================================================
-- 3. ANÁLISE DE SEMÁFOROS
-- =====================================================

-- Consulta 3.1: Eficácia dos Ajustes (View Pré-processada)
SELECT * FROM vw_eficacia_semaforos
ORDER BY eficacia_media DESC;

-- Consulta 3.2: Histórico de Ajustes de um Semáforo
SELECT 
    c.nome_cruzamento,
    v.nome_via,
    f.id_tempo,
    f.tempo_verde_anterior_segundos,
    f.tempo_verde_novo_segundos,
    (f.tempo_verde_novo_segundos - f.tempo_verde_anterior_segundos) AS ajuste_segundos,
    ROUND(f.eficacia_ajuste::NUMERIC, 2) AS eficacia_percentual,
    f.motivo_ajuste,
    f.data_criacao
FROM fato_ciclo_semaforo f
JOIN dim_cruzamento c ON f.id_semaforo = c.id_semaforo
JOIN dim_via v ON c.id_via_principal = v.id_via
WHERE c.id_semaforo = 1  -- Filtro: trocar ID do semáforo
ORDER BY f.data_criacao DESC
LIMIT 50;

-- Consulta 3.3: Taxa de Ajustes Realizados
SELECT 
    c.id_semaforo,
    c.nome_cruzamento,
    COUNT(*) AS total_ciclos,
    SUM(CASE WHEN f.ajuste_realizado = TRUE THEN 1 ELSE 0 END) AS ciclos_ajustados,
    ROUND(100.0 * SUM(CASE WHEN f.ajuste_realizado = TRUE THEN 1 ELSE 0 END)::NUMERIC / 
        NULLIF(COUNT(*), 0), 2) AS percentual_ajuste,
    ROUND(AVG(COALESCE(f.eficacia_ajuste, 0))::NUMERIC, 2) AS eficacia_media
FROM fato_ciclo_semaforo f
JOIN dim_cruzamento c ON f.id_semaforo = c.id_semaforo
WHERE f.data_criacao >= NOW() - INTERVAL '7 days'
GROUP BY c.id_semaforo, c.nome_cruzamento
ORDER BY eficacia_media DESC;

-- =====================================================
-- 4. DETECÇÃO DE INCIDENTES
-- =====================================================

-- Consulta 4.1: Incidentes Recentes
SELECT 
    v.nome_via,
    r.nome_bairro,
    f.tipo_incidente,
    COUNT(*) AS frequencia_24h,
    MAX(f.data_criacao) AS ultima_ocorrencia,
    ROUND(AVG(f.nivel_congestionamento_score)::NUMERIC, 2) AS score_medio_com_incidente
FROM fato_transito_tempo_real f
JOIN dim_via v ON f.id_via = v.id_via
JOIN dim_regiao r ON v.id_regiao = r.id_regiao
WHERE f.incidente_presente = TRUE
    AND f.data_criacao >= NOW() - INTERVAL '24 hours'
GROUP BY v.nome_via, r.nome_bairro, f.tipo_incidente
ORDER BY frequencia_24h DESC;

-- Consulta 4.2: Impacto de Incidentes no Trânsito
SELECT 
    v.nome_via,
    f.tipo_incidente,
    COUNT(*) AS total_ocorrencias,
    ROUND(AVG(f.nivel_congestionamento_score)::NUMERIC, 2) AS score_com_incidente,
    (SELECT ROUND(AVG(f2.nivel_congestionamento_score)::NUMERIC, 2)
     FROM fato_transito_tempo_real f2
     WHERE f2.id_via = v.id_via AND f2.incidente_presente = FALSE
     AND f2.data_criacao >= NOW() - INTERVAL '30 days') AS score_sem_incidente
FROM fato_transito_tempo_real f
JOIN dim_via v ON f.id_via = v.id_via
WHERE f.incidente_presente = TRUE
    AND f.data_criacao >= NOW() - INTERVAL '30 days'
GROUP BY v.id_via, v.nome_via, f.tipo_incidente
ORDER BY score_com_incidente DESC;

-- =====================================================
-- 5. ANÁLISE REGIONAL
-- =====================================================

-- Consulta 5.1: Congestionamento por Bairro
SELECT 
    r.nome_bairro,
    r.zona_cidade,
    COUNT(DISTINCT v.id_via) AS total_vias,
    ROUND(AVG(f.nivel_congestionamento_score)::NUMERIC, 2) AS score_bairro,
    ROUND(AVG(f.velocidade_atual)::NUMERIC, 2) AS velocidade_media,
    MAX(f.nivel_congestionamento_score) AS score_maximo
FROM fato_transito_tempo_real f
JOIN dim_via v ON f.id_via = v.id_via
JOIN dim_regiao r ON v.id_regiao = r.id_regiao
WHERE f.data_criacao >= NOW() - INTERVAL '24 hours'
GROUP BY r.id_regiao, r.nome_bairro, r.zona_cidade
ORDER BY score_bairro DESC;

-- Consulta 5.2: Ranking de Bairros
SELECT 
    RANK() OVER (ORDER BY AVG(f.nivel_congestionamento_score) DESC) AS ranking,
    r.nome_bairro,
    ROUND(AVG(f.nivel_congestionamento_score)::NUMERIC, 2) AS score_medio,
    COUNT(*) AS medicoes
FROM fato_transito_tempo_real f
JOIN dim_via v ON f.id_via = v.id_via
JOIN dim_regiao r ON v.id_regiao = r.id_regiao
WHERE f.data_criacao >= NOW() - INTERVAL '24 hours'
GROUP BY r.id_regiao, r.nome_bairro
HAVING COUNT(*) >= 10;

-- =====================================================
-- 6. MÉTRICAS DE DESEMPENHO
-- =====================================================

-- Consulta 6.1: Velocidade Média por Via
SELECT 
    v.nome_via,
    v.limite_velocidade AS limite_legal,
    ROUND(AVG(f.velocidade_atual)::NUMERIC, 2) AS velocidade_media,
    ROUND((AVG(f.velocidade_atual) / v.limite_velocidade * 100)::NUMERIC, 2) AS percentual_limite,
    ROUND(AVG(f.fator_atraso)::NUMERIC, 2) AS fator_atraso_medio
FROM fato_transito_tempo_real f
JOIN dim_via v ON f.id_via = v.id_via
WHERE f.data_criacao >= NOW() - INTERVAL '7 days'
GROUP BY v.id_via, v.nome_via, v.limite_velocidade
ORDER BY percentual_limite ASC;

-- Consulta 6.2: Piores Horários
SELECT 
    EXTRACT(HOUR FROM f.data_criacao)::INTEGER AS hora,
    v.nome_via,
    ROUND(AVG(f.nivel_congestionamento_score)::NUMERIC, 2) AS score,
    ROUND(AVG(f.velocidade_atual)::NUMERIC, 2) AS velocidade
FROM fato_transito_tempo_real f
JOIN dim_via v ON f.id_via = v.id_via
WHERE f.data_criacao >= NOW() - INTERVAL '14 days'
GROUP BY EXTRACT(HOUR FROM f.data_criacao), v.id_via, v.nome_via
HAVING AVG(f.nivel_congestionamento_score) > 50
ORDER BY score DESC;

-- =====================================================
-- 7. TENDÊNCIAS TEMPORAIS
-- =====================================================

-- Consulta 7.1: Evolução do Trânsito ao Longo do Dia
SELECT 
    DATE(f.data_criacao) AS data,
    EXTRACT(HOUR FROM f.data_criacao)::INTEGER AS hora,
    v.nome_via,
    COUNT(*) AS medicoes,
    ROUND(AVG(f.nivel_congestionamento_score)::NUMERIC, 2) AS score,
    ROUND(AVG(f.velocidade_atual)::NUMERIC, 2) AS velocidade
FROM fato_transito_tempo_real f
JOIN dim_via v ON f.id_via = v.id_via
WHERE f.data_criacao >= NOW() - INTERVAL '7 days'
GROUP BY DATE(f.data_criacao), EXTRACT(HOUR FROM f.data_criacao), v.id_via, v.nome_via
ORDER BY data DESC, hora;

-- Consulta 7.2: Séries Temporais para Gráficos
SELECT 
    DATE_TRUNC('hour', f.data_criacao) AS periodo,
    v.nome_via,
    ROUND(AVG(f.nivel_congestionamento_score)::NUMERIC, 2) AS score_medio,
    ROUND(AVG(f.velocidade_atual)::NUMERIC, 2) AS velocidade_media,
    COUNT(*) AS medicoes
FROM fato_transito_tempo_real f
JOIN dim_via v ON f.id_via = v.id_via
WHERE f.data_criacao >= NOW() - INTERVAL '48 hours'
GROUP BY DATE_TRUNC('hour', f.data_criacao), v.id_via, v.nome_via
ORDER BY periodo DESC, v.nome_via;

-- =====================================================
-- 8. CONSULTAS ADMINISTRATIVAS
-- =====================================================

-- Consulta 8.1: Status do Banco de Dados
SELECT 
    (SELECT COUNT(*) FROM fato_transito_tempo_real) AS total_medicoes,
    (SELECT COUNT(*) FROM fato_ciclo_semaforo) AS total_ciclos_semaforo,
    (SELECT COUNT(DISTINCT id_via) FROM dim_via) AS vias_monitoradas,
    (SELECT COUNT(DISTINCT id_semaforo) FROM dim_cruzamento) AS semaforos_configurados,
    (SELECT COUNT(DISTINCT id_regiao) FROM dim_regiao) AS regioes,
    (SELECT MAX(data_criacao) FROM fato_transito_tempo_real) AS ultima_coleta;

-- Consulta 8.2: Qualidade dos Dados
SELECT 
    v.nome_via,
    COUNT(*) AS total_medicoes,
    COUNT(CASE WHEN f.velocidade_atual > 0 THEN 1 END) AS medicoes_validas,
    ROUND(100.0 * COUNT(CASE WHEN f.velocidade_atual > 0 THEN 1 END) / 
        NULLIF(COUNT(*), 0), 2) AS percentual_validade,
    MIN(f.data_criacao) AS primeira_medicao,
    MAX(f.data_criacao) AS ultima_medicao
FROM fato_transito_tempo_real f
JOIN dim_via v ON f.id_via = v.id_via
GROUP BY v.id_via, v.nome_via
ORDER BY percentual_validade DESC;

-- Consulta 8.3: Espaço em Disco
SELECT 
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS tamanho
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;

-- =====================================================
-- 9. ALERTAS E MONITORAMENTO
-- =====================================================

-- Consulta 9.1: Alertar Congestionamento Crítico (score > 75)
SELECT 
    v.nome_via,
    r.nome_bairro,
    f.nivel_congestionamento_score,
    f.velocidade_atual,
    f.data_criacao
FROM fato_transito_tempo_real f
JOIN dim_via v ON f.id_via = v.id_via
JOIN dim_regiao r ON v.id_regiao = r.id_regiao
WHERE f.nivel_congestionamento_score > 75
    AND f.data_criacao >= NOW() - INTERVAL '1 hour'
ORDER BY f.nivel_congestionamento_score DESC;

-- Consulta 9.2: Vias com Atraso Extremo (fator > 2.5)
SELECT 
    v.nome_via,
    f.fator_atraso,
    f.tempo_atual_segundos,
    f.tempo_livre_segundos,
    (f.tempo_atual_segundos - f.tempo_livre_segundos) AS atraso_segundos,
    f.data_criacao
FROM fato_transito_tempo_real f
JOIN dim_via v ON f.id_via = v.id_via
WHERE f.fator_atraso > 2.5
    AND f.data_criacao >= NOW() - INTERVAL '1 hour'
ORDER BY f.fator_atraso DESC;

-- =====================================================
-- 10. ÍNDICES PARA OTIMIZAR PERFORMANCE
-- =====================================================

-- Se ainda não existem, criar índices adicionais:
-- CREATE INDEX idx_fato_atraso ON fato_transito_tempo_real(fator_atraso);
-- CREATE INDEX idx_fato_incidente ON fato_transito_tempo_real(incidente_presente);
-- CREATE INDEX idx_ciclo_ajuste ON fato_ciclo_semaforo(ajuste_realizado);

-- =====================================================
-- FIM DAS CONSULTAS
-- =====================================================
