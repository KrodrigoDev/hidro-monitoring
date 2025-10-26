import streamlit as st
from src.model.login_model import dump_login, load_config, auth
from src.utils.sidebar import customizar_sidebar
from src.utils.components import load_css

# Configuração da página
st.set_page_config(page_title="Login", page_icon="🔐", layout="centered")

load_css("assets/style.css")

customizar_sidebar()

config = load_config()
authenticator = auth(config)

try:
    authenticator.login(
        location='main',
        max_login_attempts=7,
        max_concurrent_users=9,
        key='Login',
        clear_on_submit=True,
        fields={
            'Form name': 'Login',
            'Username': 'Nome',
            'Password': 'Senha',
            'Login': 'Entrar'
        },
        captcha=config.get('auth', {}).get('use_captcha', True)
    )
except Exception as e:
    st.error(f'Erro durante a autenticação: {e}')

auth_status = st.session_state.get('authentication_status')

if auth_status:
    st.switch_page("pages/1_dashboard.py")


elif auth_status is False:
    st.error('Nome de usuário ou senha incorretos.')
    dump_login()

elif auth_status is None:
    st.info('Por favor, insira seu nome de usuário e senha.')
