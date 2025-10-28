import streamlit as st
from src.model.database import SessionLocal
from src.model import crud, models
from src.utils.sidebar import customizar_sidebar
from src.utils.components import load_css

# ==================================================
# Configuração da página e CSS
# ==================================================
st.set_page_config(page_title="Criar Usuário", layout="wide")
load_css("assets/style.css")
customizar_sidebar()


# ==================================================
# Função de validação básica de CPF
# ==================================================
def validar_cpf(cpf: str) -> bool:

    cpf = ''.join(filter(str.isdigit, cpf))

    # Verifica tamanho
    if len(cpf) != 11:
        return False

    # Verifica se todos os dígitos são iguais
    if cpf == cpf[0] * 11:
        return False

    # Exemplo simples de multiplicação para validação complementar
    soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
    if soma <= 0:
        return False

    return True


# ==================================================
# Container do Formulário
# ==================================================
with st.container():
    st.subheader("Cadastro de Usuário")

    nome = st.text_input("Nome")
    sobrenome = st.text_input("Sobrenome")
    cpf = st.text_input("CPF")
    senha = st.text_input("Senha", type="password")
    confirmar_senha = st.text_input("Confirmar Senha", type="password")

    # Colunas para botões
    col1, col2 = st.columns(2)

    with col1:
        if st.button("Criar Usuário", use_container_width=True):

            # Valida preenchimento
            if not all([nome, sobrenome, cpf, senha, confirmar_senha]):
                st.warning("Preencha todos os campos!")

            # Valida senhas
            elif senha != confirmar_senha:
                st.error("As senhas não coincidem!")

            # Valida CPF
            elif not validar_cpf(cpf):
                st.error("CPF inválido! Verifique os dígitos.")
            else:
                db = SessionLocal()

                # Verifica se já existe usuário com o CPF informado
                usuario_existente = db.query(models.Usuario).filter(models.Usuario.cpf == cpf).first()

                if not usuario_existente:
                    crud.criar_usuario(
                        db,
                        nome=nome,
                        sobrenome=sobrenome,
                        cpf=cpf,
                        senha=senha,
                        id_empresa=1
                    )
                    st.success(f"Usuário {nome} criado com sucesso!")
                    st.balloons()
                else:
                    st.info("Já existe um usuário cadastrado com este CPF.")
                db.close()

    with col2:
        if st.button("Voltar", type='secondary'):
            st.switch_page('pages/login.py')
