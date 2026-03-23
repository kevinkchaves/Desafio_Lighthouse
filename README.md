
# DESAFIO LIGHTHOUSE - LH NAUTICAL ⚓

Este repositório contém o desafio final de dados e IA do Programa Lighthouse da Indicium.

O projeto busca solucionar o caos de dados que tem prejudicado a varejista náutica "LH Nautical", transformando-a em uma empresa de estratégias data-driven. O desenvolvimento abrange desde a engenharia de dados e modelagem SQL até a implementação de inteligência preditiva e sistemas de recomendação.

## Tecnologias e Ferramentas:

| | | | | | | 
| :---: | :---: | :---: | :---: | :---: | :---: |
| ![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white) | ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white) | ![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white) | ![NumPy](https://img.shields.io/badge/numpy-%23013243.svg?style=for-the-badge&logo=numpy&logoColor=white) | ![Scikit-learn](https://img.shields.io/badge/scikit--learn-%23F7931E.svg?style=for-the-badge&logo=scikit-learn&logoColor=white) | ![Jupyter](https://img.shields.io/badge/Jupyter-F37626.svg?&style=for-the-badge&logo=Jupyter&logoColor=white) 

## Visualização do Projeto:

- Dashboard: Link - **https://desafio-lighthouse-lhnautical.streamlit.app/**
- Notebook: Arquivo **Relatorio.ipynb** na pasta 'notebook'

## Estrutura dos Soluções:

A entrega foi dividida em frentes estratégicas para solucionar diversos aspectos do negócio.

**1) EDA:** Diagnóstico inicial de registros para validar a confiabilidade da base.

**2) Produtos:** Padronização de categorias, conversão de valores e remoção de duplicatas.

**3) Custos de Importação:** Conversão de dados aninhados (JSON) para formato tabular (CSV).

**4) Dados Públicos:** Identifica prejuízos de vendas em R$ com custos USD via API do BACEN.

**5) Análise de Clientes:** Cálculo do ticket médio e identificação de clientes de elite.

**6) Dimensão do Calendário:** Dimensionando média de vendas por dia da semana.

**7) Previsão de Demanda:** Modelo baseline simples para prever vendas e usar métrica MAE.

**8) Sistema de Recomendação:** Algoritmo de similaridade entre produtos apra recomendação.

## Repositório:

```text
DESAFIO_LIGHTHOUSE
├── data/
│   ├── processed/
│   │   ├── cambio.csv
│   │   ├── custos_importacao.csv
│   │   ├── dados_agregados.csv
│   │   ├── metricas_clientes.csv
│   │   ├── previsao_ID54.csv
│   │   ├── produtos_normalizados.csv
│   │   └── vendas_cambio_custos.csv
│   │
│   └── raw/
│       ├── clientes_crm.json
│       ├── custos_importacao.json
│       ├── produtos_raw.csv
│       └── vendas_2023_2024.csv
│   
├── notebook/
│   ├── plots/
│   │   ├── grafico_media_dia.png
│   │   ├── grafico_prejuizo.png
│   │   └── grafico_previsao_jan2024_ID54.png
│   │    
│   └── Relatorio.ipynb
│
├── solutions/
│   ├── 1_EDA.py
│   ├── 2_Produtos.py
│   ├── 3_Custos_Importacao.py
│   ├── 4_Dados_Publicos.py 
│   ├── 5_Analise_Clientes.py   
│   ├── 6_Dimensao_Calendario.py    
│   ├── 7_Previsao_Demanda.py   
│   └── 8_Sistema_Recomendacao.py   
│   
├── sql/
│   ├── Questao_01.sql
│   ├── Questao_04.sql
│   ├── Questao_05.sql
│   └── Questao_06.sql
│ 
├── streamlit/
│   ├── img_navio.jpg
│   ├── LH_logo.png
│   └── main.py
│
├── README.md
│   
└── requirements.txt
```
## Instruções de Execução: 

Primeiramente é fundamental ter o Python instalado no seu computador. 
Feito isso, seguem as etapas:

- clonar o repositório:
``` bash
git clone https://github.com/kevinkchaves/Desafio_Lighthouse.git
```
- criar um ambiente virtual:
``` bash
python3 -m venv <nomedoambiente>
pip install virtualenv
```
- ativar o ambiente virtual no Windows:
``` bash
<nomedoambiente>\Scripts\activate
```
- ativar o ambiente virtual no Linux:
``` bash
source <nomedoambiente>/bin/activate
```
- instalar as dependências 'requirements':
```bash
pip install -r requirements.txt
```
- Abrir a pasta notebook e rodar o arquivo "Relatorio.ipynb" e os códigos em ordem.
- A pasta "solutions" tem os códigos em python de cada questão individualmente.
- A pasta "sql" tem as queries das questões que solicitam as consultas SQL.
## Contato

Desenvolvido por Kevin K. Chaves

| | |
| :---: | :---: | 
![LinkedIn](https://img.shields.io/badge/linkedin-%230077B5.svg?style=for-the-badge&logo=linkedin&logoColor=white) | www.linkedin.com/in/kevinkrchaves