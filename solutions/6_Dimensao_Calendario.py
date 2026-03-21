'''
QUESTÃO 6 - DIMENSÃO DE CALENDÁRIO

Premissas obrigatórias:
•	O período de análise considerando todas as datas entre a menor e a maior data_venda;
•	A loja esteve aberta em todos os dias do período;
•	Dias sem registro na tabela de vendas devem ser considerados como valor_venda = 0;
•	“Vendas diárias” correspondem à soma de valor_venda por dia;
•	A média de vendas por dia da semana deve considerar todos os dias do calendário, inclusive os dias sem venda;
•	O nome do dia da semana deve ser apresentado em português (Segunda-feira, Terça-feira, etc.).

Tarefa:
1 -	Construir uma dimensão de datas utilizando SQL
2 -	Cruzar a dimensão de datas com a tabela de vendas para análise (considerando os dias sem vendas).
'''
# IMPORTANDO BIBLIOTECAS
import pandas as pd
import os

# CONFIGURANDO PATHS
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PATH_VENDAS = os.path.join(BASE_DIR, '..', 'data', 'raw')

df_vendas = pd.read_csv(os.path.join(PATH_VENDAS, 'vendas_2023_2024.csv'))

#FORMATANDO A COLUNA sale_date PARA O FORMATO DE DATA
def format_saledata(valor):
    if not isinstance(valor, str): return valor
    if valor[4] == '-': 
        return pd.to_datetime(valor, format='%Y-%m-%d')
    else:
        return pd.to_datetime(valor, format='%d-%m-%Y')

#PADRONIZANDO O FORMATO DAS DATAS
df_vendas['sale_date'] = df_vendas['sale_date'].apply(format_saledata)
df_vendas['sale_date'] = df_vendas['sale_date'].dt.normalize()

# ESTABELECENDO O PERÍODO DE ANÁLISE
data_inicio = df_vendas['sale_date'].min()
data_fim = df_vendas['sale_date'].max()

# SEQUENCIA DE DATAS
calendario = pd.date_range(start=data_inicio, end=data_fim, freq='D')

#CRIANDO DATAFRAME DE CALENDÁRIO
df_calendario = pd.DataFrame({'data_referencia': calendario})

# CONVERTENDO A COLUNA DE STR PARA O FORMATO DATA
df_vendas['sale_date'] = pd.to_datetime(df_vendas['sale_date'], format='mixed', dayfirst=True)
df_vendas['sale_date'] = df_vendas['sale_date'].dt.normalize()

# AGRUPAR VENDAS POR DIA SOMANDO FATURAMENTO TOTAL
df_vendas_diarias = df_vendas.groupby('sale_date')['total'].sum().reset_index()

# MERGE ENTRE CALENDÁRIO E VENDAS DIÁRIAS
df_analise = pd.merge(df_calendario, df_vendas_diarias, left_on='data_referencia', right_on='sale_date', how='left')

# CONSIDERA 0 DIAS SEM VENDAS
df_analise['total'] = df_analise['total'].fillna(0)

# TRADUZINDO NOME DOS DIAS DA SEMANA
dias = {'Monday': 'Segunda-feira',
        'Tuesday': 'Terça-feira',
        'Wednesday': 'Quarta-feira',
        'Thursday': 'Quinta-feira',
        'Friday': 'Sexta-feira',
        'Saturday': 'Sábado',
        'Sunday': 'Domingo'}

df_analise['dia_semana'] = df_analise['data_referencia'].dt.day_name().map(dias)

#CALCULO DA MÉDIA DE VENDAS POR DIA DA SEMANA
media_diaria = df_analise.groupby('dia_semana')['total'].mean().reset_index()

#IDENTIFICANDO O PIOR DIA DA SEMANA
media_diaria = media_diaria.sort_values(by='total', ascending=True)
print(media_diaria)

