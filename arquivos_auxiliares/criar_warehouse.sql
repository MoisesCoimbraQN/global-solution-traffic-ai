-- =====================================================
-- DATA WAREHOUSE - GLOBAL SOLUTION (CitizenTech)
-- Modelo Snowflake para Tráfego em Tempo Real
-- =====================================================

-- Criar banco de dados (execute como superuser)
-- CREATE DATABASE global_solution_db;

-- =====================================================
-- 1. DIMENSÃO: DIM_REGIAO (Sub-dimensão ramificada)
-- =====================================================
CREATE TABLE IF NOT EXISTS dim_regiao (
    id_regiao SERIAL PRIMARY KEY,
    nome_bairro VARCHAR(100) NOT NULL,
    zona_cidade VARCHAR(100) NOT NULL,
    cidade VARCHAR(100) NOT NULL,
    estado VARCHAR(50) NOT NULL,
    cep_principal VARCHAR(10),
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ativo BOOLEAN DEFAULT TRUE
);

CREATE INDEX idx_dim_regiao_cidade ON dim_regiao(cidade);
CREATE INDEX idx_dim_regiao_bairro ON dim_regiao(nome_bairro);

-- =====================================================
-- 2. DIMENSÃO: DIM_VIA (Trecho de via monitorado)
-- =====================================================
CREATE TABLE IF NOT EXISTS dim_via (
    id_via SERIAL PRIMARY KEY,
    nome_via VARCHAR(150) NOT NULL,
    tipo_via VARCHAR(50) NOT NULL, -- 'Avenida', 'Rua', 'Rodovia', etc
    limite_velocidade NUMERIC(5, 2) NOT NULL, -- em km/h
    comprimento_metros NUMERIC(10, 2),
    id_regiao INTEGER NOT NULL,
    sentido_unica BOOLEAN DEFAULT FALSE,
    pistas INTEGER DEFAULT 2,
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ativo BOOLEAN DEFAULT TRUE,
    CONSTRAINT fk_via_regiao FOREIGN KEY (id_regiao) 
        REFERENCES dim_regiao(id_regiao) ON DELETE RESTRICT
);

CREATE INDEX idx_dim_via_regiao ON dim_via(id_regiao);
CREATE INDEX idx_dim_via_nome ON dim_via(nome_via);
CREATE INDEX idx_dim_via_tipo ON dim_via(tipo_via);

