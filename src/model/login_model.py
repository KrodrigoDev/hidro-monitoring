import yaml
from yaml.loader import SafeLoader

import streamlit_authenticator as stauth


path_file = '../hidro-monitoring/.streamlit/config.yaml'


def dump_login() -> None:
    """Atualiza o arquivo de configuração de login."""
    with open(path_file, 'w', encoding='ISO-8859-1') as file:
        yaml.dump(config, file, default_flow_style=False, allow_unicode=True)


# Carrega configurações de autenticação
def load_config():
    """Carrega o arquivo de configuração do login."""
    with open(path_file, encoding='ISO-8859-1') as file:
        return yaml.load(file, Loader=SafeLoader)


def auth(config):
    authenticator = stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days'], auto_hash=True
    )

    return authenticator
