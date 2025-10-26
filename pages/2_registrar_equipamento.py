import streamlit as st

from src.utils.sidebar import padrao_importacao_pagina
from src.utils.components import load_css

st.set_page_config(page_title="Dashboard", layout="wide")

padrao_importacao_pagina()
load_css("assets/style.css")