import streamlit as st

from src.utils.auth import validar_login
from src.utils.sidebar import customizar_sidebar, titulos_pagina
from src.model.database import SessionLocal
from src.utils.components import load_css

st.set_page_config(page_title="Login", layout="centered")
load_css("assets/style.css")
customizar_sidebar()

with st.container(border=True):
    titulos_pagina("Sistema de Login", font_size="1.9em", text_color="#3064AD", icon='<i class="fas fa-lock"></i>')

    username = st.text_input("Usuário")
    password = st.text_input("Senha", type="password")

    if st.button("CONTINUAR", help="Clique para fazer login", use_container_width=True, type='primary'):
        db = SessionLocal()
        usuario = validar_login(db, nome=username, senha=password)

        if usuario:
            st.session_state.authentication_status = True
            st.session_state.usuario_logado = usuario

            st.switch_page("pages/1_dashboard.py")

        else:
            st.error("Usuário ou senha incorretos.")
