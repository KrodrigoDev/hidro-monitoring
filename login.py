import yaml
from yaml.loader import SafeLoader
import streamlit as st
import streamlit_authenticator as stauth
from sidebar import run_sidebar
from scripts.data_loader import carregar_dados

# Caminho do arquivo de configuração
path_file = '../hidro-monitoring/.streamlit/config.yaml'


def dump_login() -> None:
    """Atualiza o arquivo de configuração de login."""
    with open(path_file, 'w') as file:
        yaml.dump(config, file, default_flow_style=False, allow_unicode=True)


# Carrega configurações de autenticação
def load_config():
    """Carrega o arquivo de configuração do login."""
    with open(path_file, encoding='ISO-8859-1') as file:
        return yaml.load(file, Loader=SafeLoader)


# Inicializa a autenticação
config = load_config()
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'], auto_hash=True
)

try:
    # Definição das regras de login
    authenticator.login(
        location='main', max_login_attempts=7, max_concurrent_users=9, key='Login', clear_on_submit=True,
        fields={'Form name': 'Login', 'Username': 'Nome', 'Password': 'Senha', 'Login': 'Entrar'},
        captcha=config.get('auth', {}).get('use_captcha', True)
    )
except Exception as e:
    st.error(f'Erro durante a autenticação: {e}')

if st.session_state.get('authentication_status'):

    if 'df_bombas' not in st.session_state or 'gdf_limites' not in st.session_state:
        st.session_state.df_bombas, st.session_state.gdf_limites = carregar_dados()

    run_sidebar(authenticator)

    pg = st.navigation(pages=[st.Page('app.py')], expanded=False, position='sidebar')
    pg.run()

elif st.session_state.get('authentication_status') is False:
    st.error('O nome ou senha está incorreto!')
    dump_login()

elif st.session_state.get('authentication_status') is None:
    st.warning('Por favor insira seu nome e senha.')
