import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import streamlit as st
import feedparser
from urllib.parse import quote

# Lista pré-definida de tickers das ações mais importantes da B3
tickers_disponiveis = [
    'PETR4.SA', 'VALE3.SA', 'ITUB4.SA', 'BBDC4.SA', 'BBAS3.SA',
    'ABEV3.SA', 'B3SA3.SA', 'PETR3.SA', 'WEGE3.SA', 'SUZB3.SA',
    'ITSA4.SA', 'JBSS3.SA', 'RENT3.SA', 'BPAC11.SA', 'HAPV3.SA',
    'GGBR4.SA', 'VIVT3.SA', 'LREN3.SA', 'RAIL3.SA', 'SANB11.SA',
    'CIEL3.SA', 'EGIE3.SA', 'ELET3.SA', 'EMBR3.SA', 'FLRY3.SA',
    'HYPE3.SA', 'IRBR3.SA', 'KLBN11.SA', 'LAME4.SA', 'MGLU3.SA',
    'MRFG3.SA', 'MRVE3.SA', 'MULT3.SA', 'NTCO3.SA', 'PCAR3.SA',
    'QUAL3.SA', 'RADL3.SA', 'SBSP3.SA', 'TIMP3.SA', 'UGPA3.SA',
    'USIM5.SA', 'VVAR3.SA', 'YDUQ3.SA', 'AZUL4.SA', 'CCRO3.SA',
    'CMIG4.SA', 'CSAN3.SA', 'CSNA3.SA', 'CYRE3.SA', 'ECOR3.SA',
    'ENBR3.SA', 'EQTL3.SA', 'EZTC3.SA', 'GFSA3.SA', 'GOAU4.SA',
    'GOLL4.SA', 'GUAR3.SA', 'HGTX3.SA', 'JHSF3.SA', 'LCAM3.SA',
    'LEVE3.SA', 'LOGG3.SA', 'MDIA3.SA', 'MOVI3.SA', 'ODPV3.SA',
    'POMO4.SA', 'POSI3.SA', 'PRIO3.SA', 'RAPT4.SA', 'SAPR11.SA',
    'SLCE3.SA', 'SMTO3.SA', 'TAEE11.SA', 'TOTS3.SA', 'TRPL4.SA',
    'VULC3.SA', 'WIZS3.SA'
]

# Dicionário de nomes das empresas
nomes_empresas = {
    'PETR4.SA': 'Petrobras',
    'VALE3.SA': 'Vale',
    'ITUB4.SA': 'Itaú Unibanco',
    'BBDC4.SA': 'Bradesco',
    'BBAS3.SA': 'Banco do Brasil',
    'ABEV3.SA': 'Ambev',
    'B3SA3.SA': 'B3',
    'PETR3.SA': 'Petrobras (ON)',
    'WEGE3.SA': 'Weg',
    'SUZB3.SA': 'Suzano',
    'ITSA4.SA': 'Itaúsa',
    'JBSS3.SA': 'JBS',
    'RENT3.SA': 'Localiza',
    'BPAC11.SA': 'BTG Pactual',
    'HAPV3.SA': 'Hapvida',
    'GGBR4.SA': 'Gerdau',
    'VIVT3.SA': 'Telefônica Brasil',
    'LREN3.SA': 'Lojas Renner',
    'RAIL3.SA': 'Rumo',
    'SANB11.SA': 'Santander Brasil',
    'CIEL3.SA': 'Cielo',
    'EGIE3.SA': 'Engie Brasil',
    'ELET3.SA': 'Eletrobras',
    'EMBR3.SA': 'Embraer',
    'FLRY3.SA': 'Fleury',
    'HYPE3.SA': 'Hypera',
    'IRBR3.SA': 'IRB Brasil',
    'KLBN11.SA': 'Klabin',
    'LAME4.SA': 'Lojas Americanas',
    'MGLU3.SA': 'Magazine Luiza',
    'MRFG3.SA': 'Marfrig',
    'MRVE3.SA': 'MRV Engenharia',
    'MULT3.SA': 'Multiplan',
    'NTCO3.SA': 'Natura',
    'PCAR3.SA': 'Pão de Açúcar',
    'QUAL3.SA': 'Qualicorp',
    'RADL3.SA': 'Raia Drogasil',
    'SBSP3.SA': 'Sabesp',
    'TIMP3.SA': 'TIM',
    'UGPA3.SA': 'Ultrapar',
    'USIM5.SA': 'Usiminas',
    'VVAR3.SA': 'Via Varejo',
    'YDUQ3.SA': 'Yduqs',
    'AZUL4.SA': 'Azul',
    'CCRO3.SA': 'CCR',
    'CMIG4.SA': 'Cemig',
    'CSAN3.SA': 'Cosan',
    'CSNA3.SA': 'Sid Nacional',
    'CYRE3.SA': 'Cyrela',
    'ECOR3.SA': 'Ecorodovias',
    'ENBR3.SA': 'EDP Brasil',
    'EQTL3.SA': 'Equatorial',
    'EZTC3.SA': 'EZTEC',
    'GFSA3.SA': 'Gafisa',
    'GOAU4.SA': 'Metalúrgica Gerdau',
    'GOLL4.SA': 'Gol',
    'GUAR3.SA': 'Guararapes',
    'HGTX3.SA': 'Cia Hering',
    'JHSF3.SA': 'JHSF',
    'LCAM3.SA': 'Locamerica',
    'LEVE3.SA': 'Metal Leve',
    'LOGG3.SA': 'Log Commercial',
    'MDIA3.SA': 'M.Dias Branco',
    'MOVI3.SA': 'Movida',
    'ODPV3.SA': 'Odontoprev',
    'POMO4.SA': 'Marcopolo',
    'POSI3.SA': 'Positivo',
    'PRIO3.SA': 'PetroRio',
    'RAPT4.SA': 'Randon',
    'SAPR11.SA': 'Sanepar',
    'SLCE3.SA': 'SLC Agrícola',
    'SMTO3.SA': 'São Martinho',
    'TAEE11.SA': 'Taesa',
    'TOTS3.SA': 'Totvs',
    'TRPL4.SA': 'Transmissão Paulista',
    'VULC3.SA': 'Vulcabras',
    'WIZS3.SA': 'Wiz Soluções',
}

