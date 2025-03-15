import pandas as pd
import geopandas as gpd
import os
import streamlit as st


@st.cache_data
def carregar_dados():
    """Carrega os dados do DataFrame e do shapefile de Coruripe."""
    URL_DATAFRAME = os.getenv('URL_DATAFRAME')

    if not URL_DATAFRAME:
        raise ValueError("A variável 'URL_DATAFRAME' não foi encontrada no arquivo de configuração.")

    df = pd.read_csv(URL_DATAFRAME, decimal=',')

    shp_path = '../hidro-monitoring/data/shp/delimitacao_coruripe.shp'
    gdf = gpd.read_file(shp_path)

    return df, gdf
