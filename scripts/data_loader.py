import pandas as pd
import geopandas as gpd
from dotenv import dotenv_values
import streamlit as st


@st.cache_data
def carregar_dados():
    """Carrega os dados do DataFrame e do shapefile de Coruripe."""
    config = dotenv_values('../hidro-monitoring/data/bombas.env')
    url_dataframe = config.get('URL_DATAFRAME')

    if not url_dataframe:
        raise ValueError("A variável 'URL_DATAFRAME' não foi encontrada no arquivo de configuração.")

    df = pd.read_csv(url_dataframe, decimal=',')

    shp_path = '../hidro-monitoring/data/shp/delimitacao_coruripe.shp'
    gdf = gpd.read_file(shp_path)

    return df, gdf
