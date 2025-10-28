import streamlit as st

def load_css(file_path: str) -> None:
    """
    Carrega arquivo CSS personalizado

    Args:
        file_path: Caminho para o arquivo CSS
    """
    with open(file_path, "r", encoding="utf-8") as f:
        css = f.read()
    st.html(f"<style>{css}</style>")


def create_brand_header(title: str = "Hidro Monitoring",
                        subtitle: str = "Sistema de acompanhamento hidráulico") -> None:

    st.markdown(
        f"""
        <div class="brand-title">
            <span class="text-blue">{title}</span>
        </div>
        <div class="brand-subtitle">
            {subtitle}
        </div>
        """,
        unsafe_allow_html=True
    )