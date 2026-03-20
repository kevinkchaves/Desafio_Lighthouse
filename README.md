## Desafio Lighthouse: LH Nautical ⚓

Este repositório contém a solução para o desafio final de dados e IA do Programa Lighthouse da Indicium.
O projeto consiste em transformar o caos dos dados da empresa LH Nautical (varejista de peças náuticas) em uma operação data-driven. 
O desenvolvimento abrange desde a engenharia de dados e modelagem SQL até a implementação de inteligência preditiva e sistemas de recomendação.

### Tecnologias e Ferramentas
Linguagem: Python 3.10+

Processamento de Dados: Pandas, NumPy

Banco de Dados: SQL (PostgreSQL)

Ciência de Dados: Scikit-Learn (Cosine Similarity, MAE)

Consumo de API: API do Banco Central (Câmbio)

### Estrutura do Projeto
A entrega foi dividida em frentes estratégicas para cobrir toda a jornada de dados:

1_EDA: Diagnóstico de registros para validar a confiabilidade da base.

2_Produtos: Script Python para padronização de categorias (Eletrônicos, Propulsão, Ancoragem) e remoção de duplicatas.

3_Custos_Importação: Conversão de dados aninhados (JSON) para formato tabular (CSV).

4_Dados_Públicos: Análise financeira cruzando vendas (BRL) com custos (USD) via API do Banco Central para identificar prejuízos reais.

5_Análise_Clientes: Identificação da fidelidade dos clientes.

6_Dimensão_Calendário: Correção de médias de vendas através de uma estrutura de datas completa.

7_Previsão_Demanda: Modelo de baseline simples para evitar a ruptura de estoque de motores.

8_Sistema_Recomendação: Algoritmo de similaridade de cosseno para sugestão de produtos complementares.

### Principais Insights e Resultados
```text
[BREVE]
```

### Organização do Repositório

```text
DESAFIO_LIGHTHOUSE
├── data/
│   ├── raw/
│   │   ├── clientes_crm.json
│   │   ├── custos_importacao.json
│   │   ├── produtos_raw.csv
│   │   └── vendas_2023_2024.csv
│   └── processed/
├── notebooks/
│   ├── 1_EDA.ipynb
│   ├── 2_Produtos.ipynb
│   ├── 3_Custos_Importacao.ipynb
│   ├── 4_Dados_Publicos.ipynb
│   ├── 5_Analise_Clientes.ipynb
│   ├── 6_Dimensao_Calendario.ipynb
│   ├── 7_Previsao_Demanda.ipynb
│   └── 8_Sistema_Recomendacao.ipynb
├── scripts/
├── sql/
└── README.md


### Como Executar
Clone o repositório.

Instale as dependências: pip install -r requirements.txt.

Para a análise financeira, certifique-se de ter acesso à internet para o consumo da API do Banco Central.

Execute os scripts na ordem numérica das questões.

### Contato

Desenvolvido por Kevin K. Chaves
- Linkedin: www.linkedin.com/in/kevinkrchaves