'''
QUESTÃO 7 - PREVISÃO DE DEMANDA

Premissas obrigatórias:
•	O período de treino até 31/12/2023;
•	O período de teste todo o mês de Janeiro de 2024;
•	A previsão deve ser feita em base diária;
•	Não é permitido utilizar dados futuros no treino (data leakage);
•	Considerar apenas produto: "Motor de Popa Yamaha Evo Dash 155HP"

Tarefa:
1 . Utilize o dataset vendas_2023_2024.csv
2. Construa um modelo baseline simples, utilizando: Média móvel dos últimos 7 dias de vendas (considerando apenas dados anteriores à data prevista).
3. Gere a previsão diária de vendas para Janeiro de 2024.
4. Compare as previsões com os valores reais do período de teste utilizando a métrica: MAE — Mean Absolute Error
5. Responda objetivamente:
     a. O baseline é adequado para esse produto?
     b. Cite uma limitação desse método.  
'''
# IMPORTANDO BIBLIOTECAS
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from sklearn.metrics import mean_absolute_error

# CONFIGURAÇÃO DE PATH
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PATH_VENDAS = os.path.join(BASE_DIR, '..', 'data', 'raw', 'vendas_2023_2024.csv')
PATH_PRODUTOS = os.path.join(BASE_DIR, '..', 'data', 'raw', 'produtos_raw.csv')
PATH_PROCESSED = os.path.join(BASE_DIR, '..', 'data', 'processed')
PATH_PLOTS = os.path.join(BASE_DIR, '..', 'notebook', 'plots')
PRODUTO_ALVO = "Motor de Popa Yamaha Evo Dash 155HP"

#CARREGANDO OS DATASETS
vendas = pd.read_csv(PATH_VENDAS)
produtos = pd.read_csv(PATH_PRODUTOS)

#TRATAMENTO DE DATAS
def format_saledata(valor):
    if not isinstance(valor, str): return valor
    try:
        if valor[4] == '-': return pd.to_datetime(valor, format='%Y-%m-%d')
        else: return pd.to_datetime(valor, format='%d-%m-%Y')
    except: return pd.to_datetime(valor, errors='coerce')

#MERGE ENTRE VENDAS E PRODUTOS PARA FILTRAR PELO NOME DO PRODUTO ALVO
df_merged = pd.merge(vendas, produtos, left_on='id_product', right_on='code', how='inner')
df_filtrado = df_merged[df_merged['name'] == PRODUTO_ALVO].copy()
df_filtrado['sale_date'] = df_filtrado['sale_date'].apply(format_saledata)

# CRIAÇÃO DE CALENDARIO (01/01/23 a 31/01/24)
vendas_diarias = df_filtrado.groupby('sale_date')['qtd'].sum().reset_index()
calendario = pd.DataFrame({'sale_date': pd.date_range(start='2023-01-01', end='2024-01-31', freq='D')})
df_final = pd.merge(calendario, vendas_diarias, on='sale_date', how='left').fillna(0)

#FAZENDO O BASELINE DE MÉDIA MÓVEL 7 DIAS
df_final['previsao'] = df_final['qtd'].shift(1).rolling(window=7).mean().fillna(0)

#SEPARANDO TREINO E TESTE
treino = df_final[df_final['sale_date'] <= '2023-12-31'].copy()
teste = df_final[(df_final['sale_date'] >= '2024-01-01') & (df_final['sale_date'] <= '2024-01-31')].copy()

#MÉTRICA MAE
mae = mean_absolute_error(teste['qtd'], teste['previsao'])

df_previsao = df_final.to_csv(os.path.join(PATH_PROCESSED, 'previsao_ID54.csv'), index=False)

#EXIBINDO RESULTADOS    

print(f"RESULTADOS PARA: {PRODUTO_ALVO}")

print(f"MAE: {mae:.4f}")
print(f"REAL: {teste['qtd'].sum():.2f}")
print(f"PREVISÃO: {teste['previsao'].sum():.2f}")

# GERANDO O GRÁFICO DE COMPARAÇÃO ENTRE REAL E PREVISÃO
plt.figure(figsize=(10, 6))

plt.plot(teste['sale_date'], teste['qtd'],
         label='Real',
         color="#0411caf6",
         marker='o',
         markersize=4)

plt.plot(teste['sale_date'], teste['previsao'],
         label='Previsão',
         color="#f712bd",
         linestyle='--',
         marker='x')

ax = plt.gca()
ax.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m'))

plt.xticks(rotation=45)
plt.title(
    f'PREVISÃO: {(PRODUTO_ALVO).upper()} - JAN/2024\nMAE: {mae:.4f} -  Aprox. {mae:.0f} Unidade de Erros/Dia', fontsize=14)
plt.ylabel('QUANTIDADE', fontsize=12)
plt.xlabel('')

plt.xticks(rotation=0)
plt.grid(True, linestyle=':', alpha=0.6)
plt.legend()
plt.tight_layout()

# SALVANDO O GRÁFICO
plt.savefig(os.path.join(PATH_PLOTS, 'grafico_previsao_jan2024_ID54.png'))
plt.show()
