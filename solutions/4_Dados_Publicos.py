'''
QUESTÃO 4 - DADOS PÚBLICOS

Premissas obrigatórias:
•   O custo em USD é unitário
•	O custo em BRL deve ser calculado usando o câmbio da data da venda
•	A taxa de câmbio deve ser considerada a média da cotação de venda do dia (Banco Central)
•	A receita total do produto considera todas as vendas (inclusive as sem prejuízo)
•	Ignorar impostos e frete

Tarefas: 
 1 — Cálculo e modelagem:
•	Calcular o custo total em BRL por transação
•	Identificar transações com prejuízo
•	Agregar os dados por id_produto, gerando:
    a.	Receita total (BRL)
    b.	Prejuízo total (BRL)
    c.	Percentual de perda (prejuízo_total / receita_total)

 2 — Análise visual:
Gerar gráfico representandoo prejuízo total por produto, considerando apenas produtos que tiveram prejuízo.

 3 — Análise objetiva:
•	Qual produto concentra o maior prejuízo absoluto?
•	O produto com maior prejuízo absoluto também é o que possui a maior porcentagem de perda? 
'''

#IMPORTANDO BIBLIOTECAS
import pandas as pd
import os
import requests
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
from matplotlib.ticker import FuncFormatter

# CONFIGURANDO PATHS
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PATH_RAW = os.path.join(BASE_DIR, '..', 'data', 'raw')
PATH_PROCESSED = os.path.join(BASE_DIR, '..', 'data', 'processed')
PATH_PLOTS = os.path.join(BASE_DIR, '..', 'notebook', 'plots')

# --------- PARTE 1: EXTRAINDO COTAÇÕES DO DÓLAR ---------

#API do BACEN para obter as cotações do dólar entre 30 de dezembro de 2022 e 31 dezembro de 2024
url = "https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/CotacaoDolarPeriodo(dataInicial=@dataInicial,dataFinalCotacao=@dataFinalCotacao)?@dataInicial='12-30-2022'&@dataFinalCotacao='12-31-2024'&$format=json" 

# REQUISITANDO API E CONVERTENDO EM DATAFRAME
response = requests.get(url)
data = response.json()
df_cambio = pd.DataFrame(data['value'])

# CONVERTENDO A COLUNA DE DATA PARA O FORMATO CORRETO E EXTRAINDO APENAS A DATA
df_cambio['dataHoraCotacao'] = pd.to_datetime(df_cambio['dataHoraCotacao'])
df_cambio['data'] = df_cambio['dataHoraCotacao'].dt.date

#RENOMEANDO AS COLUNAS PARA FICAR MAIS CLARO
df_cambio = df_cambio.rename(columns={'cotacaoVenda': 'cotacao_vendas'})
df_cambio = df_cambio.rename(columns={'data': 'cotacao_data'})

# MÉDIA DIÁRIA DA COTAÇÃO DE VENDA DO DÓLAR
df_cambio = df_cambio.groupby('cotacao_data')['cotacao_vendas'].mean().reset_index()
print(df_cambio.head(10))

# SALVANDO O DATAFRAME DE COTAÇÃO EM CSV
df_cambio.to_csv(os.path.join(PATH_PROCESSED, 'cambio.csv'), index=False)

# --------- PARTE 2: EXTRAINDO COTAÇÕES DO DÓLAR ---------

# CARREGANDO OS DADOS DE VENDAS, CUSTOS DE IMPORTAÇÃO E COTAÇÃO DO DÓLAR
df_vendas = pd.read_csv(os.path.join(PATH_RAW, 'vendas_2023_2024.csv'))             
df_custos = pd.read_csv(os.path.join(PATH_PROCESSED, 'custos_importacao.csv'))
df_cambio = pd.read_csv(os.path.join(PATH_PROCESSED, 'cambio.csv')) 

#FORMATANDO A COLUNA sale_date PARA O FORMATO DE DATA, CONSIDERANDO OS DIFERENTES FORMATOS ENCONTRADOS
def format_saledata(valor):
    if not isinstance(valor, str): return valor
    if valor[4] == '-': 
        return pd.to_datetime(valor, format='%Y-%m-%d')
    else:
        return pd.to_datetime(valor, format='%d-%m-%Y')

#PADRONIZANDO O FORMATO DAS DATAS
df_vendas['sale_date'] = df_vendas['sale_date'].apply(format_saledata)
df_custos['start_date'] = pd.to_datetime(df_custos['start_date'],format='mixed',dayfirst=True)
df_cambio['cotacao_data'] = pd.to_datetime(df_cambio['cotacao_data'],format='mixed',dayfirst=True)

# ORDENANDO OS DATAFRAMES PELAS DATAS
df_vendas = df_vendas.sort_values('sale_date')
df_custos = df_custos.sort_values('start_date')
df_cambio = df_cambio.sort_values('cotacao_data')

# PADRONIZANDO O NOME DA COLUNA DE ID DO PRODUTO 
df_custos = df_custos.rename(columns={'product_id': 'id_product'})

# ASSOCIANDO A COTAÇÃO DE CÂMBIO MAIS PRÓXIMA 
df_vendas_cambio = pd.merge_asof(df_vendas.sort_values('sale_date'), df_cambio.sort_values('cotacao_data'), 
    left_on='sale_date', 
    right_on='cotacao_data', 
    direction='backward')

# ASSOCIANDO O CUSTO MAIS PRÓXIMO (ANTERIOR OU IGUAL) A DATA DE VENDA, CONSIDERANDO O ID DO PRODUTO
df_vendas_cambio_custos = pd.merge_asof(df_vendas_cambio.sort_values('sale_date'), df_custos.sort_values('start_date'), 
    left_on='sale_date', 
    right_on='start_date', 
    by='id_product', 
    direction='backward')

