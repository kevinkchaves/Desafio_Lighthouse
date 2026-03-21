'''
QUESTÃO 3 - CUSTOS DE IMPORTAÇÃO

Premissas obrigatórias:
•	Utilizar apenas o JSON custos_importacao.json
•	Utilizar obrigatoriamente Python 3

Tarefas: 
- Carregar o arquivo JSON e gerar um novo arquivo CSV organizando-o de acordo com a definição:
Coluna                Tipo   
product_id           integer
product_name         text
category             text
start_date           date
usd_price            float
'''

#IMPORTANDO BIBLIOTECAS
import pandas as pd
import json
import os

#CARREGANDO OS DADOS 
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PATH_RAW = os.path.join(BASE_DIR, '..', 'data', 'raw')
PATH_PROCESSED = os.path.join(BASE_DIR, '..', 'data', 'processed')

with open(os.path.join(PATH_RAW, 'custos_importacao.json'), 'r', encoding='utf-8') as arquivo_json:
    dados = json.load(arquivo_json)

# DESANINHANDO JSON PARA CRIAR O DATAFRAME
df_custos_importacao = pd.json_normalize(dados,
                                         record_path=['historic_data'],
                                         meta=['product_id', 'product_name', 'category'])

df_custos_importacao = df_custos_importacao[[
    'product_id', 'product_name', 'category', 'start_date', 'usd_price']]

# EXIBINDO AS PRIMEIRAS LINHAS, AS ÚLTIMAS LINHAS E O FORMATO DO DATAFRAME
print(df_custos_importacao.head(3))
print(df_custos_importacao.tail(3))
print(df_custos_importacao.shape)

#AVALIANDO OS TIPOS DE DADOS
print(f"Tipos de dados:\n{df_custos_importacao.dtypes}")

# CONVERTENDO TIPOS DE DADOS
df_custos_importacao['product_id'] = df_custos_importacao['product_id'].astype(
    int)  

df_custos_importacao['start_date'] = pd.to_datetime(df_custos_importacao['start_date'], 
                                                    errors='coerce', 
                                                    dayfirst=True)

df_custos_importacao['usd_price'] = pd.to_numeric(df_custos_importacao['usd_price'], 
                                                  errors='coerce')

print(f"\nTipos de dados convertidos:{df_custos_importacao.dtypes}")
print(df_custos_importacao.head(3))
print(df_custos_importacao.shape)


# SALVANDO EM CSV
df_custos_importacao.to_csv(os.path.join(PATH_PROCESSED, 'custos_importacao.csv'), index=False)