# Função para calcular o rendimento
def calcular_rendimento(inicio, fim):
    return ((fim - inicio) / inicio) * 100

# Função para buscar notícias no Google News
def buscar_noticias(ticker):
    nome_empresa = nomes_empresas.get(ticker, ticker)
    query = (
        f'"{nome_empresa}" AND '
        '("ações" OR "bolsa de valores" OR "mercado financeiro" OR '
        '"investimentos" OR "dividendos" OR "lucro" OR "prejuízo" OR '
        '"relatório trimestral" OR "B3")'
    )
    query_codificada = quote(query)
    url = f'https://news.google.com/rss/search?q={query_codificada}&hl=pt-BR&gl=BR&ceid=BR:pt-419'
    feed = feedparser.parse(url)
    return feed

# Função para processar o feed RSS
def processar_feed_rss(feed):
    noticias = []
    for entry in feed.entries[:5]:  # Limita a 5 notícias
        titulo = entry.title
        link = entry.link
        noticias.append({'title': titulo, 'link': link})
    return noticias

# Configuração do Streamlit
st.title('Painel de Cotações da Bolsa')
st.write('Rendimentos das ações no dia, semana, mês e ano.')

# Permitir que o usuário selecione os tickers
tickers_selecionados = st.multiselect('Selecione as ações:', tickers_disponiveis)

