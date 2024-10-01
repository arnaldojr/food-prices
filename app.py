import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
from datetime import datetime


# Carregando o conjunto de dados
@st.cache_data
def load_data():
    data = pd.read_csv('wfp_food_prices_afg.csv', encoding='ISO-8859-1', header=0)
    # Remover a primeira linha que contém valores inválidos
    data = data.iloc[1:].reset_index(drop=True)
    return data

data = load_data()

st.title('Análise Interativa de Preços de Alimentos')

st.write('Este aplicativo permite explorar dados históricos de preços de alimentos coletados pelo Programa Mundial de Alimentos (WFP).')

# Exibindo os primeiros registros
st.subheader('Visão Geral dos Dados')
st.dataframe(data.head())

# Convertendo a coluna de data para datetime
data['date'] = pd.to_datetime(data['date'], format='%Y-%m-%d')

# Verificando valores ausentes
st.subheader('Valores Ausentes')
st.write(data.isnull().sum())

# Tratando valores ausentes
data = data.dropna(subset=['price', 'usdprice', 'latitude', 'longitude'])


# Renomeando colunas para facilitar
data.rename(columns={
    'date': 'Date',
    'admin1': 'Admin1',
    'admin2': 'Admin2',
    'market': 'Market',
    'latitude': 'latitude',
    'longitude': 'longitude',
    'category': 'Category',
    'commodity': 'Commodity',
    'unit': 'Unit',
    'priceflag': 'PriceFlag',
    'pricetype': 'PriceType',
    'currency': 'Currency',
    'price': 'Price',
    'usdprice': 'USDPrice'
}, inplace=True)


st.sidebar.header('Filtros')



# Filtro por País (Admin1)
countries = data['Admin1'].unique()
selected_countries = st.sidebar.multiselect('Selecione o(s) País(es):', countries, default=countries[0])

# Filtro por Commodity
commodities = data['Commodity'].unique()
selected_commodities = st.sidebar.multiselect('Selecione a(s) Commodity(s):', commodities, default=commodities[0])

# Filtro por Intervalo de Datas
min_date = data['Date'].min()
max_date = data['Date'].max()
selected_dates = st.sidebar.date_input('Selecione o Intervalo de Datas:', [min_date, max_date])

# Aplicando os filtros
filtered_data = data[
    (data['Admin1'].isin(selected_countries)) &
    (data['Commodity'].isin(selected_commodities)) &
    (data['Date'] >= pd.to_datetime(selected_dates[0])) &
    (data['Date'] <= pd.to_datetime(selected_dates[1]))
]



st.subheader('Dados Filtrados')
st.write(f'Total de registros: {filtered_data.shape[0]}')
st.dataframe(filtered_data.head())

# Opção para download dos dados filtrados
def convert_df(df):
    return df.to_csv(index=False).encode('utf-8')

csv = convert_df(filtered_data)

st.download_button(
    label='📥 Baixar dados filtrados em CSV',
    data=csv,
    file_name='dados_filtrados.csv',
    mime='text/csv',
)


st.subheader('Variação de Preços ao Longo do Tempo')

if not filtered_data.empty:
    fig = px.line(filtered_data, x='Date', y='Price', color='Market', title='Preço ao Longo do Tempo')
    st.plotly_chart(fig)
else:
    st.write('Nenhum dado disponível para os filtros selecionados.')


st.subheader('Comparação de Preços entre Commodities')


# Garantindo que a coluna 'Price' contenha apenas valores numéricos
filtered_data['Price'] = pd.to_numeric(filtered_data['Price'], errors='coerce')

# Removendo valores NaN resultantes da conversão
filtered_data = filtered_data.dropna(subset=['Price'])

# Agrupando os dados
commodity_price = filtered_data.groupby(['Date', 'Commodity'])['Price'].mean().reset_index()




if not commodity_price.empty:
    fig2 = px.line(commodity_price, x='Date', y='Price', color='Commodity', title='Comparação de Preços')
    st.plotly_chart(fig2)
else:
    st.write('Nenhum dado disponível para os filtros selecionados.')



st.subheader('Mapa Interativo dos Mercados')

if not filtered_data.empty:
    # Convertendo as colunas 'latitude' e 'longitude' para numérico
    filtered_data['latitude'] = pd.to_numeric(filtered_data['latitude'], errors='coerce')
    filtered_data['longitude'] = pd.to_numeric(filtered_data['longitude'], errors='coerce')
    
    # Plotando o mapa com as colunas em minúsculas
    st.map(filtered_data[['latitude', 'longitude']])
else:
    st.write('Nenhum dado disponível para os filtros selecionados.')



# Usando o preço em USD
filtered_data['Price_USD'] = filtered_data['USDPrice']

st.subheader('Variação de Preços em USD')

if not filtered_data.empty:
    fig_usd = px.line(filtered_data, x='Date', y='Price_USD', color='Market', title='Preço em USD ao Longo do Tempo')
    st.plotly_chart(fig_usd)
else:
    st.write('Nenhum dado disponível para os filtros selecionados.')



st.subheader('Análise de Tendências com Médias Móveis')

# Calculando a média móvel de 30 dias
if not filtered_data.empty:
    filtered_data = filtered_data.sort_values('Date')
    filtered_data['Rolling_Mean'] = filtered_data['Price'].rolling(window=30).mean()

    fig_trend = px.line(filtered_data, x='Date', y='Rolling_Mean', color='Market', title='Média Móvel de 30 dias')
    st.plotly_chart(fig_trend)
else:
    st.write('Nenhum dado disponível para os filtros selecionados.')