#SALVANDO O DATAFRAME FINAL COM AS INFORMAÇÕES DE VENDAS, COTAÇÃO E CUSTOS
df_vendas_cambio_custos.to_csv(os.path.join(PATH_PROCESSED, 'vendas_cambio_custos.csv'), index=False)

# CALCULO DO CUSTO TOTAL EM REAIS POR TRANSAÇÃO
df_vendas_cambio_custos['custo_reais'] = (df_vendas_cambio_custos['usd_price'] * df_vendas_cambio_custos['cotacao_vendas']) * df_vendas_cambio_custos['qtd']

# IDENTIFICANDO AS TRANSAÇÕES COM PREJUÍZO
df_vendas_cambio_custos['prejuizo'] = df_vendas_cambio_custos['total'] < df_vendas_cambio_custos['custo_reais']
print(df_vendas_cambio_custos['prejuizo'].value_counts())

# CALCULANDO O VALOR DO PREJUÍZO PARA AS TRANSAÇÕES QUE TIVERAM PREJUÍZO, CASO CONTRÁRIO CONSIDERA 0
df_vendas_cambio_custos['valor_prejuizo'] = np.where(df_vendas_cambio_custos['total'] < df_vendas_cambio_custos['custo_reais'],
    df_vendas_cambio_custos['custo_reais'] - df_vendas_cambio_custos['total'], 0)
print(df_vendas_cambio_custos[['id_product', 'sale_date', 'total', 'cotacao_vendas', 'usd_price', 'custo_reais', 'prejuizo', 'valor_prejuizo']].head(10))

# AGREGANDO OS DADOS POR ID DO PRODUTO E NOME DO PRODUTO PARA CALCULAR A RECEITA TOTAL, PREJUÍZO TOTAL E PERCENTUAL DE PERDA
df_dados_agregados = df_vendas_cambio_custos.groupby(['id_product', 'product_name']).agg({
    'total': 'sum',              
    'valor_prejuizo': 'sum'      
}).reset_index()

# RENOMEANDO AS COLUNAS PARA FICAR MAIS CLARO
df_dados_agregados.rename(columns={
    'total': 'receita_total', 
    'valor_prejuizo': 'prejuizo_total'
}, inplace=True)

# CALCULANDO O PERCENTUAL DE PERDA
df_dados_agregados['percentual_perda'] = df_dados_agregados['prejuizo_total'] / df_dados_agregados['receita_total']
print(df_dados_agregados.sort_values(by='prejuizo_total', ascending=False).head(100).reset_index(drop=True))

df_dados_agregados.to_csv(os.path.join(PATH_PROCESSED, 'dados_agregados.csv'), index=False)

# ANÁLISE VISUAL - GRÁFICO DE PREJUÍZO TOTAL POR PRODUTO 
top10_prejuizo = df_dados_agregados[df_dados_agregados['prejuizo_total'] > 0].nlargest(10, 'prejuizo_total')

plt.figure(figsize=(14, 10))
sns.set_theme(style="whitegrid")

# DEFININDO FORMATAÇÃO PARA EIXO X EM MILHÕES
def formatacao(x, pos):
    return f'R$ {x/1e6:.1f} M'

# CRUAÇÃO DO GRÁFICO DE BARRAS HORIZONTAIS 
grafico = sns.barplot( data=top10_prejuizo,
                       x='prejuizo_total',
                       y='product_name', 
                       palette='magma',
                       hue='product_name',
                       legend=False)
grafico.xaxis.set_major_formatter(FuncFormatter(formatacao))

for barra in grafico.containers:
    labels = [f'R$ {v.get_width()/1e6:.2f} M' for v in barra]
    grafico.bar_label(barra, labels=labels, padding=5, fontsize=10)

plt.title('TOP 10 PRODUTOS COM MAIOR PREJUÍZO TOTAL', fontsize=16, fontweight='bold', pad=20)
plt.xlabel('Prejuízo Acumulado em Milhões', fontsize=10)
plt.ylabel('Produto', fontsize=10)
plt.tight_layout()

# SALVANDO O GRÁFICO
plt.savefig(os.path.join(PATH_PLOTS, 'grafico_prejuizo.png'))

# INDICANDO O PRODUTO COM MAIOR PREJUÍZO ABSOLUTO
produto_maior_prejuizo = df_dados_agregados.sort_values(by='prejuizo_total', ascending=False).iloc[0]
print(f"Produto com maior prejuízo absoluto: {produto_maior_prejuizo['product_name']} (ID: {produto_maior_prejuizo['id_product']})\nPrejuízo de R$ {produto_maior_prejuizo['prejuizo_total']/1e6:.2f} milhoes")
      
# INDICANDO O PRODUTO COM MAIOR PERCENTUAL DE PERDA
produto_maior_percentual_perda = df_dados_agregados[df_dados_agregados['percentual_perda'] > 0].sort_values(by='percentual_perda', ascending=False).iloc[0]
print(f"Produto com maior percentual de perda: {produto_maior_percentual_perda['product_name']} (ID: {produto_maior_percentual_perda['id_product']})\nPercentual de perda: {produto_maior_percentual_perda['percentual_perda']*100:.2f}%")

# VERIFICANDO SE O PRODUTO COM MAIOR PREJUÍZO ABSOLUTO É O MESMO QUE O PRODUTO COM MAIOR PERCENTUAL DE PERDA
print("É o mesmo produto com maior prejuízo e maior percentual de perda?", 
      "Sim" if produto_maior_prejuizo['id_product']==produto_maior_percentual_perda['id_product'] else "Não. Produtos diferentes")
