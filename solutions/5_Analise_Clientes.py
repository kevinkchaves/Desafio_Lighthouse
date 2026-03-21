'''
QUESTÃO 5 - ANÁLISE DE CLIENTES

Premissas obrigatórias:
•	Faturamento Total: Soma da coluna total por cliente.
•	Frequência: Contagem total de transações (IDs de venda) por cliente.
•	Ticket Médio: Faturamento Total / Frequência.
•	Diversidade de Categorias: Quantidade de categorias distintas que o cliente comprou.
•	Limpeza de Dados: nomes das categorias no arquivo produtos_raw.csv
•	Filtro de Elite: Apenas clientes que compraram produtos de 3 ou mais categorias distintas devem ser considerados no ranking.
•	Desempate: Em caso de empate no Ticket Médio, utilizar o id_cliente em ordem crescente.

Tarefas: 
 1 — Realizar a limpeza das categorias de produtos para evitar duplicidade por erro de grafia.
 2 — Calcular o Ticket Médio e a Diversidade de Categorias para cada id_cliente.
 3 — Filtrar os 10 clientes com o maior Ticket Médio que atendam ao critério de diversidade (3+ categorias).
 4 — Para este grupo de 10 clientes, identificar qual categoria concentra a maior quantidade total de itens comprados (sum(qtd)).
'''

#IMPORTANDO BIBLIOTECAS
import pandas as pd
import os
import re

# CONFIGURANDO PATHS
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PATH_VENDAS = os.path.join(BASE_DIR, '..', 'data', 'raw') 
PATH_PRODUTOS = os.path.join(BASE_DIR, '..', 'data', 'raw') 
PATH_CLIENTES = os.path.join(BASE_DIR, '..', 'data', 'raw')
PATH_PROCESSED = os.path.join(BASE_DIR, '..', 'data', 'processed')
PATH_PLOTS = os.path.join(BASE_DIR, '..', 'notebook', 'plots')

# CARREGANDO OS DADOS
df_vendas =   pd.read_csv(os.path.join(PATH_VENDAS, 'vendas_2023_2024.csv'))
df_produtos = pd.read_csv(os.path.join(PATH_PRODUTOS, 'produtos_raw.csv'))
df_clientes = pd.read_json(os.path.join(PATH_CLIENTES, 'clientes_crm.json'))

# LIMPEZA DAS CATEGORIAS DE PRODUTOS

# EXIBINDO AS PRIMEIRAS LINHAS E INFORMAÇÕES DOS PRODUTOS
print(df_produtos.head(3))
print(df_produtos.info())

# APONTANDO AS CATEGORIAS ÚNICAS E SUAS FREQUÊNCIAS
print(df_produtos['actual_category'].value_counts())

# FUNCAO PARA NORMALIZAR AS CATEGORIAS
def normalizar_categoria(categoria):
    '''Normaliza a categoria de produtos: retira os espaços, converte para minúsculas e categoriza com base em radicais em comum'''
    categoria = categoria.strip().lower().replace(' ', '')
    if 'el' in categoria:
        return 'eletrônicos'
    elif 'pr' in categoria:
        return 'propulsão'
    elif 'anc' in categoria or 'cor' in categoria:
        return 'ancoragem'
    return categoria

df_produtos['actual_category'] = df_produtos['actual_category'].apply(normalizar_categoria)

#CONFERINDO RESULTADOS DA NORMALIZAÇÃO
print(f"{df_produtos['actual_category'].value_counts()}\nTotal de registros: {df_produtos['actual_category'].value_counts().sum()}")

#CONVERSÃO PARA TIPO NUMÉRICO COLUNA PRICE

#ANTES DA CONVERSÃO, REQUER RETIRAR CARACTERES DE CIFRÃO
df_produtos['price'] = df_produtos['price'].astype(str).str.replace('R$', '').str.strip()
df_produtos['price'] = pd.to_numeric(df_produtos['price'], errors='coerce')

# CONFERINDO RESULTADOS DA CONVERSÃO
print(f"Tipo da coluna price: {df_produtos['price'].dtype}")
print(f"Qtd dos valores: {df_produtos['price'].value_counts().sum()}")

