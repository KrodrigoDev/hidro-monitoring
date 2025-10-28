import streamlit as st

from src.model.database import SessionLocal
from src.model import crud
from src.utils.sidebar import padrao_importacao_pagina
from src.utils.components import load_css

# ==================================================
# Configuração da página e CSS
# ==================================================
st.set_page_config(page_title="Histórico", layout="wide")
load_css("assets/style.css")
padrao_importacao_pagina()
