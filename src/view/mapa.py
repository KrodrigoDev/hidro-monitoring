
import folium
from shapely.geometry import Point
import geopandas as gpd
from folium.features import CustomIcon


def criar_mapa(df_filtrado, gdf_limites, tipo_equipamento='Todos', raio_metros=300):
    """
    Cria e retorna um mapa Folium com limites, pontos e buffers opcionais.

    Parâmetros:
    - df_filtrado: DataFrame com pontos de interesse
    - gdf_limites: GeoDataFrame com os limites da área
    - tipo_equipamento: filtro de equipamento ('Bomba', 'Reservatório', 'Poço' ou 'Todos')
    - raio_metros: raio para exibir área de abrangência das bombas
    """

    # Criar mapa centralizado (ex: Coruripe)
    m = folium.Map(location=[-10.124419, -36.176283], zoom_start=11)

    # Adicionar limites
    folium.GeoJson(
        gdf_limites,
        style_function=lambda x: {
            'fillColor': 'transparent',
            'color': 'black',
            'weight': 2,
            'fillOpacity': 0
        }
    ).add_to(m)

    # Adicionar pontos
    for _, ponto in df_filtrado.iterrows():
        lat, lon = ponto["lat"], ponto["lon"]
        nome, tipo = ponto["nome"], ponto["tipo"]
        ult_manutencao, ult_limpeza, situacao = ponto["ult_manutencao"], ponto["ult_limpeza"], ponto["situaçao"]
        amperagem, potencia, voltagem = ponto["amperagem"], ponto["potencia"], ponto["voltagem"]
        vazao, profundidade = ponto["vazão"], ponto["profundidade"]

        # Adicionar buffer se for Bomba
        if tipo == 'Bomba' and tipo_equipamento in ['Bomba', 'Todos']:
            ponto_geo = Point(lon, lat)
            buffer = ponto_geo.buffer(raio_metros / 111320, resolution=16)
            gdf_buffer = gpd.GeoDataFrame(geometry=[buffer], crs="EPSG:4326")
            folium.GeoJson(
                gdf_buffer,
                style_function=lambda x: {"fillColor": "lightblue", "color": "darkblue",
                                          "weight": 1, "fillOpacity": 0.3}
            ).add_to(m)

        # Conteúdo do popup
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

        # Ícone personalizado
        icone_path = {
            'Bomba': '../hidro-monitoring/image/bomba-de-agua.png',
            'Reservatório': '../hidro-monitoring/image/torre-de-agua.png',
            'Poço': '../hidro-monitoring/image/poco-de-agua.png'
        }.get(tipo, '../../image/default.png')

        custom_icon = CustomIcon(icon_image=icone_path, icon_size=(30, 30))

        folium.Marker(
            [lat, lon],
            popup=folium.Popup(popup_content, max_width=500),
            tooltip=nome,
            icon=custom_icon
        ).add_to(m)

    return m
