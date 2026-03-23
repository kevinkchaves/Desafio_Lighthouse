-- QUESTÃO 05 - ANÁLISE DE CLIENTES
-- Código calculando:
-- O Ticket Médio e diversidade de categorias por cliente.
-- identificar e filtrar dos 10 clientes mais fiéis (maior Ticket Médio entre aqueles com diversidade >= 3 categorias).
-- A categoria mais vendida (em quantidade total de itens) considerando apenas o histórico desses 10 clientes.
-- obs: compatibilidade com MySQL, PostgreSQL e SQLServer

SELECT 
    v_final.categoria_normalizada,
    SUM(v_final.qtd) AS total_itens
FROM (
    SELECT 
        v.id_client,
        v.qtd,
        CASE 
            WHEN LOWER(REPLACE(p_unica.cat_bruta, ' ', '')) LIKE '%anc%' OR LOWER(p_unica.cat_bruta) LIKE '%cor%' THEN 'ancoragem'
            WHEN LOWER(REPLACE(p_unica.cat_bruta, ' ', '')) LIKE '%el%' THEN 'eletrônicos'
            WHEN LOWER(REPLACE(p_unica.cat_bruta, ' ', '')) LIKE '%pr%' THEN 'propulsão'
            ELSE p_unica.cat_bruta 
        END AS categoria_normalizada
    FROM vendas_2023_2024 v
    JOIN (
        -- AQUI ESTÁ O SEGREDO: Agrupamos por código antes do JOIN
        -- Isso garante que cada ID de produto conte apenas UMA VEZ
        SELECT code, MAX(actual_category) AS cat_bruta
        FROM produtos_raw
        GROUP BY code
    ) AS p_unica ON v.id_product = p_unica.code
) AS v_final

WHERE v_final.id_client IN (
    SELECT id_client FROM (
        SELECT 
            v2.id_client,
            (SUM(v2.total) / COUNT(DISTINCT v2.id)) AS ticket_medio
        FROM vendas_2023_2024 v2
        JOIN (
            -- Repetimos a desduplicação para o cálculo da elite ser justo
            SELECT code, MAX(actual_category) as cat_raw
            FROM produtos_raw
            GROUP BY code
        ) AS p2 ON v2.id_product = p2.code
        GROUP BY v2.id_client

        HAVING COUNT(DISTINCT 
            CASE 
                WHEN LOWER(REPLACE(p2.cat_raw, ' ', '')) LIKE '%anc%' OR LOWER(p2.cat_raw) LIKE '%cor%' THEN 'ancoragem'
                WHEN LOWER(REPLACE(p2.cat_raw, ' ', '')) LIKE '%el%' THEN 'eletrônicos'
                WHEN LOWER(REPLACE(p2.cat_raw, ' ', '')) LIKE '%pr%' THEN 'propulsão'
                ELSE p2.cat_raw 
            END
        ) >= 3
        ORDER BY ticket_medio DESC, id_client ASC
        LIMIT 10
    ) AS ranking_elite
)
GROUP BY v_final.categoria_normalizada
ORDER BY total_itens DESC;
