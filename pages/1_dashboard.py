import streamlit as st
from streamlit_folium import st_folium

from src.model.database import SessionLocal
from src.model.crud import listar_equipamentos_com_local
from src.view.card import create_number_card
from src.view.mapa import criar_mapa
from src.utils.sidebar import padrao_importacao_pagina
from src.utils.components import load_css

# ==================================================
# Configuração da página e CSS
# ==================================================
st.set_page_config(page_title="Dashboard", layout="wide")
load_css("assets/style.css")
padrao_importacao_pagina()

# ==================================================
# Banco de dados
# ==================================================
db = SessionLocal()
usuario = st.session_state.get("usuario_logado")

if not usuario:
    st.warning("Usuário não logado.")
    st.stop()

id_empresa = usuario.id_empresa
df_bomba = listar_equipamentos_com_local(db, id_empresa)

# ==================================================
# Cards de métricas
# ==================================================
metricas = df_bomba['tipo'].value_counts().to_dict()

col1, col2, col3, col4 = st.columns(4)
with col1:
    create_number_card(sum(metricas.values()), 'Total')
with col2:
    create_number_card(metricas.get('Bomba', 0), 'Bombas')
with col3:
    create_number_card(metricas.get('Reservatório', 0), 'Reservatórios')
with col4:
    create_number_card(metricas.get('Poço', 0), 'Poços')

# ==================================================
# Filtros
# ==================================================
filt1, filt2, filt3, filt4 = st.columns(4)

with filt1:
    municipio = st.selectbox(
        "Município", options=sorted(df_bomba['municipio'].unique().tolist()),
        key="municipio"
    )

with filt2:
    area = st.selectbox(
        "Equipamento",
        options=['Todos'] + sorted(df_bomba['nome'].unique().tolist()),
        key="area"
    )

with filt3:
    tipo_situacao = st.selectbox(
        "Situação",
        options=['Todos'] + sorted(df_bomba['situacao'].unique().tolist()),
        key="situacao"
    )

with filt4:
    tipo_equipamento = st.selectbox(
        "Tipo de Equipamento",
        options=['Todos'] + sorted(df_bomba['tipo'].unique().tolist()),
        key="tipo_equipamento"
    )

# Aplicar filtros
if area != 'Todos':
    df_bomba = df_bomba[df_bomba['area'] == area]
if tipo_equipamento != 'Todos':
    df_bomba = df_bomba[df_bomba['tipo'] == tipo_equipamento]
if tipo_situacao != 'Todos':
    df_bomba = df_bomba[df_bomba['situacao'] == tipo_situacao]

# ==================================================
# Mapa
# ==================================================

mapa = criar_mapa(df_bomba, tipo_equipamento=tipo_equipamento, raio_metros=300)
st_folium(mapa, width="100%", height=600)
