import streamlit as st


def run_sidebar(df_bombas):
    with st.sidebar:

        # Seção de filtros
        with st.expander("🎯 **Filtros**", expanded=True):
            # Armazena os filtros no session_state
            area = st.selectbox('Área', options=['Todos'] + df_bombas['area'].unique().tolist())

            tipo_situacao = st.selectbox('Situação',
                                         options=['Todos'] + df_bombas['situaçao'].unique().tolist())

            tipo_equipamento = st.selectbox('Tipo de Equipamento',
                                            options=['Todos'] + df_bombas['tipo'].unique().tolist())

            ativar_raio = st.checkbox(label='Raio de abrangência (Bomba)', key="manter_raio",
                                      label_visibility="visible",
                                      value=True)

        if st.button("🔄 Atualizar Dados"):
            st.cache_data.clear()

        st.divider()

        # Rodapé personalizado
        st.markdown(
            """
            <div style="text-align: center; font-size: 14px; margin-top: 20px;">
                Created by <b>Kauã Rodrigo</b> 🚀<br>
                <a href="https://www.linkedin.com/in/krodrigodev/" target="_blank">LinkedIn</a> |
                <a href="https://github.com/KrodrigoDev" target="_blank">GitHub</a>
            </div>
            """,
            unsafe_allow_html=True
        )

        return area, tipo_situacao, tipo_equipamento, ativar_raio
