import streamlit as st
import folium
from shapely.geometry import Point
import geopandas as gpd
from streamlit_folium import st_folium
import pandas as pd
from dotenv import dotenv_values

# Título principal
st.header("Panorama Geral")


@st.cache_data
def carregar_dados():
    url_dataframe = dotenv_values('../hidro-monitoring/data/bombas.env')['URL_DATAFRAME']

    df = pd.read_csv(url_dataframe, decimal=',')

    shp_coruripe = gpd.read_file('../Painel_Daesc/data/shp/delimitacao_coruripe.shp')

    return df, shp_coruripe


df_bombas, gdf_limites = carregar_dados()

# Seção de Filtros
with st.sidebar:
    st.header('Filtros')

    area = st.selectbox('Área', options=['Todos'] + df_bombas['area'].unique().tolist())

    tipo_situacao = st.selectbox('Situação', options=['Todos'] + df_bombas['Situaçao'].unique().tolist())

    tipo_equipamento = st.selectbox('Tipo de Equipamento', options=['Todos'] + df_bombas['Tipo'].unique().tolist())

    ativar_raio = st.checkbox(label='Raio de abrangência', key="manter_raio", label_visibility="visible")

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

df_filtrado = df_bombas.copy()

# Aplicar filtros
if area != 'Todos':
    df_filtrado = df_bombas[df_bombas['area'] == area].copy()

if tipo_equipamento != 'Todos':
    df_filtrado = df_filtrado[df_filtrado['Tipo'] == tipo_equipamento]

if tipo_situacao != 'Todos':
    df_filtrado = df_filtrado[df_filtrado['Situaçao'] == tipo_situacao]

# Métricas de Contagem
metricas = df_filtrado['Tipo'].value_counts().to_dict()

col1, col2, col3 = st.columns(3)

col1.container(border=True).metric(label='Total de Bombas', value=metricas.get('Bomba', 0))
col2.container(border=True).metric(label='Total de Reservatórios', value=metricas.get('Reservatório', 0))
col3.container(border=True).metric(label='Total de Poços', value=metricas.get('Poço', 0))

with st.container(border=True):
    if (tipo_equipamento in ['Todos'] or metricas.get('Bomba')) and ativar_raio:
        raio_metros = st.slider("Raio de abrangência (metros)", min_value=100, max_value=5000, value=300, step=50)

    # Criar o mapa centralizado em Coruripe
    m = folium.Map(location=[-10.124419, -36.176283], zoom_start=11)

    # Adicionar os limites de Coruripe ao mapa com estilo sem preenchimento
    folium.GeoJson(
        gdf_limites,
        style_function=lambda x: {
            'fillColor': 'transparent',  # Remover a cor de fundo (preenchimento)
            'color': 'black',  # Cor da borda (linha)
            'weight': 2,  # Espessura da linha
            'fillOpacity': 0  # Opacidade do preenchimento (0 significa transparente)
        }
    ).add_to(m)

    # Adicionar pontos ao mapa
    for _, ponto in df_filtrado.iterrows():
        lat, lon = ponto["lat"], ponto["lon"]
        nome, tipo = ponto["nome"], ponto["Tipo"]
        ult_manutencao, ult_limpeza, situacao = ponto["ult_manutencao"], ponto["ult_limpeza"], ponto["Situaçao"]
        amperagem, potencia = ponto["amperagem"], ponto["potencia"]

        if tipo == 'Bomba' and tipo_equipamento in ['Bomba', 'Todos'] and ativar_raio:
            ponto_geo = Point(lon, lat)
            buffer = ponto_geo.buffer(raio_metros / 111320)

            gdf = gpd.GeoDataFrame(geometry=[buffer], crs="EPSG:4326")

            folium.GeoJson(
                gdf, style_function=lambda x: {"fillColor": "lightblue", "color": "darkblue", "weight": 1,
                                               "fillOpacity": 0.3}
            ).add_to(m)

        popup_content = f"""
        <div style="width: 350px;">
            <b>{nome}</b><br>
            Última Manutenção: {ult_manutencao}<br>
            Última Limpeza: {ult_limpeza}<br>
            Situação: {situacao}<br>
            Amperagem: {amperagem}<br>
            Potência: {potencia}<br>
            Coordenadas: {lat}, {lon}<br>
        </div>
        """

        icone_path = {
            'Bomba': '../Painel_Daesc/images/bomba-de-agua.png',
            'Reservatório': '../Painel_Daesc/images/torre-de-agua.png',
            'Poço': '../Painel_Daesc/images/poco-de-agua.png'
        }.get(tipo, '../Painel_Daesc/images/default.png')

        custom_icon = folium.CustomIcon(icon_image=icone_path, icon_size=(30, 30))

        folium.Marker(
            [lat, lon], popup=folium.Popup(popup_content, max_width=500),
            tooltip=nome, icon=custom_icon
        ).add_to(m)

    # Exibir o mapa
    st_folium(m, width=800, height=600)

# Botão para atualizar os dados
if st.button("🔄 Atualizar Dados"):
    st.cache_data.clear()
