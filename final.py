import matplotlib
import folium as folium
from folium.plugins import FastMarkerCluster
import streamlit as st
import pandas as pd
from streamlit_folium import st_folium, folium_static
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
            "https://github.com/fatcat-klm/vsosh/raw/main/archive%20(10).zip")
        df = pd.read_csv(data_url, nrows=rows)
        return df


    df = get_data(50000)
    st.sidebar.subheader('Описание параметров датасета')
    st.sidebar.subheader('Анализировать данные')
    st.markdown("### Анализ результатов участия московских школ во Всероссийской и Московской Олимпиаде Школьников")
    img_1 = "https://github.com/fatcat-klm/vsosh/raw/main/%D0%B2%D1%81%D0%BE%D1%88%20%D0%BB%D0%BE%D0%B3%D0%BE.jpg"
    st.image(img_1, width=500)
    st.markdown(
        " **ВСОШ** это самая престижная олимпиада, которая позволяет ее победителям и призерам поступить в профильный ВУЗ без вступительных испытаний. Например, став призером ВСОШ по экономике или математике можно поступить на бюджет ✨**Совбака**✨ без вступительных испытаний, чтобы создавать такие же прекрасные веб-приложения!")
    if st.button("Вы все уже победители🎈"):
        st.balloons()
    st.markdown(
        "Проанализировав различные характеристики датасета вы сможете выявить зависимости. Например,узнать какая школа является лидером в том или ином предмете")
    st.markdown(" ### Приступить к анализу данных")
    if st.checkbox("Показать датасет", False):
        st.subheader('Датасет')
        st.write(df)