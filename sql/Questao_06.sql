-- QUESTÃO 06 - DIMENSÃO DE CALENDÁRIO 
-- Código com:
-- Desenvolvimento de um calendário traduzido para português;
-- LEFT JOIN entre o calendário e a tabela de vendas;
-- agregar vendas por dia (soma de valor_venda);
-- substituição de valores nulos por zero para dias sem vendas;
-- obs: compatível com Postgresql

WITH vendas_tratadas AS (
    SELECT 
        CASE 
            -- Tratando data que inicia com 4 digiyos (ano) 
            WHEN sale_date ~ '^\d{4}' THEN TO_DATE(sale_date, 'YYYY-MM-DD')
            -- Tratando data que inicia com 1 ou 2 dígitos
            WHEN sale_date ~ '^\d{1,2}-' THEN TO_DATE(sale_date, 'DD-MM-YYYY')
            ELSE TO_DATE(sale_date, 'DD-MM-YYYY')
        END AS data,
        total
    FROM vendas_2023_2024
    WHERE sale_date IS NOT NULL AND sale_date <> ''
),

limites AS (
    SELECT 
        MIN(data) AS data_inicio,
        MAX(data) AS data_fim
    FROM vendas_tratadas
),

dim_calendario AS (
    SELECT 
        generate_series(data_inicio, data_fim, interval '1 day')::date AS data
    FROM limites
),

dim_calendario_pt AS (
    SELECT 
        data,
        CASE EXTRACT(DOW FROM data)
            WHEN 0 THEN 'Domingo'
            WHEN 1 THEN 'Segunda-feira'
            WHEN 2 THEN 'Terça-feira'
            WHEN 3 THEN 'Quarta-feira'
            WHEN 4 THEN 'Quinta-feira'
            WHEN 5 THEN 'Sexta-feira'
            WHEN 6 THEN 'Sábado'
        END AS dia_semana,
        EXTRACT(DOW FROM data) AS cod_dia
    FROM dim_calendario
),

vendas_por_dia AS (
    SELECT 
        data,
        SUM(total) AS total_dia
    FROM vendas_tratadas
    GROUP BY data
),

base_final AS (
    SELECT 
        c.data,
        c.dia_semana,
        c.cod_dia,
        COALESCE(v.total_dia, 0) AS faturamento_final
    FROM dim_calendario_pt c
    LEFT JOIN vendas_por_dia v ON c.data = v.data
)

SELECT 
    dia_semana,
    ROUND(AVG(faturamento_final)::numeric, 2) AS media_vendas
FROM base_final
GROUP BY dia_semana, cod_dia
ORDER BY media_vendas ASC;