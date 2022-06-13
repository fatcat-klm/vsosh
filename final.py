import matplotlib
import folium as folium
from folium.plugins import FastMarkerCluster
import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
from geopy import distance
from shapely.geometry import Point

with st.echo(code_location='below'):
    matplotlib.use("Agg")
    st.set_option('deprecation.showPyplotGlobalUse', False)


    @st.cache(persist=True, show_spinner=True)
    def get_data(rows):
        data_url = (
            "https://github.com/fatcat-klm/vsosh/raw/main/flavors_of_cacao%20(2).csv.zip")
        df = pd.read_csv(data_url, nrows=rows)
        return df


    df = get_data(50000)
    st.sidebar.subheader('Описание параметров датасета')
    st.sidebar.subheader('Анализировать данные')
    st.markdown(" ### Приступить к анализу данных")
    if st.checkbox("Показать датасет", False):
        st.subheader('Датасет')
        st.write(df)