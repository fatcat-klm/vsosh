from geopy.extra.rate_limiter import RateLimiter
import matplotlib
import seaborn as sns
import streamlit as st
import pandas as pd
import seaborn as sns
import altair as alt
from geopy import distance
from typing import Union, Any
import folium as folium
from folium.plugins import MarkerCluster, FastMarkerCluster
import streamlit as st
import pandas as pd
from streamlit_folium import st_folium, folium_static
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import altair as alt
import geopandas
from geopy import distance
from shapely.geometry import Point, MultiPolygon
from shapely.wkt import dumps, loads

with st.echo(code_location='below'):
    matplotlib.use("Agg")
    st.set_option('deprecation.showPyplotGlobalUse', False)


    @st.cache(persist=True, show_spinner=True)
    def get_data(rows):
        data_url = (
            "https://github.com/fatcat-klm/vsosh/raw/main/%D0%9A%D0%BE%D0%BF%D0%B8%D1%8F%20moscow%20schools%20"
            "-%20winners%20-%20moscow%20schools%20-%20winners%20("
            "2)%20-%20moscow%20schools%20-%20winners%20-%20moscow%20schools%20-%20winners%20(2).csv.zip")
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

    st.title('Описание параметров датасета')
    if st.sidebar.checkbox('Формат данных'):
        st.subheader('Формат данных:')
        st.write(df.head())
    if st.sidebar.checkbox('Параметры'):
        st.subheader('Параметры:')
        st.write(df.columns.to_list())
    if st.sidebar.checkbox('Статистически описываемые данные'):
        st.subheader('Статистически описываемые данные')
        st.write(df.describe())

    st.title('Анализировать данные')
    st.sidebar.markdown("## Меняйте параметры модели, чтобы создать интересующие вас визуализации данных")
    st.info(
        "Если при построении выдается ошибка, то формат выбранного параметра не подходит для построения графика такого типа. Выберите другой")
    if st.sidebar.checkbox('Count Plot'):
        st.subheader('Count Plot')
        column_count_plot_x = st.sidebar.selectbox("Х Подходят только числовые значения: ", df.columns)
        column_count_plot_y = st.sidebar.selectbox("Y дополнительная переменная:",
                                                   df.columns.insert(0, None))
        fig = sns.countplot(x=column_count_plot_x, hue=column_count_plot_y, data=df, palette="husl",
                            labels=[df.columns.insert(0, None)])
        st.pyplot()

    if st.sidebar.checkbox('Boxplot'):
        st.subheader('Boxplot')
        column_box_plot_X = st.sidebar.selectbox("X Подходят только числовые значения:", df.columns)
        column_box_plot_Y = st.sidebar.selectbox("Y: ", df.columns.insert(0, None))
        column_box_plot_Z = st.sidebar.selectbox("Z дополнительная переменная:", df.columns.insert(0, None))
        fig = sns.boxplot(x=column_box_plot_X, y=column_box_plot_Y, hue=column_box_plot_Z, data=df, palette="husl",
                          labels=[df.columns.insert(0, None)])
        st.pyplot()

    if st.sidebar.checkbox('Distplot'):
        st.subheader('Distplot')
        column_dist_plot = st.sidebar.selectbox("Подходят только числовые значения:", df.columns)
        fig = sns.distplot(df[column_dist_plot])
        st.pyplot()

    if st.sidebar.checkbox('Pairplot'):
        st.subheader('Pairplot')
        column_pair_plot = st.sidebar.selectbox("X дополнительная переменная:)", df.columns)
        fig = sns.pairplot(df, hue=column_pair_plot, palette="husl")
        st.pyplot()

    st.sidebar.markdown(
        "[Источник исходного датасета](https://www.kaggle.com/datasets/romazepa/moscow-schools-winners-of-educational-olympiads?resource=download)")
    st.sidebar.markdown(
        "[Программа на основе](https://github.com/maladeep/palmerpenguins-streamlit-eda)")


    @st.cache()
    def get_distance():
        # Добавляем расстояние до центра Москвы
        distance_from_c = []
        for lat, long in zip(df['lat'], df['long']):
            distance_from_c.append(distance.distance((lat, long), (55.753544, 37.621211)).km)
            # geometry.append(Point(lon, lat))
        return pd.Series(distance_from_c)

    dist = get_distance()
    df['distance_from_center'] = dist


    @st.cache()
    def get_districts():
        # Здесь мы получаем данные о полигонах московских административных округов и районов
        # source (http://osm-boundaries.com)

        districts_df = geopandas.read_file(
            'https://drive.google.com/file/d/1dUazgN1VCYcBCEi09cNeJfReNmnU_jmw/view?usp=sharing')
        moscow = geopandas.read_file(
            'https://drive.google.com/file/d/1DM1zXVsMDt_T8F_iCIAU_oAFeTM3Pw0E/view?usp=sharing')
        okruga = geopandas.read_file(
            'https://drive.google.com/file/d/1yK8Si_Hq7W5Cak79a7XQ5yt0TFEuBLiH/view?usp=sharing')
        moscow_geometry = list(moscow['geometry'])[0]
        moscow_districts = pd.DataFrame()
        idx = 0
        for name, poly in zip(districts_df['local_name'], districts_df['geometry']):
            if moscow_geometry.contains(poly):
                for okr, geo in zip(okruga['local_name'], okruga['geometry']):
                    if geo.contains(poly):
                        moscow_districts.at[idx, 'okrug'] = okr
                        moscow_districts.at[idx, 'district'] = name
                        moscow_districts.at[idx, 'geometry'] = poly
            else:
                continue
            idx += 1
        return moscow_districts


    moscow_geometry_df = get_districts()


    def get_coords(lat, long):
        return Point(long, lat)


    df['coords'] = df[['lat', 'long']].apply(lambda x: get_coords(*x), axis=1)


    @st.cache(allow_output_mutation=True)
    def get_municipality():
        new_df = df.copy(deep=True)
        for idx, row in new_df.iterrows():
            coord = row.coords
            for distr, okr, geometry in zip(moscow_geometry_df['district'], moscow_geometry_df['okrug'],
                                            moscow_geometry_df['geometry']):
                if geometry.contains(coord):
                    new_df.at[idx, 'district'] = distr
                    new_df.at[idx, 'okrug'] = okr
                    break
                else:
                    continue
        return new_df


    full_df = get_municipality()

    m = folium.Map(location=[55.753544, 37.621211], zoom_start=10)
    FastMarkerCluster(
        data=[[lat, lon] for lat, lon in zip(full_df['lat'], full_df['long'])]
        , name='Заказы').add_to(m)

    folium_static(m)

    df_municipalities = full_df.groupby(['district'], as_index=False).agg({'id': 'count', 'amount_charged': 'mean'})
    df_municipalities



