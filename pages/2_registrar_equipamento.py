from datetime import date
import streamlit as st
from time import sleep

from src.utils.sidebar import padrao_importacao_pagina
from src.utils.components import load_css
from src.model.database import SessionLocal
from src.model import crud

# ==================================================
# Configuração da página e CSS
# ==================================================
st.set_page_config(page_title="Registrar Equipamento", layout="wide")
load_css("assets/style.css")
padrao_importacao_pagina()

# ==================================================
# Banco de dados
# ==================================================
db = SessionLocal()
usuario = st.session_state.get("usuario_logado")

if not usuario:
    st.warning("Usuário não logado.")
    st.stop()

# ==================================================
# Divisão dos forms
# ==================================================
tab1, tab2 = st.tabs(["Cadastrar Local", "Cadastrar Equipamento"])

# ==================================================
# Aba 1: Cadastro do Local do Equipamento
# ==================================================
with tab1:
    st.subheader("Cadastro do Local do Equipamento")
    municipio = st.selectbox("Município", key="municipio", options=['Coruripe'])
    bairro = st.selectbox("Bairro", key="bairro", options=['Conjunto Doutor Fialho', 'Centro', 'Cruzeiro'])
    lat_long = st.text_input("Coordenadas (Latitude e Longitude)", key="lat_long")

    with st.expander("Como conseguir as coordenadas"):
        st.markdown('''
        Para obter as **coordenadas de latitude e longitude** no formato correto (ex: `-10.123456, -36.543210`), siga os passos abaixo:

        1. Acesse o [Google Maps](https://www.google.com/maps).
        2. Localize o ponto exato onde o equipamento está instalado.
        3. Clique **com o botão direito do mouse** sobre o local desejado.
        4. No menu que aparecer, clique sobre os **números de latitude e longitude** exibidos no topo.
        5. As coordenadas serão **copiadas automaticamente** para a área de transferência.
        6. Cole-as no campo **"Coordenadas (Latitude e Longitude)"** acima.

        ''', unsafe_allow_html=True)

    if st.button("Salvar Local"):
        coordenadas = lat_long.split(',')

        if len(coordenadas) == 2:
            local = crud.criar_local_equipamento(
                db=db,
                municipio=municipio,
                bairro=bairro,
                latitude=coordenadas[0],
                longitude=coordenadas[1]
            )

            st.session_state.id_local_equipamento = local.id
            st.success(f"Local '{coordenadas[0]} , {coordenadas[1]}' cadastrado com sucesso!")
            st.info("Agora vá para a aba 'Cadastrar Equipamento' para registrar o equipamento neste local.")

        else:
            st.error('Informe as coordenadas de forma correta e separadas por vírgula.')

# ==================================================
# Aba 2: Cadastro do Equipamento
# ==================================================
with tab2:
    st.subheader("Cadastro do Equipamento")

    if "id_local_equipamento" not in st.session_state:
        st.warning("Primeiro cadastre o local do equipamento na aba 'Cadastrar Local'.")
    else:

        tipo = st.selectbox("Tipo de equipamento", key="tipo", options=['Bomba', 'Reservatório', 'Poço'])
        nome = st.text_input("Nome popular", key="nome")
        situacao = st.selectbox("Situação", key="situacao", options=['Funcionando', 'Manutenção', 'Inativo'])

        if tipo == 'Bomba':
            voltagem = st.text_input("Voltagem", key="voltagem")
            vazao = st.number_input("Vazão (L/s)", min_value=0.0, step=0.1, key="vazao")
            ult_manutencao = st.date_input("Última manutenção", value=date.today(), key="manutencao")
            profundidade = st.number_input("Profundidade (m)", min_value=0.0, step=0.1, key="profundidade")

        elif tipo == 'Reservatório':
            voltagem = vazao = ult_manutencao = profundidade = None

        elif tipo == 'Poço':
            profundidade = st.number_input("Profundidade (m)", min_value=0.0, step=0.1, key="profundidade")
            voltagem = vazao = ult_manutencao = None

        ult_limpeza = st.date_input("Última limpeza", value=date.today(), key="limpeza")

        if st.button("Salvar Equipamento"):
            id_empresa = usuario.id_empresa

            equipamento = crud.criar_equipamento(
                db=db,
                nome=nome,
                tipo=tipo,
                situacao=situacao,
                voltagem=voltagem,
                vazao=vazao,
                profundidade=profundidade,
                ult_manutencao=ult_manutencao,
                ult_limpeza=ult_limpeza,
                id_empresa=id_empresa,
                id_local_equipamento=st.session_state.id_local_equipamento
            )

            crud.registrar_log(db, id_usuario=usuario.id, acao="criar", id_equipamento=equipamento.id)

            st.balloons()
            sleep(2)
            del st.session_state['id_local_equipamento']
            st.rerun()
