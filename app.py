import streamlit as st
import folium
from shapely.geometry import Point
import geopandas as gpd
from streamlit_folium import st_folium
from scripts.data_loader import carregar_dados
from sidebar import run_sidebar

# Carregando dados
df_filtrado, gdf_limites = carregar_dados()

# Título principal
st.header("Panorama Geral")

area, tipo_equipamento, tipo_situacao, ativar_raio = run_sidebar(df_filtrado)

# Aplicar filtros
if area != 'Todos':
    df_filtrado = df_filtrado[df_filtrado['area'] == area].copy()

if tipo_equipamento != 'Todos':
    df_filtrado = df_filtrado[df_filtrado['tipo'] == tipo_equipamento]

if tipo_situacao != 'Todos':
    df_filtrado = df_filtrado[df_filtrado['situaçao'] == tipo_situacao]

# Métricas de Contagem
metricas = df_filtrado['tipo'].value_counts().to_dict()

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
        nome, tipo = ponto["nome"], ponto["tipo"]
        ult_manutencao, ult_limpeza, situacao = ponto["ult_manutencao"], ponto["ult_limpeza"], ponto["situaçao"]
        amperagem, potencia, voltagem = ponto["amperagem"], ponto["potencia"], ponto["voltagem"]
        vazao, profundidade = ponto["vazão"], ponto["profundidade"]

        if tipo == 'Bomba' and tipo_equipamento in ['Bomba', 'Todos'] and ativar_raio:
            ponto_geo = Point(lon, lat)
            buffer = ponto_geo.buffer(raio_metros / 111320)

            gdf = gpd.GeoDataFrame(geometry=[buffer], crs="EPSG:4326")

            folium.GeoJson(
                gdf, style_function=lambda x: {"fillColor": "lightblue", "color": "darkblue", "weight": 1,
                                               "fillOpacity": 0.3}
            ).add_to(m)

        popup_content = f"""
            <div style="width: 320px; font-family: Arial, sans-serif;">
                <h4 style="margin: 5px 0;">{nome}</h4>
                <hr style="border: 0.5px solid #ccc;">
                <p><b>Última Manutenção: </b>{ult_manutencao}</p>
                <p><b>Última Limpeza: </b>{ult_limpeza}</p>
                <p><b>Situação: </b>{situacao}</p>
                <hr style="border: 0.5px solid #ccc;">
                <p><b>Voltagem: </b>{voltagem}</p>
                <p><b>Amperagem: </b>{amperagem}</p>
                <p><b>Potência: </b>{potencia}</p>
                <hr style="border: 0.5px solid #ccc;">
                <p><b>Coordenadas: </b>{lat}, {lon}</p>
                <p><b>Vazão: </b>{vazao}</p>
                <p><b>Profundidade: </b>{profundidade}</p>
            </div>
        """

        icone_path = {
            'Bomba': '../hidro-monitoring/images/bomba-de-agua.png',
            'Reservatório': '../hidro-monitoring/images/torre-de-agua.png',
            'Poço': '../hidro-monitoring/images/poco-de-agua.png'
        }.get(tipo, '../hidro-monitoring/images/default.png')

        custom_icon = folium.CustomIcon(icon_image=icone_path, icon_size=(30, 30))

        folium.Marker(
            [lat, lon], popup=folium.Popup(popup_content, max_width=500),
            tooltip=nome, icon=custom_icon
        ).add_to(m)

    # Exibir o mapa
    st_folium(m, width=800, height=600)
