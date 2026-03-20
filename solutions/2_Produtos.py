'''QUESTÃO 2 - PRODUTOS
O dataset de produtos apresenta uma coluna 'actual_category' que contém categorias de produtos, mas os dados estão inconsistentes, com variações de formatação e possíveis erros de digitação. Além disso, a coluna 'price' contém valores monetários que precisam ser convertidos para um formato numérico.'''

#IMPORTANDO BIBLIOTECA
import pandas as pd

# CARREGANDO O DATASET
df = pd.read_csv('./data/raw/produtos_raw.csv')

# EXIBINDO AS PRIMEIRAS LINHAS E INFORMAÇÕES DO DATASET
print(df.head())
print(df.info())

# APONTANDO AS CATEGORIAS ÚNICAS E SUAS FREQUÊNCIAS
print(df['actual_category'].unique())
print(df['actual_category'].value_counts())

# FUNCÃO PARA NORMALIZAR AS CATEGORIAS DE PRODUTOS
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

# APLICANDO A FUNÇÃO DE NORMALIZAÇÃO NA COLUNA 'actual_category'
df['actual_category'] = df['actual_category'].apply(normalizar_categoria)

# CONFERINDO RESULTADOS DA NORMALIZAÇÃO
print(f"{df['actual_category'].value_counts()}\n Total de registros: {df['actual_category'].value_counts().sum()}")

print('-'*50)

#CONVERSÃO DA COLUNA 'price' PARA NUMÉRICO

# ANTES DA CONVERSÃO, REQUER RETIRAR CARACTERES DE CIFRÃO
df['price'] = df['price'].astype(str).str.replace('R$', '').str.strip()
df['price'] = pd.to_numeric(df['price'], errors='coerce')

#CONFERINDO RESULTADOS DA CONVERSÃO
print(f"Tipo da coluna price: {df['price'].dtype}")
print(f"Qtd dos valores: {df['price'].value_counts().sum()}")

#REMOVENDO REGISTROS DUPLICADOS
antes_remocao = len(df)
df = df.drop_duplicates()
depois_remocao = len(df)
print(f"Registros removidos: {antes_remocao - depois_remocao}")
print(f"Dataset: {depois_remocao} linhas normalizadas e sem duplicatas.")

#SALVANDO O DATASET NORMALIZADO
df.to_csv('./data/processed/produtos_normalizados.csv', index=False)