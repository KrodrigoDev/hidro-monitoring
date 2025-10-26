import streamlit as st

def load_css(file_path: str) -> None:
    """
    Carrega arquivo CSS personalizado

    Args:
        file_path: Caminho para o arquivo CSS
    """
    with open(file_path, "r", encoding="utf-8") as f:
        css = f.read()
    # st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
    st.html(f"<style>{css}</style>")