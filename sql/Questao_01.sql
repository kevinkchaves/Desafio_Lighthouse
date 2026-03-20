-- QUESTÃO 01 - EDA
-- Consultar métricas gerais do arquivo vendas_2023_2024: quantidade total de linhas, colunas, data mínima, data máxima, valor mínimo, valor máximo e valor médio da coluna total.
-- obs: para totaol de colunas,  "INFORMATION_SCHEMA.COLUMNS" é um recurso compatível com MySQL, PostgreSQL e SQLServer. A sintaxe pode variar dependendo do sistema que está usando. 

SELECT     
COUNT(*) AS qtd_total_linhas,
(SELECT COUNT(*) 
FROM INFORMATION_SCHEMA.COLUMNS 
WHERE(TABLE_NAME) = 'vendas_2023_2024') AS qtd_total_colunas,
MIN(sale_date) AS data_minima,
MAX(sale_date) AS data_maxima,
MIN(total) AS valor_minimo,
MAX(total) AS valor_maximo,
AVG(total) AS valor_medio
FROM vendas_2023_2024;