-- =====================================================
-- 3. DIMENSÃO: DIM_TEMPO (Dimensão temporal)
-- =====================================================
CREATE TABLE IF NOT EXISTS dim_tempo (
    id_tempo VARCHAR(12) PRIMARY KEY, -- Formato: YYYYMMDDHHMM
    data DATE NOT NULL,
    hora TIME NOT NULL,
    dia_semana VARCHAR(20) NOT NULL, -- 'Segunda', 'Terça', etc
    numero_dia_semana INTEGER NOT NULL, -- 1-7 (segunda a domingo)
    semana_ano INTEGER NOT NULL,
    mes INTEGER NOT NULL,
    ano INTEGER NOT NULL,
    trimestre INTEGER NOT NULL,
    periodo_pico BOOLEAN DEFAULT FALSE, -- True para horários de pico
    horario_comercial BOOLEAN DEFAULT FALSE, -- True entre 08:00 e 18:00
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_dim_tempo_data ON dim_tempo(data);
CREATE INDEX idx_dim_tempo_hora ON dim_tempo(hora);
CREATE INDEX idx_dim_tempo_pico ON dim_tempo(periodo_pico);

-- =====================================================
-- 4. DIMENSÃO: DIM_CRUZAMENTO (Localização dos semáforos)
-- =====================================================
CREATE TABLE IF NOT EXISTS dim_cruzamento (
    id_semaforo SERIAL PRIMARY KEY,
    nome_cruzamento VARCHAR(200) NOT NULL,
    latitude NUMERIC(10, 8) NOT NULL,
    longitude NUMERIC(11, 8) NOT NULL,
    id_via_principal INTEGER NOT NULL,
    id_via_secundaria INTEGER,
    quantidade_lotes_fiscais INTEGER DEFAULT 0,
    tipo_cruzamento VARCHAR(50) DEFAULT 'normal', -- 'normal', 'complexo', 'rotatoria'
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ativo BOOLEAN DEFAULT TRUE,
    CONSTRAINT fk_cruzamento_via_principal FOREIGN KEY (id_via_principal) 
        REFERENCES dim_via(id_via) ON DELETE RESTRICT,
    CONSTRAINT fk_cruzamento_via_secundaria FOREIGN KEY (id_via_secundaria) 
        REFERENCES dim_via(id_via) ON DELETE SET NULL
);

CREATE INDEX idx_dim_cruzamento_localizacao ON dim_cruzamento(latitude, longitude);
CREATE INDEX idx_dim_cruzamento_via_principal ON dim_cruzamento(id_via_principal);
CREATE INDEX idx_dim_cruzamento_via_secundaria ON dim_cruzamento(id_via_secundaria);

-- =====================================================
-- 5. TABELA FATO: FATO_TRANSITO_TEMPO_REAL
-- =====================================================
CREATE TABLE IF NOT EXISTS fato_transito_tempo_real (
    id_fato BIGSERIAL PRIMARY KEY,
    id_via INTEGER NOT NULL,
    id_tempo VARCHAR(12) NOT NULL,
    velocidade_atual NUMERIC(6, 2) NOT NULL, -- km/h
    velocidade_livre NUMERIC(6, 2) NOT NULL, -- km/h esperada sem trânsito
    tempo_atual_segundos INTEGER NOT NULL,
    tempo_livre_segundos INTEGER NOT NULL,
    fator_atraso NUMERIC(5, 2) GENERATED ALWAYS AS (
        CASE 
            WHEN tempo_livre_segundos > 0 
            THEN (tempo_atual_segundos::NUMERIC / tempo_livre_segundos)
            ELSE 1.0
        END
    ) STORED,
    nivel_congestionamento_score NUMERIC(5, 2) NOT NULL, -- 0-100
    densidade_veiculos NUMERIC(8, 2), -- veículos por km
    fluxo_veiculo_por_hora INTEGER,
    incidente_presente BOOLEAN DEFAULT FALSE,
    tipo_incidente VARCHAR(100),
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_fato_transito_via FOREIGN KEY (id_via) 
        REFERENCES dim_via(id_via) ON DELETE RESTRICT,
    CONSTRAINT fk_fato_transito_tempo FOREIGN KEY (id_tempo) 
        REFERENCES dim_tempo(id_tempo) ON DELETE RESTRICT
);

CREATE INDEX idx_fato_transito_via ON fato_transito_tempo_real(id_via);
CREATE INDEX idx_fato_transito_tempo ON fato_transito_tempo_real(id_tempo);
CREATE INDEX idx_fato_transito_score ON fato_transito_tempo_real(nivel_congestionamento_score);
CREATE INDEX idx_fato_transito_criacao ON fato_transito_tempo_real(data_criacao);
CREATE INDEX idx_fato_transito_via_tempo ON fato_transito_tempo_real(id_via, id_tempo);

-- =====================================================
-- 6. TABELA FATO: FATO_CICLO_SEMAFORO
-- =====================================================
CREATE TABLE IF NOT EXISTS fato_ciclo_semaforo (
    id_ciclo BIGSERIAL PRIMARY KEY,
    id_semaforo INTEGER NOT NULL,
    id_tempo VARCHAR(12) NOT NULL,
    tempo_verde_anterior_segundos INTEGER NOT NULL,
    tempo_verde_novo_segundos INTEGER NOT NULL,
    ajuste_realizado BOOLEAN DEFAULT FALSE,
    reducao_fila_estimada_metros NUMERIC(8, 2),
    velocidade_media_antes NUMERIC(6, 2),
    velocidade_media_depois NUMERIC(6, 2),
    motivo_ajuste VARCHAR(200),
    algoritmo_utilizado VARCHAR(50) DEFAULT 'adaptativo',
    eficacia_ajuste NUMERIC(5, 2), -- Percentual de melhoria esperada
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_ciclo_semaforo FOREIGN KEY (id_semaforo) 
        REFERENCES dim_cruzamento(id_semaforo) ON DELETE RESTRICT,
    CONSTRAINT fk_ciclo_tempo FOREIGN KEY (id_tempo) 
        REFERENCES dim_tempo(id_tempo) ON DELETE RESTRICT
);

CREATE INDEX idx_fato_ciclo_semaforo ON fato_ciclo_semaforo(id_semaforo);
CREATE INDEX idx_fato_ciclo_tempo ON fato_ciclo_semaforo(id_tempo);
CREATE INDEX idx_fato_ciclo_ajuste ON fato_ciclo_semaforo(ajuste_realizado);
CREATE INDEX idx_fato_ciclo_criacao ON fato_ciclo_semaforo(data_criacao);

-- =====================================================
-- 7. TABELA AUXILIAR: HORARIOS_PICO
-- =====================================================
CREATE TABLE IF NOT EXISTS horarios_pico (
    id_horario_pico SERIAL PRIMARY KEY,
    id_regiao INTEGER NOT NULL,
    dia_semana INTEGER NOT NULL, -- 1-7
    hora_inicio TIME NOT NULL,
    hora_fim TIME NOT NULL,
    intensidade_pico NUMERIC(5, 2) NOT NULL, -- Multiplicador de fluxo esperado
    descricao VARCHAR(200),
    CONSTRAINT fk_horario_pico_regiao FOREIGN KEY (id_regiao) 
        REFERENCES dim_regiao(id_regiao) ON DELETE CASCADE
);

CREATE INDEX idx_horarios_pico_regiao ON horarios_pico(id_regiao);
CREATE INDEX idx_horarios_pico_dia ON horarios_pico(dia_semana);

-- =====================================================
-- 8. VIEW: Visão Agregada de Tráfego por Via
-- =====================================================
CREATE OR REPLACE VIEW vw_transito_resumido AS
SELECT 
    v.id_via,
    v.nome_via,
    r.nome_bairro,
    r.cidade,
    AVG(f.velocidade_atual) AS velocidade_media,
    AVG(f.nivel_congestionamento_score) AS score_medio,
    MAX(f.nivel_congestionamento_score) AS score_maximo,
    COUNT(*) AS total_medicoes,
    MAX(f.data_criacao) AS ultima_medicao
FROM fato_transito_tempo_real f
JOIN dim_via v ON f.id_via = v.id_via
JOIN dim_regiao r ON v.id_regiao = r.id_regiao
WHERE f.data_criacao >= NOW() - INTERVAL '1 hour'
GROUP BY v.id_via, v.nome_via, r.nome_bairro, r.cidade
ORDER BY score_medio DESC;

-- =====================================================
-- 9. VIEW: Visão de Ajustes de Semáforo
-- =====================================================
CREATE OR REPLACE VIEW vw_eficacia_semaforos AS
SELECT 
    c.id_semaforo,
    c.nome_cruzamento,
    v.nome_via,
    COUNT(*) AS total_ciclos,
    SUM(CASE WHEN f.ajuste_realizado = TRUE THEN 1 ELSE 0 END) AS ciclos_ajustados,
    ROUND(100.0 * SUM(CASE WHEN f.ajuste_realizado = TRUE THEN 1 ELSE 0 END) / 
        NULLIF(COUNT(*), 0), 2) AS percentual_ajuste,
    AVG(CASE WHEN f.eficacia_ajuste IS NOT NULL THEN f.eficacia_ajuste ELSE 0 END) AS eficacia_media,
    MAX(f.data_criacao) AS ultima_atuacao
FROM fato_ciclo_semaforo f
JOIN dim_cruzamento c ON f.id_semaforo = c.id_semaforo
JOIN dim_via v ON c.id_via_principal = v.id_via
WHERE f.data_criacao >= NOW() - INTERVAL '7 days'
GROUP BY c.id_semaforo, c.nome_cruzamento, v.nome_via
ORDER BY eficacia_media DESC;

-- =====================================================
-- 10. Função para Popular dim_tempo (24 horas do dia)
-- =====================================================
CREATE OR REPLACE FUNCTION popular_dim_tempo(data_inicio DATE, data_fim DATE) 
RETURNS TABLE (mensagem TEXT) AS $$
DECLARE
    v_data DATE := data_inicio;
    v_hora INTEGER;
    v_minuto INTEGER;
    v_id_tempo VARCHAR(12);
    v_dia_semana INTEGER;
    v_nome_dia_semana VARCHAR(20);
    v_pico BOOLEAN;
BEGIN
    WHILE v_data <= data_fim LOOP
        FOR v_hora IN 0..23 LOOP
            FOR v_minuto IN 0, 15, 30, 45 LOOP
                v_id_tempo := TO_CHAR(v_data, 'YYYYMMDD') || 
                             LPAD(v_hora::TEXT, 2, '0') || 
                             LPAD(v_minuto::TEXT, 2, '0');
                
                v_dia_semana := EXTRACT(DOW FROM v_data)::INTEGER;
                v_nome_dia_semana := CASE WHEN v_dia_semana = 0 THEN 'Domingo'
                                          WHEN v_dia_semana = 1 THEN 'Segunda'
                                          WHEN v_dia_semana = 2 THEN 'Terça'
                                          WHEN v_dia_semana = 3 THEN 'Quarta'
                                          WHEN v_dia_semana = 4 THEN 'Quinta'
                                          WHEN v_dia_semana = 5 THEN 'Sexta'
                                          WHEN v_dia_semana = 6 THEN 'Sábado'
                                     END;
                
                v_pico := (v_hora BETWEEN 7 AND 9) OR (v_hora BETWEEN 17 AND 19);
                
                INSERT INTO dim_tempo 
                (id_tempo, data, hora, dia_semana, numero_dia_semana, 
                 semana_ano, mes, ano, trimestre, periodo_pico, horario_comercial)
                VALUES 
                (v_id_tempo, v_data, v_hora::TEXT || ':' || LPAD(v_minuto::TEXT, 2, '0') || ':00'::TIME,
                 v_nome_dia_semana, v_dia_semana, 
                 EXTRACT(WEEK FROM v_data)::INTEGER, 
                 EXTRACT(MONTH FROM v_data)::INTEGER,
                 EXTRACT(YEAR FROM v_data)::INTEGER,
                 CEIL(EXTRACT(MONTH FROM v_data)::INTEGER / 3)::INTEGER,
                 v_pico, v_hora BETWEEN 8 AND 18)
                ON CONFLICT DO NOTHING;
            END LOOP;
        END LOOP;
        v_data := v_data + INTERVAL '1 day';
    END LOOP;
    
    RETURN QUERY SELECT 'Dimensão de tempo populada com sucesso!'::TEXT;
END;
$$ LANGUAGE plpgsql;

-- =====================================================
-- COMENTÁRIOS DAS TABELAS (Documentação)
-- =====================================================
COMMENT ON TABLE dim_regiao IS 'Sub-dimensão ramificada que armazena informações geográficas (bairro, zona, cidade)';
COMMENT ON TABLE dim_via IS 'Dimensão que armazena informações das vias monitoradas';
COMMENT ON TABLE dim_tempo IS 'Dimensão temporal com granularidade de 15 minutos';
COMMENT ON TABLE dim_cruzamento IS 'Dimensão que armazena localizações dos semáforos';
COMMENT ON TABLE fato_transito_tempo_real IS 'Tabela fato principal com métricas de tráfego coletadas em tempo real';
COMMENT ON TABLE fato_ciclo_semaforo IS 'Tabela fato secundária com histórico de ajustes do sistema adaptativo';

-- =====================================================
-- FIM DO SCRIPT
-- =====================================================
