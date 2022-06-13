import matplotlib
import folium as folium
import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
from folium.plugins import FastMarkerCluster
from geopy import distance
import networkx as nx
from matplotlib.pyplot import figure
from shapely.geometry import Point
from streamlit_folium import st_folium, folium_static
import plotly.express as px
from geopy.geocoders import Nominatim

with st.echo(code_location='below'):
    matplotlib.use("Agg")
    st.set_option('deprecation.showPyplotGlobalUse', False)


    @st.cache(persist=True, show_spinner=True)
    def get_data(rows):
        data_url = (
            "https://github.com/fatcat-klm/vsosh/raw/main/flavors_of_cacao%20(2)%20-%20flavors_of_cacao%20(2)%20(1).csv.zip")
        df = pd.read_csv(data_url, nrows=rows)
        return df


    df = get_data(7)
    st.sidebar.subheader('Описание параметров датасета')
    st.sidebar.subheader('Анализировать данные')
    st.markdown("### Что-то про  шоколад")
    st.markdown("Что-то прикольное паро шоколад пишем")
    if st.button("🎈"):
        st.balloons()
    st.markdown(
        "Проанализировав различные характеристики датасета вы сможете выявить зависимости. Например,чего-то там")
    st.markdown(" ### Приступить к анализу данных")
    if st.checkbox("Показать датасет", False):
        st.subheader('Датасет')
        st.write(df)
    df1 = df.copy(deep=True)

    if st.checkbox("Построим рейтинг по странам проихзводителям", False):
        st.subheader('Рейтинг')
        dict1 = df1.groupby('Company').aggregate(np.sum)['Add'].to_dict()
        sorted_values = sorted(dict1.values())
        new_sorted_dict = {}
        for i in sorted_values:
            for j in dict1.keys():
                if dict1[j] == i:
                    new_sorted_dict[j] = dict1[j]
                    break
        st.write(new_sorted_dict)

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
        "[Источник исходного датасета](https://www.kaggle.com/datasets/rtatman/chocolate-bar-ratings)")

    st.markdown("Граф")
    if st.checkbox("Показать граф", False):
        df2 = df.copy(deep=True)
        df3 = df2[['Specific_Bean_Origin', 'Company_Location']]
        G = nx.Graph()
        G = nx.from_pandas_edgelist(df3, 'Specific_Bean_Origin', 'Company_Location')
        figure(figsize=(10, 8))
        nx.draw_shell(G, with_labels=True)

    st.title('Геоданные')


    def get_coords(lat, lon):
        try:
            return Point(lon, lat)
        except Exception as e:
            raise ValueError('get_coords: {} {}'.format(lat, lon))


    @st.experimental_singleton()
    def final_df():
        d = df.drop(['coords'], axis=1).copy(deep=True)
        return d
    # df_new = final_df()


    if st.checkbox("Показать геоданные", False):
        st.subheader('Геоданные')
        df_new = df.copy(deep=True)

        st.write(df_new['lat'])

        df_new['coords'] = df_new[['lat', 'lon']].apply(lambda x: get_coords(*x), axis=1)
        df_new = df_new.drop(['coords'], axis=1).copy(deep=True)

        m = folium.Map(location=[55.753544, 37.621211], zoom_start=10)
        FastMarkerCluster(data=[[lat, lon] for lat, lon in zip(df_new['lat'], df_new['lon'])]).add_to(m)
        folium_static(m)
