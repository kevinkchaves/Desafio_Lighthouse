'''
QUESTÃO 1 - EDA

Premissas obrigatórias:
•	Utilizar apenas o dataset vendas_2023_2024.csv;
•	Não fazer limpeza nem tratamento dos dados;
•	Apenas observar, agregar e descrever.

Tarefas: 
1 — Visão geral do dataset (quantidade de linhas, colunas e intervalo de datas);
2 — Análise de valores numéricos da coluna "total";  
3 — Interpretação e diagnóstico para análises futuras (outliers, qualidade dos dados e prontidão para análises).
'''

# IMPORTANDO BIBLIOTECAS
import pandas as pd 
from datetime import datetime

# CARREGANDO O DATASET
df = pd.read_csv('../data/raw/vendas_2023_2024.csv')
print(f"Linhas: {df.shape[0]} Colunas: {df.shape[1]}")

# CONFERINDO AS DATAS
df_data = df.copy()
df_data['sale_date'] = pd.to_datetime(df['sale_date'], format='mixed', dayfirst=True)
print(f"Data mínima: {df_data['sale_date'].min().strftime('%d-%m-%y')} e Data máxima: {df_data['sale_date'].max().strftime('%d-%m-%y')}")

#ANÁLISE DA COLUNA TOTAL
print(f"Valor mínimo: {df['total'].min()}")
print(f"Valor máximo: {df['total'].max()}")
print(f"Valor médio: {round(df['total'].mean(), 2)}")
print(f"Mediana: {df['total'].median()}")

#AVALIANDO OUTLIERS PELO MÉTODO INTERQUARTIL
q1 = df['total'].quantile(0.25) 
q3 = df['total'].quantile(0.75)
iqr = q3 - q1
lim_inferior = q1 - 1.5 * iqr
lim_superior = q3 + 1.5 * iqr

outliers_inferiores = df[df['total'] < lim_inferior]
outliers_superiores = df[df['total'] > lim_superior]

print(f"Q1: {q1}\nQ3: {q3}")
print(f"limite inferior: {lim_inferior}\nlimite superior: {lim_superior}")
print(f"outliers inferiores: {outliers_inferiores.shape[0]}")
print(f"outliers superiores: {outliers_superiores.shape[0]}")

# RANKING DE OUTLIERS
outliers_ranking = outliers_superiores.sort_values(by='total', ascending=False)
top_outliers = outliers_ranking[['id_product', 'total']].head(10)
print("Top 10 maiores outliers de vendas:")
print(top_outliers)

'''Os outliers significativos são os superiores com 1018 casos (cerca de 10% dos dados), que indicam valores  elevados acima dos 2 milhões, principalmente quandoo comparados às medidas de tendencia central deste dataframe. A média de 263 mil e a mediana 82 mil evidenciam a influência dos extremos de cima.\nAlém disso, só de observar o ranking dos 10 maiores outliers, percebemos mesmo produto (ID 76) aparecendo multiplas vezes entre os maiores, sendo que em quatro delas com o mesmo valor máximo de 2222973, o que pode nos indicar alguma anomalia, como talvez, registros duplicados.'''

#ANALISANDO OUTLIERS SUSPEITOS
outliers_suspeitos = df[(df['id_product'] == 76) & (df['total'] > 222900)]
print(outliers_suspeitos.head())

'''Apesar da possibilidade de comportamento anômalo, com o mesmo produto registrando o mesmo total elevado quatro vezes, podemos visualizar que não se trata de duplicatas, apenas compras do mesmo produto em mesma quantidade, realizadas por clientes diferentes em datas distintas.'''

#ANALISANDO VALORES NULOS, NEGATIVOS E DUPLICADOS
valores_nulos = df.isnull().sum()
print(f"Valores nulos: {valores_nulos}")
valores_negativos = (df.select_dtypes(include='number') < 0).sum()
print(f"Valores negativos: {valores_negativos}")
valores_duplicados = df.duplicated().sum()
print(f"Valores duplicados: {valores_duplicados}")

#ANALISANDO FORMATOS DA COLUNA sale_date
df['sale_date'].astype(str).str.replace(r'\d', 'X', regex=True).value_counts()

'''Os dados são de qualidade, não constando valores nulos, negativos ou duplicados. Entretanto, temos inconsistências no formato padrão de datas da coluna "sale_date", que apresenta dois tipos de configuração. 

Ademais, podemos considerar o dataset parcialmente apto para prosseguir nas análises, e que estará completamente pronto após solucionadas inconsistências.
'''
