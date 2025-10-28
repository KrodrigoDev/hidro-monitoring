import streamlit as st


def criar_botao_navegacao(nome_pagina, caminho_pagina, icone, tipo="secondary"):
    """
    Cria um botão de navegação na barra lateral que redireciona para a página especificada.

    Args:
        nome_pagina (str): Nome a ser exibido no botão
        caminho_pagina (str): Caminho para o arquivo da página (ex: "pages/cadastro.py")
        icone (str): Ícone a ser exibido no botão
        tipo (str): Tipo do botão (primary, secondary)

    Returns:
        bool: True se o botão foi clicado, False caso contrário
    """

    pagina_atual = st.session_state.get("selected_page", "")

    tipo_botao = "primary" if pagina_atual == nome_pagina else tipo
    if st.sidebar.button(f"{icone} {nome_pagina}", use_container_width=True, type=tipo_botao):
        st.session_state.selected_page = nome_pagina
        st.switch_page(caminho_pagina)
        return True
    return False


def exibir_menu_navegacao():
    """
    Exibe o menu de navegação na barra lateral com base nas permissões do usuário.
    """

    paginas = {
        "1_dashboard": {"nome_exibicao": "Dashboard", "caminho": "pages/1_dashboard.py", "icone": ""},
        "2_registrar_equipamento": {"nome_exibicao": "Registrar", "caminho": "pages/2_registrar_equipamento.py",
                                    "icone": ""},
        "3_historico": {"nome_exibicao": "Histórico", "caminho": "pages/3_historico.py", "icone": ""}
    }

    if not st.session_state.get("authentication_status"):
        st.switch_page("pages/login.py")

    for chave_pagina, info in paginas.items():
        criar_botao_navegacao(info["nome_exibicao"], info["caminho"], info["icone"], "primary")

    st.sidebar.markdown("---")

    if st.sidebar.button("Sair", use_container_width=True, type='primary'):
        for key in list(st.session_state.keys()):
            if key.startswith("authentication") or key in ("username", "name"):
                del st.session_state[key]

        st.session_state["authentication_status"] = None
        st.session_state["usuario_logado"] = None

        st.switch_page("pages/login.py")


def ocultar_barra_lateral_streamlit():
    """
    Função para ocultar a barra lateral do Streamlit, utilizando CSS.
    """

    st.markdown("""
        <style>
        [data-testid="stSidebarNav"] {display: none;}
        </style>
    """, unsafe_allow_html=True)


def configurar_sidebar_marca():
    """
    Exibe o logo da empresa e um separador visual na barra lateral.
    """
    st.sidebar.image("image/logo-daesc.png")
    st.sidebar.caption('---')


def titulos_pagina(
        text,
        font_size="3.1em",
        # text_color="#3064AD",
        text_color="#3064AD",
        icon=None
):
    """
    Cria um cabeçalho estilizado com texto, tamanho de fonte e ícone HTML personalizáveis.

    Parâmetros:
    - text (str): O texto a ser exibido no cabeçalho
    - font_size (str): Tamanho da fonte (padrão: "3.1em")
    - text_color (str): Cor do texto (padrão: "#3064AD")
    - bg_color (str): Cor de fundo (padrão: "#F0F2F9")
    - border_color (str): Cor da borda (padrão: "#EAEDF1")
    - icon_html (str): HTML do ícone (ex: '<i class="fas fa-balance-scale"></i>') a ser exibido antes do texto
    """
    icon_part = f"{icon} " if icon else ""
    st.markdown(
        f"""
        <h1 style='
            text-align: center;
            color: {text_color};
            font-weight: bold;
            margin: 0;
            padding: 0;
            font-size: {font_size};
            white-space: pre-line;
        '>
            {icon_part}<b>{text}</b>
        </h1>
        """,
        unsafe_allow_html=True
    )


def exibir_info_usuario_sidebar():
    """
    Exibe o nome do usuário em uma caixa estilizada na barra lateral, se disponível.
    """
    if st.session_state.get('authentication_status'):
        st.sidebar.markdown(f"""
        <style>
        .caixa-info-usuario {{
            background: #EAEDF1;
            color: #3064AD;
            border-radius: 10px;
            padding: 18px 12px 14px 12px;
            margin-bottom: 10px;
            font-size: 1.05em;
            font-weight: 500;
            box-shadow: 0 2px 8px rgba(48,100,173,0.08);
            text-align: center;
        }}
        .caixa-info-usuario a {{
            color: #3064AD;
            text-decoration: underline;
            font-weight: bold;
        }}
        .caixa-info-usuario a:hover {{
            color: #18325e;
            text-decoration: underline;
        }}
        </style>
        <div class="caixa-info-usuario">
            {st.session_state.get('usuario_logado').nome}
        </div>
        """, unsafe_allow_html=True)
        st.sidebar.markdown("<br>", unsafe_allow_html=True)


def customizar_sidebar():
    """
    Função principal para customizar a barra lateral do Streamlit.
    """
    ocultar_barra_lateral_streamlit()
    configurar_sidebar_marca()
    exibir_info_usuario_sidebar()


def padrao_importacao_pagina():
    """
    Função para definir o padrão de importação do Streamlit.
    """
    customizar_sidebar()
    exibir_menu_navegacao()
