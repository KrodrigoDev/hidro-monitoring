import streamlit as st
from typing import List, Optional, Union


def create_number_card(number: Union[int, float, str], label: Optional[str] = None) -> None:
    """
    Cria um card com um número centralizado, similar a um metric.

    Args:
        number: Número a ser exibido
        label: Rótulo opcional abaixo do número
    """
    st.markdown(
        f"""
        <div class="info-card" style="display: flex; flex-direction: column; align-items: center; justify-content: center; min-height: 120px;">
            {f'<div style="font-size: 1.1rem; font-weight: 500; color: var(--primary, #004B8D); margin-bottom: 0.5rem;">{label}</div>' if label else ''}
            <div style="font-size: 2.5rem; font-weight: bold; color: var(--primary, #004B8D);">{number}</div>
        </div>
        """,
        unsafe_allow_html=True
    )