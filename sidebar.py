import streamlit as st


def run_sidebar(authenticator):
    with st.sidebar:
        st.image('../hidro-monitoring/images/logo-daesc.png')
        st.divider()

        # Seção do usuário
        if st.session_state.get('authentication_status'):
            with st.expander("👤 **Usuário Logado**", expanded=True):
                st.markdown(f"**Nome:** {st.session_state.get('name')}")
                st.markdown(f"**Email:** {st.session_state.get('email')}")
                st.markdown(f"**Acesso:** `{', '.join(st.session_state.get('roles'))}`")

        col_1, col_2 = st.columns(2)
        with col_1:
            if st.button("🔄 Atualizar Dados"):
                st.cache_data.clear()
        with col_2:
            authenticator.logout(button_name='🔒 Deslogar', key='pos_login')

        st.divider()

        # Acessa o DataFrame do session_state
        df_bombas = st.session_state.df_bombas

        # Seção de filtros
        with st.expander("🎯 **Filtros**", expanded=True):
            # Armazena os filtros no session_state
            st.session_state.area = st.selectbox('Área', options=['Todos'] + df_bombas['area'].unique().tolist())

            st.session_state.tipo_situacao = st.selectbox('Situação',
                                                          options=['Todos'] + df_bombas['situaçao'].unique().tolist())

            st.session_state.tipo_equipamento = st.selectbox('Tipo de Equipamento',
                                                             options=['Todos'] + df_bombas['tipo'].unique().tolist())

            st.session_state.ativar_raio = st.checkbox(label='Raio de abrangência (Bomba)', key="manter_raio",
                                                       label_visibility="visible",
                                                       value=True)

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
