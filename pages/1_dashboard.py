import streamlit as st
from streamlit_folium import st_folium


from src.view.card import create_number_card
from src.view.mapa import criar_mapa
from src.model.bomba_model import carregar_dados
from src.utils.sidebar import padrao_importacao_pagina
from src.utils.components import load_css

st.set_page_config(page_title="Dashboard", layout="wide")

padrao_importacao_pagina()
load_css("assets/style.css")


df_bombas, gdf_limites = carregar_dados()

df_filtrado = df_bombas
gdf_limites = gdf_limites

# Métricas de Contagem
metricas = df_filtrado['tipo'].value_counts().to_dict()

col1, col2, col3, col4 = st.columns(4)
with col1:
    create_number_card(sum(metricas.values()), 'Total')

with col2:
    create_number_card(metricas.get('Bomba', 0), 'Bombas')

with col3:
    create_number_card(metricas.get('Reservatório', 0), 'Reservatórios')

with col4:
    create_number_card(metricas.get('Poço', 0), 'Poços')

filt1, filt2, filt3, filt4 = st.columns(4)

with filt1:
    municipio = st.selectbox(
        "Município",
        options=['Coruripe'],
        key="municipio"
    )

with filt2:
    area = st.selectbox(
        "Área",
        options=['Todos'] + df_filtrado['area'].unique().tolist(),
        key="area"
    )
with filt3:
    tipo_situacao = st.selectbox(
        "Situação",
        options=['Todos'] + df_filtrado['situaçao'].unique().tolist(),
        key="situacao"
    )

with filt4:
    tipo_equipamento = st.selectbox(
        "Tipo de Equipamento",
        options=['Todos'] + df_filtrado['tipo'].unique().tolist(),
        key="tipo_equipamento"
    )

# Aplicar filtros
if area != 'Todos':
    df_filtrado = df_filtrado[df_filtrado['area'] == area].copy()

if tipo_equipamento != 'Todos':
    df_filtrado = df_filtrado[df_filtrado['tipo'] == tipo_equipamento]

if tipo_situacao != 'Todos':
    df_filtrado = df_filtrado[df_filtrado['situaçao'] == tipo_situacao]

mapa = criar_mapa(df_filtrado, gdf_limites, tipo_equipamento=tipo_equipamento, raio_metros=300)
st_folium(mapa, width="100%", height=600)
