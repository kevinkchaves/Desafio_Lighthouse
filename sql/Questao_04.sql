-- QUESTÃO 04 - DADOS PÚBLICOS
-- Código calculando o custo em R$ (custo_usd * taxa_cambio_data); 
-- agregação por id_produto contendo:
-- receita total (soma do valor de venda em reais),
-- prejuízo total (soma apenas das perdas),
-- percentual de perda (prejuízo_total / receita_total).
-- obs: compatibilidade com MySQL, PostgreSQL e SQLServer
-- QUERY DO ARQUIVO "vendas_cambio_custos.csv"

SELECT
    id_product,
    product_name,
    ROUND(CAST(SUM(total) AS NUMERIC), 2) AS receita_total,
    
    ROUND(CAST(SUM(
        CASE 
            WHEN (usd_price * cotacao_vendas * qtd) > total 
            THEN (usd_price * cotacao_vendas * qtd) - total 
            ELSE 0 END) 
            AS NUMERIC), 2) AS prejuizo_total,

    ROUND(CAST(SUM(
      CASE WHEN (usd_price * cotacao_vendas * qtd) > total 
      THEN (usd_price * cotacao_vendas * qtd) - total 
      ELSE 0 END)/ NULLIF(SUM(total), 0) 
      AS NUMERIC),4) AS percentual_perda

FROM vendas_cambio_custos
GROUP BY id_product, product_name
ORDER BY prejuizo_total DESC;