# Verifica se há tickers selecionados
if tickers_selecionados:
    # Data de hoje
    hoje = datetime.datetime.now()
    um_dia_atras = hoje - datetime.timedelta(days=1)
    uma_semana_atras = hoje - datetime.timedelta(weeks=1)
    um_mes_atras = hoje - datetime.timedelta(weeks=4)
    um_ano_atras = hoje - datetime.timedelta(weeks=52)

    # DataFrame para armazenar os dados
    dados = pd.DataFrame(columns=['Ticker', 'Preço Hoje', 'Rendimento Dia', 'Rendimento Semana', 'Rendimento Mês', 'Rendimento Ano', 'Volume Médio 5 Dias', 'Média Móvel 7 Dias'])

    # Coletar dados para cada ticker selecionado
    for ticker in tickers_selecionados:
        acao = yf.Ticker(ticker)
        historico = acao.history(period="1y")

        # Verifica se o histórico está vazio
        if historico.empty:
            st.warning(f"Nenhum dado disponível para o ticker {ticker}.")
            continue  # Pula para o próximo ticker

        # Verifica se há dados suficientes para os cálculos
        if len(historico) < 22:  # Pelo menos 22 dias úteis para o cálculo mensal
            st.warning(f"Dados insuficientes para o ticker {ticker}. Necessário pelo menos 22 dias úteis.")
            continue  # Pula para o próximo ticker

        # Acessa os preços de fechamento
        try:
            preco_hoje = historico['Close'].iloc[-1]  # Corrigido para 'Close' com letra maiúscula
            preco_um_dia_atras = historico['Close'].iloc[-2]
            preco_uma_semana_atras = historico['Close'].iloc[-5]
            preco_um_mes_atras = historico['Close'].iloc[-22]
            preco_um_ano_atras = historico['Close'].iloc[0]
        except IndexError:
            st.warning(f"Dados insuficientes para o ticker {ticker}.")
            continue  # Pula para o próximo ticker

        # Calcula os rendimentos
        rendimento_dia = calcular_rendimento(preco_um_dia_atras, preco_hoje)
        rendimento_semana = calcular_rendimento(preco_uma_semana_atras, preco_hoje)
        rendimento_mes = calcular_rendimento(preco_um_mes_atras, preco_hoje)
        rendimento_ano = calcular_rendimento(preco_um_ano_atras, preco_hoje)

        # Calcular volume médio dos últimos 5 dias e média móvel de 7 dias
        volume_medio_5_dias = historico['Volume'].tail(5).mean()
        media_movel_7_dias = historico['Close'].tail(7).mean()

        # Adicionar os dados ao DataFrame usando pd.concat
        novo_dado = pd.DataFrame({
            'Ticker': [ticker],
            'Preço Hoje': [preco_hoje],
            'Rendimento Dia': [rendimento_dia],
            'Rendimento Semana': [rendimento_semana],
            'Rendimento Mês': [rendimento_mes],
            'Rendimento Ano': [rendimento_ano],
            'Volume Médio 5 Dias': [volume_medio_5_dias],
            'Média Móvel 7 Dias': [media_movel_7_dias]
        })
        dados = pd.concat([dados, novo_dado], ignore_index=True)

    # Adicionar nomes das empresas ao DataFrame
    dados['Nome da Empresa'] = dados['Ticker'].map(nomes_empresas)

    # Exibir os dados em uma tabela no Streamlit
    st.write('### Dados das Ações')
    st.dataframe(dados[['Nome da Empresa', 'Preço Hoje', 'Rendimento Dia', 'Rendimento Semana', 'Rendimento Mês', 'Rendimento Ano']])

    # Gráfico de rendimento
    st.write('### Gráfico de Rendimento')
    if not dados.empty:
        fig, ax = plt.subplots(figsize=(10, 6))
        for i, row in dados.iterrows():
            ax.plot([1, 2, 3, 4], [row['Rendimento Dia'], row['Rendimento Semana'], row['Rendimento Mês'], row['Rendimento Ano']], label=nomes_empresas[row['Ticker']])
            ax.scatter([1, 2, 3, 4], [row['Rendimento Dia'], row['Rendimento Semana'], row['Rendimento Mês'], row['Rendimento Ano']])
        ax.axhline(0, color='black', linestyle='--', linewidth=0.8)
        ax.set_xticks([1, 2, 3, 4])
        ax.set_xticklabels(['Dia', 'Semana', 'Mês', 'Ano'])
        ax.set_ylabel('Rendimento (%)')
        ax.set_title('Rendimento das Ações')
        ax.legend()
        ax.grid(True)
        st.pyplot(fig)
    else:
        st.warning("Nenhum dado disponível para exibir o gráfico de rendimento.")

    # Gráfico de barras para volume médio
    st.write('### Volume Médio de Negociação (Últimos 5 Dias)')
    if not dados.empty:
        fig2, ax2 = plt.subplots(figsize=(10, 6))
        dados.plot(kind='bar', x='Nome da Empresa', y='Volume Médio 5 Dias', ax=ax2, color='skyblue')
        ax2.set_ylabel('Volume Médio')
        ax2.set_title('Volume Médio de Negociação')
        st.pyplot(fig2)
    else:
        st.warning("Nenhum dado disponível para exibir o gráfico de volume médio.")

    # Filtro de ações com rendimento positivo no mês
    st.write('### Ações com Rendimento Positivo no Mês')
    if not dados.empty:
        filtro = dados[dados['Rendimento Mês'] > 0]
        if not filtro.empty:
            st.dataframe(filtro[['Nome da Empresa', 'Preço Hoje', 'Rendimento Dia', 'Rendimento Semana', 'Rendimento Mês', 'Rendimento Ano']])
        else:
            st.info("Nenhuma ação com rendimento positivo no mês.")
    else:
        st.warning("Nenhum dado disponível para exibir o filtro de rendimento positivo.")

    # Notícias sobre as ações
    st.write('### Notícias Recentes')
    if not dados.empty:
        ticker_selecionado = st.selectbox('Selecione uma ação para ver notícias:', tickers_selecionados)
        try:
            feed = buscar_noticias(ticker_selecionado)
            if feed.entries:
                noticias = processar_feed_rss(feed)
                if noticias:
                    for noticia in noticias:
                        st.write(f"**{noticia['title']}**")
                        st.markdown(f"[Saiba mais]({noticia['link']})", unsafe_allow_html=True)
                        st.write('---')
                else:
                    st.info("Nenhuma notícia encontrada para esta ação.")
            else:
                st.error("Não foi possível carregar as notícias.")
        except Exception as e:
            st.error(f"Ocorreu um erro ao buscar notícias: {e}")
    else:
        st.warning("Nenhum dado disponível para buscar notícias.")

    # Exportar dados para Excel
    if st.button('Exportar Dados para Excel'):
        if not dados.empty:
            output = pd.ExcelWriter('dados_bolsa.xlsx', engine='xlsxwriter')
            dados.to_excel(output, index=False, sheet_name='Dados')
            output.close()
            with open('dados_bolsa.xlsx', 'rb') as f:
                st.download_button(
                    label="Baixar Excel",
                    data=f,
                    file_name='dados_bolsa.xlsx',
                    mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                )
            st.success('Dados exportados com sucesso para "dados_bolsa.xlsx"!')
        else:
            st.warning("Nenhum dado disponível para exportar.")

else:
    st.info("Nenhuma ação selecionada. Selecione ações para visualizar os dados.")