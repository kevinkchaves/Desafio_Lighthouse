'''
QUESTÃO 8 - SISTEMA DE RECOMENDAÇÃO

Identificar qual produto deve ser recomendado junto ao item “GPS Garmin Vortex Maré Drift”, 
com base na similaridade de comportamento de compra dos clientes.

Tarefas:
1. Criar matriz de interação Usuário x Produto obedecendo às regras:
     a. Linhas: id_cliente
     b. Colunas: id_produto
     c. Valor da célula:
     d. 1 se o cliente comprou ao menos uma vez o produto
     e. 0 caso contrário
     f. Ignore a quantidade comprada (presença/ ausência apenas)

2. Calcular Similaridade entre Produtos
     a.  Similaridade de Cosseno (Cosine Similarity) entre os vetores dos produtos
     b.  Similaridade deve ser calculada produto x produto, com base nos clientes que compraram cada item

3. Ranking de Produtos Similares
     a. Considerar produto “GPS Garmin Vortex Maré Drift” como item de referência
     b. Gerar ranking com os 5 produtos mais similares a ele
     c. Desconsiderar o próprio GPS no ranking
'''
# IMPORTANDO BIBLIOTECAS
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

#CARREGANDO O DATASET
df = pd.read_csv('./data/processed/vendas_cambio_custos.csv')
PRODUTO_ALVO = "GPS Garmin Vortex Maré Drift"

# MATRIZ DE INTERAÇÃO USUÁRIO X PRODUTO
matriz_interacao = df.pivot_table(index='id_client', 
                                  columns='id_product', 
                                  values='total',
                                  aggfunc='count', 
                                  fill_value=0)

# TRANSFORMANDO EM MATRIZ BINÁRIA
matriz_binaria = pd.DataFrame(np.where(matriz_interacao.values > 0, 1, 0),
                              index=matriz_interacao.index,
                              columns=matriz_interacao.columns)

#SIMILARIDADE DE COSSENO ENTRE OS PRODUTOS
matriz_produtos = matriz_binaria.T
dist_cosseno = cosine_similarity(matriz_produtos)

#CRIANDO UM DATAFRAME DE SIMILARIDADE
df_similaridade = pd.DataFrame(dist_cosseno, 
                               index=matriz_produtos.index, 
                               columns=matriz_produtos.index)

# RELACIONANDO O ID DO PRODUTO ALVO PARA O RANKING
id_alvo = df[df['product_name'] == PRODUTO_ALVO]['id_product'].values[0]

# RANKING DE PRODUTOS SIMILARES
ranking = df_similaridade[id_alvo].sort_values(ascending=False)
ranking = ranking.drop(labels=[id_alvo]) 

# PEGANDO OS 5 PRODUTOS MAIS SIMILARES
top_5 = ranking.head(5)

for id_prod, score in top_5.items():
    produto = df[df['id_product'] == id_prod]['product_name'].unique()[0]
    print(f"ID {id_prod} - PRODUTO: {produto} - SIMILARIDADE: {score:.3f}")