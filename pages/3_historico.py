import streamlit as st

from src.model.database import SessionLocal
from src.model import crud
from src.utils.sidebar import padrao_importacao_pagina
from src.utils.components import load_css
from src.view.card import create_number_card

# ==================================================
# Configuração da página e CSS
# ==================================================
st.set_page_config(page_title="Histórico", layout="wide")
load_css("assets/style.css")
padrao_importacao_pagina()

# ==================================================
# Banco de dados e usuário
# ==================================================
db = SessionLocal()
usuario = st.session_state.get("usuario_logado")

if not usuario:
    st.warning("Usuário não logado.")
    st.stop()

# ==================================================
# Dados gerais
# ==================================================

df_equipamentos = crud.listar_equipamentos_com_local(db, usuario.id_empresa)
total_equipamentos = len(df_equipamentos)


df_logs = crud.listar_logs_usuario(db)

equipamentos_criados_usuario = (
    df_logs[
        (df_logs["acao"] == "criar") &
        (df_logs["id_usuario"] == usuario.id)
    ]["id_equipamento"]
    .nunique()
)

# ==================================================
# Cards
# ==================================================

col1, col2 = st.columns(2)
with col1:
    create_number_card(total_equipamentos, "Total de Equipamentos")
with col2:
    create_number_card(equipamentos_criados_usuario, "Equipamentos Criados por Você")

# ==================================================
# Filtro por usuário
# ==================================================
st.markdown("### Histórico de Ações")

usuarios_disponiveis = df_logs["nome_usuario"].dropna().unique().tolist()
usuarios_disponiveis.sort()

usuario_filtrado = st.selectbox(
    "Filtrar por usuário:",
    options=["Todos"] + usuarios_disponiveis,
    index=0
)

if usuario_filtrado != "Todos":
    df_logs = df_logs[df_logs["nome_usuario"] == usuario_filtrado]

# ==================================================
# Exibição da tabela
# ==================================================
if df_logs.empty:
    st.info("Nenhum registro encontrado.")
else:
    colunas_exibir = ["nome_usuario", "acao", "nome_equipamento", "tipo", "municipio", "bairro", "data"]
    st.dataframe(df_logs[colunas_exibir], use_container_width=True)
