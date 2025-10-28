import folium
from shapely.geometry import Point, box
import geopandas as gpd
from folium.features import CustomIcon


def gerar_popup(ponto):
    """
    Gera o conteúdo HTML do popup dinamicamente conforme o tipo de equipamento.
    """
    nome = ponto["nome"]
    tipo = ponto["tipo"]
    lat, lon = ponto["latitude"], ponto["longitude"]
    situacao = ponto.get("situacao", "—")
    ult_manutencao = ponto.get("ult_manutencao", "—")
    ult_limpeza = ponto.get("ult_limpeza", "—")

    html = f"""
    <div style="width: 320px; font-family: Arial, sans-serif;">
        <h4 style="margin: 5px 0;">{nome}</h4>
        <p><b>Tipo:</b> {tipo}</p>
        <p><b>Situação:</b> {situacao}</p>
        <hr style="border: 0.5px solid #ccc;">
        <p><b>Última Limpeza:</b> {ult_limpeza}</p>
    """

    # 🔹 Campos específicos por tipo
    if tipo == "Bomba":
        voltagem = ponto.get("voltagem", "—")
        vazao = ponto.get("vazao", "—")
        profundidade = ponto.get("profundidade", "—")
        html += f"""
            <p><b>Última Manutenção:</b> {ult_manutencao}</p>
            <hr style="border: 0.5px solid #ccc;">
            <p><b>Voltagem:</b> {voltagem}</p>
            <p><b>Vazão:</b> {vazao}</p>
            <p><b>Profundidade:</b> {profundidade}</p>
        """

    elif tipo == "Reservatório":
        capacidade = ponto.get("capacidade", "—")
        material = ponto.get("material", "—")
        html += f"""
            <hr style="border: 0.5px solid #ccc;">
            <p><b>Capacidade:</b> {capacidade} L</p>
            <p><b>Material:</b> {material}</p>
        """

    elif tipo == "Poço":
        profundidade = ponto.get("profundidade", "—")
        nivel_agua = ponto.get("nivel_agua", "—")
        html += f"""
            <hr style="border: 0.5px solid #ccc;">
            <p><b>Profundidade:</b> {profundidade} m</p>
            <p><b>Nível da Água:</b> {nivel_agua} m</p>
        """

    return html


def criar_mapa(df_filtrado, tipo_equipamento='Todos', raio_metros=300):
    """
    Cria e retorna um mapa Folium com pontos e buffers opcionais.
    """
    m = folium.Map(location=[-10.124419, -36.176283], zoom_start=11)

    # Limites do município
    shp_path = '../hidro-monitoring/src/model/shp/delimitacao_coruripe.shp'
    gdf = gpd.read_file(shp_path)

    # ✅ Padroniza o CRS para EPSG:4326 (WGS84)
    gdf = gdf.to_crs(epsg=4326)

    # Borda do município
    folium.GeoJson(
        gdf,
        style_function=lambda x: {
            'fillColor': 'transparent',
            'color': 'black',
            'weight': 2,
            'fillOpacity': 0
        }
    ).add_to(m)

    # 🔹 Cria o "mundo" e escurece tudo fora do município
    world = gpd.GeoDataFrame(geometry=[box(-180, -90, 180, 90)], crs="EPSG:4326")
    mask_outside = world.overlay(gdf, how='difference')

    folium.GeoJson(
        mask_outside,
        style_function=lambda x: {
            'fillColor': 'black',
            'color': 'black',
            'weight': 0,
            'fillOpacity': 0.6  # ajuste de intensidade da sombra
        }
    ).add_to(m)

    # 🔹 Adiciona os pontos filtrados
    for _, ponto in df_filtrado.iterrows():
        lat, lon = ponto["latitude"], ponto["longitude"]
        tipo = ponto["tipo"]

        # Buffer visual (somente bombas)
        if tipo == 'Bomba' and tipo_equipamento in ['Bomba', 'Todos']:
            ponto_geo = Point(lon, lat)
            buffer = ponto_geo.buffer(raio_metros / 111320, resolution=16)
            gdf_buffer = gpd.GeoDataFrame(geometry=[buffer], crs="EPSG:4326")

            folium.GeoJson(
                gdf_buffer,
                style_function=lambda x: {
                    "fillColor": "lightblue",
                    "color": "darkblue",
                    "weight": 1,
                    "fillOpacity": 0.3
                }
            ).add_to(m)

        # Popup dinâmico
        popup_content = gerar_popup(ponto)

        # Ícone específico
        icone_path = {
            'Bomba': '../hidro-monitoring/image/bomba-de-agua.png',
            'Reservatório': '../hidro-monitoring/image/torre-de-agua.png',
            'Poço': '../hidro-monitoring/image/poco-de-agua.png'
        }.get(tipo, '../hidro-monitoring/image/default.png')

        custom_icon = CustomIcon(icon_image=icone_path, icon_size=(30, 30))

        folium.Marker(
            [lat, lon],
            popup=folium.Popup(popup_content, max_width=500),
            tooltip=ponto["nome"],
            icon=custom_icon
        ).add_to(m)

    return m