# REMOÇÃO DE DUPLICATAS

antes_remocao = len(df_produtos)
df_produtos = df_produtos.drop_duplicates()
depois_remocao = len(df_produtos)
print(f"Registros removidos: {antes_remocao - depois_remocao}")
print(f"Dataset: {depois_remocao} linhas normalizadas e sem duplicatas.")

# SALVANDO O DATASET NORMALIZADO
df_produtos.to_csv(os.path.join(PATH_PROCESSED, 'produtos_normalizados.csv'), index=False)


#CONFERINDO AS INFORMAÇÕES DOS CLIENTES
print(df_clientes.info())
print(df_clientes.head())

#TRATANDO AS INCONSISTÊNCIAS DE EMAIL
df_clientes['email'] = df_clientes['email'].str.replace('#', '@')

# OBSERVANDO E TRATANDO AS INCONSISTÊNCIAS EM LOCALIZAÇÃO
print(df_clientes['location'].unique())

#CRIANDO UMA FUNÇÃO PARA SEPARAR CIDADE E ESTADO UF
def tratando_localizacao(localizacao):
   '''Recebe a localização, separa por vírgula, barra ou hífen, e identifica a cidade e o estado UF.'''
   separacao = [p.strip() for p in re.split(r'[,/-]', str(localizacao))]
   uf = next((p.upper() for p in separacao if len(p) == 2), None)
   cidade = next((p for p in separacao if len(p) != 2), None)
   return pd.Series([cidade, uf])

#APLICANDO A FUNÇÃO DE TRATAMENTO DE LOCALIZAÇÃO E REMOVENDO A COLUNA ORIGINAL SUJA
df_clientes[['cidade','UF']] = df_clientes['location'].apply(tratando_localizacao)
df_clientes = df_clientes.drop(columns=['location'])
print(df_clientes[['cidade', 'UF']].head(3))

#AGREGANDO OS DADOS DE VENDAS COM OS PRODUTOS
df_vendas_produtos = pd.merge(df_vendas, df_produtos, left_on='id_product', right_on='code')
print(df_vendas_produtos.head(3))

# UNINDO O RESULTADO COM OS DADOS DE CLIENTES
df_clientes_transacoes = pd.merge(df_vendas_produtos, df_clientes, left_on='id_client', right_on='code')
print(df_clientes_transacoes.head(3))

# CALCULANDO AS MÉTRICAS POR CLIENTE
df_metricas = df_clientes_transacoes.groupby('id_client').agg(
    full_name=('full_name', 'first'),
    faturamento_total=('total', 'sum'),
    frequencia=('id', 'nunique'),
    diversidade_categorias=('actual_category', 'nunique')).reset_index()

# CALCULANDO O TICKET MÉDIO
df_metricas['ticket_medio'] = df_metricas['faturamento_total'] / df_metricas['frequencia']
print(df_metricas.head())

df_metricas.to_csv(os.path.join(PATH_PROCESSED, 'metricas_clientes.csv'), index=False)

#OBSERVANDO QUANTOS CLIENTES COMPRARAM MAIS DE 3 CATEGORIAS DIFERENTES
df_clientes_categorias = df_metricas[df_metricas['diversidade_categorias'] >= 3]
print(f"Numero de clientes que compraram pelo menos 3 categorias: {df_clientes_categorias.shape[0]}")

#SELECIONANDO OS 10 CLIENTES DE ELITE COM BASE NO TICKET MÉDIO
top_10_clientes = df_metricas.sort_values(by=['ticket_medio', 'id_client'], ascending=[False, True]).head(10)
top_10_clientes = top_10_clientes.sort_values(by='id_client', ascending=True)
print(top_10_clientes)

# IDENTIFICANDO A CATEGORIA DOMINANTE ENTRE OS CLIENTES DE ELITE
df_vendas_elite = df_clientes_transacoes[df_clientes_transacoes['id_client'].isin(top_10_clientes['id_client'])]
categoria_dominante = df_vendas_elite.groupby('actual_category')['qtd'].sum().sort_values(ascending=False)
print(categoria_dominante.head(1))

