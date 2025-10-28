import streamlit as st
from src.utils.auth import validar_login
from src.utils.components import load_css, create_brand_header
from src.utils.sidebar import customizar_sidebar, titulos_pagina
from src.model.database import SessionLocal

# Configuração inicial
st.set_page_config(page_title="Login", layout="centered")
load_css("assets/style.css")

create_brand_header(
    title="Hidro Monitoring",
    subtitle="",
)

customizar_sidebar()

if "erro_login" not in st.session_state:
    st.session_state.erro_login = False

with st.container(border=True):
    titulos_pagina(text="Login", font_size="1.9em", text_color="#004B8D", icon='<i class="fas fa-lock"></i>')

    username = st.text_input("Usuário")
    password = st.text_input("Senha", type="password")

    if st.button("LOGIN",  use_container_width=True, type='primary'):
        db = SessionLocal()
        usuario = validar_login(db, nome=username, senha=password)

        if usuario:
            st.session_state.authentication_status = True
            st.session_state.usuario_logado = usuario
            st.session_state.erro_login = False
            st.switch_page("pages/1_dashboard.py")
        else:
            st.session_state.erro_login = True

    col_1, _ = st.columns(2)

    with col_1:
        if st.button("CADASTRE-SE", help="Criar nova conta", use_container_width=True, type='secondary'):
            st.switch_page("pages/4_criar_usuario.py")

if st.session_state.erro_login:
    st.markdown('<div class="erro-login">', unsafe_allow_html=True)
    st.error("Usuário ou senha incorretos.")
    st.markdown('</div>', unsafe_allow_html=True)
