import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.metrics import mean_absolute_error
from sklearn.metrics.pairwise import cosine_similarity

# Configuração da Página
st.set_page_config(
    page_title='LH NAUTICAL | Dashboard',
    page_icon='⚓',
    layout='wide',
)

#CSS TITULO E GUIAS
st.markdown("""
    <style>
    .block-container {
        padding-top: 2.5rem; 
        padding-left: 2rem; 
        padding-right: 2rem;
    }

    [data-testid="column"] {
        padding: 0px !important;
        gap: 0px !important;
    }
    
    [data-testid="column"]:nth-child(2) {
        margin-left: -15px !important; 
    }

    h1 {
        margin-top: 0px !important;
        margin-bottom: 0px !important;
        padding-bottom: 0px !important;
        font-size: 3.8rem !important;
        line-height: 1.0 !important;
        color: #003B5C !important; 
    }
    
    .title-container {
        text-align: left;
        display: flex;
        flex-direction: column;
        justify-content: center;
        height: 100%;
    }

    .extra-image-container {
        display: flex;
        justify-content: flex-end;
        align-items: flex-start;
        margin-top: -10px;
    }

    .stTabs {
        margin-top: -30px !important; 
    }
    
    [data-testid="stTabList"] {
        border-bottom: none !important;
        display: flex !important;
        justify-content: space-between !important; 
        width: 100% !important;
        gap: 0px !important;
    }

    button[data-testid="stTab"] {
        flex-grow: 1 !important; 
        text-align: center !important;
        border: none !important;
    }

    [data-baseweb="tab-highlight"] {
        background-color: #003B5C !important;
        height: 4px !important;
    }

    button[data-testid="stTab"] p {
        font-size: 1.15rem !important;
        font-weight: 600 !important;
        color: #555 !important;
    }

    button[data-testid="stTab"][aria-selected="true"] p {
        color: #003B5C !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown("""
    <style>
    [data-testid="stMetricLabel"] p {
        font-size: 1.8rem !important; 
        font-weight: 400 !important;   
        color: #555 !important;        
        margin-bottom: 5px !important;
    }

    [data-testid="stMetricValue"] {
        font-size: 4.2rem !important; 
        font-weight: 600 !important; 
        color: #003B5C !important; 
    }

    [data-testid="stMetric"] {
        padding: 15px !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown("""
    <style>
    /* Permite que o nome do produto quebre em várias linhas e não seja cortado */
    [data-testid="stMetricValue"] {
        word-break: break-word !important;
        white-space: normal !important;
        font-size: 2.2rem !important; /* Ajuste o tamanho para não ficar gigante em 2 linhas */
        line-height: 1.1 !important;
        min-height: 80px; /* Garante alinhamento com as outras colunas */
    }
    </style>
""", unsafe_allow_html=True)

# CABEÇALHO COM LOGO, TÍTULO E IMAGEM
col1, col2, col3 = st.columns([0.8, 3, 2.5])

with col1:
    st.image('streamlit/LH_logo.png', width=240) 

with col2:
    st.markdown('<div class="title-container">', unsafe_allow_html=True)
    st.title("LH NAUTICAL | DASHBOARD")
    st.markdown("""
        <p style="font-size: 1.5rem; font-weight: 700; color: #555; margin-top: 50px; line-height: 1.2;">
            <b>Análise estratégica de ativos náuticos baseada em dados.</b>
        </p>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="extra-image-container">', unsafe_allow_html=True)
    st.image('streamlit/img_navio.jpg', use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
abas = st.tabs([
    "INÍCIO", "EDA", "PRODUTOS", "CUSTOS DE IMPORTAÇÃO", 
    "DADOS PÚBLICOS", "ANÁLISE DE CLIENTES", "DIMENSÃO CALENDÁRIO",
    "PREVISÃO DE DEMANDA", "SISTEMA DE RECOMENDAÇÃO", "CONCLUSÕES"
])

# CONTEÚDO DAS ABAS

with abas[0]: # INÍCIO
    st.subheader("Visão Geral")
    st.info('Este dashboard foi desenvolvido para solucionar o "caos de dados" da **LH Nautical**, a fim de consolidar a inteligência de mercado e otimizar a tomada de decisão.')
    st.info('O painel inclui seções dedicadas aos principais desafios encarados pela empresa com seus ativos náuticos e relações com seus clientes.')

    m1, m2, m3, m4, m5 = st.columns(5)
    m1.metric("Total de Transações", "9895")
    m2.metric("Itens", "150")
    m3.metric("Clientes", "49")
    m4.metric("Categoria Dominante", "Propulsão")
    m5.metric(" Pior Dia de Vendas", "Domingo")



with abas[1]: # EDA
    df = pd.read_csv('./data/raw/vendas_2023_2024.csv')
    df['sale_date'] = pd.to_datetime(df['sale_date'], format='mixed', dayfirst=True)
    data_min = df['sale_date'].min().strftime('%d/%m/%Y')
    data_max = df['sale_date'].max().strftime('%d/%m/%Y')
    st.subheader("EDA - Análise Exploratória de Dados")

    c1, c2, c3, c4 = st.columns(4)
    
    with c1:
        st.metric("Transações Realizadas", f"{len(df)}")
    with c2:
        st.metric("Total de Colunas", len(df.columns))
    with c3:
        st.metric(f"Início das Vendas:", data_min)
    with c4:
        st.metric(f"Fim das Vendas:", data_max)

    st.markdown("---")
    
    st.markdown("### Faturamento por Transação")

    col_stats, col_graph = st.columns([1.5, 2])

    with col_stats:
        st.write("**Estatísticas Descritivas:**")
        
        stats_filtradas = df['total'].describe().loc[['mean', 'min', 'max']].to_frame().T
        stats_filtradas.columns = ['VALOR DA MÉDIA', 'VALOR MÍNIMO', 'VALOR MÁXIMO']
        
        st.markdown("""
            <style>
                [data-testid="stTable"] { font-size: 1.5rem !important; }
                [data-testid="stDataFrame"] td { font-size: 1.4rem !important; }
            </style>
        """, unsafe_allow_html=True)

        st.dataframe(stats_filtradas.style.format("R$ {:,.2f}"), 
                     use_container_width=True, 
                     hide_index=True)

        st.markdown("<br>", unsafe_allow_html=True) 
        st.markdown(f"""
            <div style="background-color: #f0f2f6; padding: 20px; border-radius: 10px; border-left: 5px solid #003B5C;">
                <p style="font-size: 1.3rem; color: #003B5C; font-weight: bold; margin-bottom: 5px;">
                    📝 Observação Técnica:
                </p>
                <p style="font-size: 1.2rem; color: #444; line-height: 1.4;">
                    O valor máximo de <b>{stats_filtradas['VALOR MÁXIMO'].values[0]:,.2f}</b> indica a presença de outliers, 
                    o que eleva a média para <b>{stats_filtradas['VALOR DA MÉDIA'].values[0]:,.2f}</b>. São 1018 outliers, representando 10% dos registros.
                </p>
            </div>
        """, unsafe_allow_html=True)

    with col_graph:
        st.write("**Gráfico de Boxplot (Distribuição de Valores):**")
        fig_total = px.box(df, y="total", 
                           points="outliers", 
                           boxmode="overlay",
                           color_discrete_sequence=["#072974"])
        fig_total.update_traces(boxmean=True) 
        st.plotly_chart(fig_total, use_container_width=True)


with abas[2]: # PRODUTOS
    df_produtos = pd.read_csv('./data/processed/produtos_normalizados.csv')
    st.subheader("Produtos")
   
    total_itens_unicos = df_produtos['name'].nunique()
    
    prod_mais_caro = df_produtos.loc[df_produtos['price'].idxmax()]
    nome = prod_mais_caro['name']
    valor_mais_caro = prod_mais_caro['price']

    m1, m2, m3 = st.columns(3)
    
    m1.metric("Peças/Acessórios Únicos", f"{total_itens_unicos}")

    nome_exibicao = (nome[:50]) if len(nome) > 50 else nome
    m2.metric(
        label="Item Mais Caro:", 
        value=nome_exibicao)
    
    m3.metric("Valor do Item:", f"R$ {valor_mais_caro:,.2f}")

with abas[3]: # CUSTOS DE IMPORTAÇÃO

    df_importacao = pd.read_csv('./data/processed/custos_importacao.csv')
    st.subheader("Simulação de Custo por Lote")

    c1, c2, c3 = st.columns([2, 1, 1])
    
    with c1:
        produto_selecionado = st.selectbox(
            "Selecione o Produto para Simular:", 
            options=df_importacao['product_name'].unique())
    
    with c2:
        qtd_simulada = st.number_input("Quantidade (Itens):", min_value=1, value=1, step=1)
        
    with c3:
        dolar_input = st.number_input("Cotação do Dólar (R$):", value=5.10, step=0.01)

    detalhes = df_importacao.loc[df_importacao['product_name'] == produto_selecionado]
    
    if not detalhes.empty:
        preco_usd_unitario = detalhes['usd_price'].values[0]
        
        total_usd = preco_usd_unitario * qtd_simulada
        total_brl = total_usd * dolar_input

        st.markdown("---")

        res1, res2, res3 = st.columns(3)
        
        res1.metric("Preço Unitário (US$)", f"US$ {preco_usd_unitario:,.2f}")
        res2.metric(f"Total ({qtd_simulada} itens):", f"US$ {total_usd:,.2f}")
        res3.metric("Custo Estimado (R$)", f"R$ {total_brl:,.2f}")

        with st.expander("Ver lista completa de preços em Dólar"):
            st.dataframe(
                df_importacao[['product_name', 'category', 'usd_price']].rename(
                    columns={'product_name': 'Produto', 'category': 'Categoria', 'usd_price': 'Preço (US$)'}
                ),
                use_container_width=True,
                hide_index=True)
    else:
        st.error("Produto não encontrado.")


with abas[4]: # DADOS PÚBLICOS
    df_agregado = pd.read_csv('./data/processed/dados_agregados.csv')
    
    st.subheader("Itens com Maior Impacto Negativo")

    df_prejuizo_top = df_agregado.nlargest(10, 'prejuizo_total').sort_values('prejuizo_total', ascending=True)

    fig_prejuizo = px.bar(
        df_prejuizo_top,
        x='prejuizo_total',
        y='product_name',
        orientation='h',
        color='prejuizo_total',
        color_continuous_scale=["#03B0C7", "#EEB808"], 
        title="Top 10 Produtos por Perda Financeira")

    fig_prejuizo.update_traces(
        texttemplate='R$ %{x:,.2s}',
        textposition='inside',       
        insidetextanchor='end',      
        textfont=dict(size=14, color='white', family='Arial black'))

    fig_prejuizo.update_layout(
        xaxis_title="Prejuízo Acumulado (R$)",
        yaxis_title=None,
        showlegend=False,
        height=600,
        margin=dict(l=0, r=50, t=50, b=0)
    )
    st.plotly_chart(fig_prejuizo, use_container_width=True)

with abas[5]: # ANÁLISE DE CLIENTES

    df_metricas = pd.read_csv('./data/processed/metricas_clientes.csv')
    
    st.subheader("Top 10 Clientes (Ticket Médio) e Categoria de Elite")

    df_elite = df_metricas[df_metricas['diversidade_categorias'] >= 3].copy()
    
    top_10_elite = df_elite.sort_values(
        by=['ticket_medio', 'id_client'], 
        ascending=[False, True]).head(10)

    m1, m2, m3 = st.columns(3)
    
    with m1:
        st.metric("Clientes no Filtro de Elite", len(df_elite), help="Clientes com 3+ categorias")
    with m2:
        top_ticket = top_10_elite['ticket_medio'].max()
        st.metric("Maior Ticket Médio", f"R$ {top_ticket:,.2f}")
    with m3:
        st.metric("Categoria Dominante", "Propulsão") 

    st.markdown("---")

    # 2. GRÁFICO: RANKING TICKET MÉDIO (ELITE)
    st.markdown("#### Top 10 Clientes de Elite")
    
    fig_elite = px.bar(
        top_10_elite.sort_values('ticket_medio', ascending=True),
        x='ticket_medio',
        y='full_name',  
        orientation='h',
        color='ticket_medio',
        color_continuous_scale='Blues',
        text_auto='R$.2s')
    
    fig_elite.update_traces(
        texttemplate='R$ %{x:,.3s}', 
        textposition='inside',       
        insidetextanchor='end',      
        textfont=dict(size=14, color='white', family='Arial black'))

    fig_elite.update_layout(
        xaxis_title="Ticket Médio (R$)",
        yaxis_title=None,
        showlegend=False,
        height=500)

    st.plotly_chart(fig_elite, use_container_width=True)

with abas[6]: # DIMENSÃO CALENDÁRIO
    df_vendas = pd.read_csv('./data/processed/vendas_cambio_custos.csv')

    st.subheader(" Média de Vendas por Dia da Semana")

    df_vendas['sale_date'] = pd.to_datetime(df_vendas['sale_date']).dt.normalize()
    
    data_inicio, data_fim = df_vendas['sale_date'].min(), df_vendas['sale_date'].max()
    df_calendario = pd.DataFrame({'data_ref': pd.date_range(data_inicio, data_fim, freq='D')})

    df_vendas_diarias = df_vendas.groupby('sale_date')['total'].sum().reset_index()
    df_analise = pd.merge(df_calendario, df_vendas_diarias, left_on='data_ref', right_on='sale_date', how='left')
    df_analise['total'] = df_analise['total'].fillna(0)

    dias_pt = {
        'Monday': 'Segunda-feira', 'Tuesday': 'Terça-feira', 'Wednesday': 'Quarta-feira',
        'Thursday': 'Quinta-feira', 'Friday': 'Sexta-feira', 'Saturday': 'Sábado', 'Sunday': 'Domingo'
    }
    df_analise['dia_semana'] = df_analise['data_ref'].dt.day_name().map(dias_pt)

    ordem = ['Domingo', 'Segunda-feira', 'Terça-feira', 'Quarta-feira', 'Quinta-feira', 'Sexta-feira', 'Sábado']
    media_dia = df_analise.groupby('dia_semana')['total'].mean().reindex(ordem).reset_index()

    pior_dia = media_dia.loc[media_dia['total'].idxmin()]
    melhor_dia = media_dia.loc[media_dia['total'].idxmax()]

    m1, m2 = st.columns(2)
    m1.metric("Pior Dia", pior_dia['dia_semana'], 
              delta=f"R$ {pior_dia['total']:,.2f}", delta_color="inverse")
    m2.metric("Melhor Dia", melhor_dia['dia_semana'], 
              delta=f"R$ {melhor_dia['total']:,.2f}")

    st.markdown("---")

    st.markdown("#### Média de Faturamento por Dia da Semana")
    
    fig_media = px.bar(
        media_dia,
        x='dia_semana',
        y='total',
        color='total',
        color_continuous_scale='Spectral',  
        text_auto='R$.2s')

    fig_media.update_traces(
    texttemplate='R$ %{y:,.3s}', 
    textposition='inside',
    insidetextanchor='end',
    textfont=dict(size=14, color='white', family='Arial black'))

    fig_media.update_layout(
        xaxis_title=None,
        yaxis_title="Média (R$)",
        showlegend=False,
        height=500)

    st.plotly_chart(fig_media, use_container_width=True)

    with st.expander("Ver Dados da Dimensão Calendário"):
        st.write("Dados considerando dias com faturamento zero:")
        st.dataframe(media_dia.style.format({'total': 'R$ {:,.2f}'}), use_container_width=True)


with abas[7]: # PREVISÃO DE DEMANDA
    PRODUTO_ALVO = "Motor de Popa Yamaha Evo Dash 155HP"
    st.subheader(f"Previsão Baseline: {PRODUTO_ALVO}")

    df_merged = pd.merge(df_vendas, df_produtos, left_on='id_product', right_on='code')
    df_prod_alvo = df_merged[df_merged['name'] == PRODUTO_ALVO].copy()
    df_prod_alvo['sale_date'] = pd.to_datetime(df_prod_alvo['sale_date'], errors='coerce').dt.normalize()

    # Criando o calendário completo para não pular dias com zero vendas
    calendario = pd.DataFrame({'sale_date': pd.date_range(start='2023-01-01', end='2024-01-31', freq='D')})
    vendas_dia = df_prod_alvo.groupby('sale_date')['qtd'].sum().reset_index()
    df_final = pd.merge(calendario, vendas_dia, on='sale_date', how='left').fillna(0)

    # Cálculo da Média Móvel de 7 dias (sem olhar o futuro)
    df_final['previsao'] = df_final['qtd'].shift(1).rolling(window=7).mean().fillna(0)

    teste = df_final[(df_final['sale_date'] >= '2024-01-01') & (df_final['sale_date'] <= '2024-01-31')].copy()
    mae = mean_absolute_error(teste['qtd'], teste['previsao'])

    m1 = st.columns(1)
    m1[0].metric("MAE (Erro Médio Absoluto)", f"{mae:.4f}", help="Média de erro de unidades por dia")

    st.markdown("---")

    st.markdown("#### Comparativo: Real vs. Previsão (Jan/2024)")
    
    fig_comp = go.Figure()
    fig_comp.add_trace(go.Scatter(
        x=teste['sale_date'], y=teste['qtd'],
        name='Real', mode='lines+markers',
        line=dict(color="#0653B8", width=3),
        marker=dict(size=8)))

    fig_comp.add_trace(go.Scatter(
        x=teste['sale_date'], y=teste['previsao'],
        name='Previsão (Média Móvel 7d)', mode='lines+markers',
        line=dict(color="#03A359", width=2, dash='dash'),
        marker=dict(symbol='x', size=8)))

    fig_comp.update_layout(
        xaxis_title="Dia do Mês",
        yaxis_title="Quantidade de Motores",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        height=500,
        margin=dict(l=0, r=0, t=30, b=0))

    st.plotly_chart(fig_comp, use_container_width=True)

    st.markdown("---")
    c_res1, c_res2 = st.columns(2)
    
    with c_res1:
        st.write("**O baseline é adequado para esse produto?**")
        st.info("Não. Este produto tem a caracteristica de ter uma demanda inconstante, com baixa previsibilidade de compras.\nO modelo de média móvel funciona de modo efetivo para produtos que de fato tenham a demanda mais constante.")
    
    with c_res2:
        st.write("**Limitação desse método:**")
        st.warning("O atraso é uma limitação consideravel, pois visualiza o passado imediato da semana, e com isso, a média móvel não consegue antecipar as tendências ou picos.\nEla acaba sendo mais reativa ao que já aconteceu, deslocando a previsão no tempo e falhando em capturar a sazonalidade de produtos como este ou outras imprevisibilidaddes antes que ocorram.")

with abas[8]: # RECOMENDAÇÃO

    df_vendas_prev = pd.read_csv('./data/processed/vendas_cambio_custos.csv')
    PRODUTO = "GPS Garmin Vortex Maré Drift"

    st.subheader(f"Recomendação Inteligente")
    
    st.markdown(f"**Item de Referência:** {PRODUTO}")

    matriz_interacao = df_vendas.pivot_table(
        index='id_client', 
        columns='id_product', 
        values='total', # total aqui serve apenas como âncora para o count
        aggfunc='count', 
        fill_value=0)

    matriz_binaria = np.where(matriz_interacao > 0, 1, 0)
    dist_cosseno = cosine_similarity(matriz_binaria.T)
    
    df_similaridade = pd.DataFrame(dist_cosseno, 
                                   index=matriz_interacao.columns, 
                                   columns=matriz_interacao.columns)
    try:
        id_alvo = df_vendas_prev[df_vendas_prev['product_name'] == PRODUTO]['id_product'].values[0]
        
        # Gerando o Ranking (removendo o próprio item)
        ranking_sim = df_similaridade[id_alvo].sort_values(ascending=False).drop(id_alvo).head(5)

        # Criando DataFrame para o gráfico
        res_rec = []

        for id_p, score in ranking_sim.items():
            nome_p = df_vendas_prev[df_vendas_prev['id_product'] == id_p]['product_name'].unique()[0]
            res_rec.append({'Produto': nome_p, 'Similaridade': score})
        
        df_ranking_vis = pd.DataFrame(res_rec)

        c1, c2 = st.columns([1.5, 1])

        with c1:
            st.markdown("#### Top 5 Produtos Similares")
            fig_rec = px.bar(
                df_ranking_vis.sort_values('Similaridade', ascending=True),
                x='Similaridade',
                y='Produto',
                orientation='h',
                text_auto='.3f',
                color='Similaridade',
                color_continuous_scale='darkmint')
            
            fig_rec.update_traces(
                textposition='inside',
                insidetextanchor='end',
                textfont=dict(size=14, color='white', family='Arial black'))
            
            fig_rec.update_layout(showlegend=False, yaxis_title=None)
            st.plotly_chart(fig_rec, use_container_width=True)

        with c2:
            st.info("💡 **Estratégia Cross-Sell**")
            top_1_nome = df_ranking_vis.iloc[0]['Produto']
            st.write(f"""
            Os clientes que compram o **GPS Garmin Vortex Maré Drift** também tem uma forte tendência de levar o **{top_1_nome}**.
            
            **Recomendação:**
            * Criar um 'Kit Náutico' unindo estes itens.
            * Posicionar o {top_1_nome} como item sugerido no carrinho ao selecionar o GPS.""")

    except IndexError:
        st.error("Produto alvo não encontrado no histórico de vendas para gerar recomendação.")


    with st.expander("Detalhes do Algoritmo"):
        st.write("""O sistema é baseado no histórico de compras dos clientes, a similaridade é calculada através do cosseno do ângulo entre os vetores de compra de cada produto. 
        Quanto mais próximo de 1.000, mais idêntico é o comportamento dos consumidores em relação aos dois produtos.""")


with abas[9]: # CONCLUSÕES
    st.header("Conclusões e Recomendações Executivas")

    # Criando três colunas para os perfis centrais
    col_tech, col_biz, col_founder = st.columns(3)

    with col_tech:
        st.info("**Sr. Gabriel Santos (Tech Lead)**")
        st.markdown("""
        **Foco: Organização e Processos**
        - **Pipeline de Dados:** Aprimorar a qualidade dos dados através de validações e normalização.
        - **Métricas:** Utilizar modelos mais eficientes para previsão de demanda, reduzindo o MAE e melhorando a acurácia.
        """)

    with col_biz:
        st.success("**Sra. Marina Costa (Gerente de Negócios)**")
        st.markdown(f"""
        **Foco: Resultados e Finanças**
        - **Ajuste de Preços:** Necessidade imediata de revisão dos valores devido à volatilidade cambial, podendo utilizar o simulador implementado.
        - **Cross-Sell:** Implementar o combo sugerido no Sistema de Recomendação para aumentar o ticket médio.
        """)

    with col_founder:
        st.warning("**Sr. Almir (Fundador)**")
        st.markdown("""
        **Foco: Estratégia e Valor Patrimonial**
        - **Data-Driven:** As análises baseadas em dados irão orientar as decisões estratégicas, evitando os prejuízos e fomentando o crescimento da LH Nautical.
        - **Essência e Tradição:** O sistema prova com números o que o senhor já sabe por experiência: os clientes estão dispostos a comprar produtos de todas as categorias, pois confiam na qualidade e tradição da marca, o que é um ativo valioso a ser explorado.""")

    st.markdown("---")

with st.expander("Sobre o Projeto"):
        st.write(f"""
        Este dashboard foi desenvolvido utilizando:
       
        - **Data Analysis:** Manipulação de dados para insights.
        - **Data Science:** Média Móvel para previsão de demanda e Similaridade de Cosseno para recomendações.
        - **Arquitetura:** Estrutura em Streamlit.
        
        Códigos e dados estão organizados no repositório do GitHub: (https://github.com/kevinkchaves/Desafio_Lighthouse)
        
        Proposta: Indicium - Desafio Lighthouse - Dados & IA
        
        **Desenvolvido por:** Kevin K. Chaves - Aspirante a Data Scientist | [LinkedIn](https://www.linkedin.com/in/kevinkrchaves) 
        """)

        st.caption("Dashboard Lighthouse - LH Nautical - 2026")