import streamlit as st
import pandas as pd
from PIL import Image
import matplotlib
import seaborn as sns
with st.echo(code_location='below'):
    matplotlib.use("Agg")
    st.set_option('deprecation.showPyplotGlobalUse', False)

    @st.cache(persist=True, show_spinner=True)
    def get_data(rows):
        data_url = (
            "https://github.com/fatcat-klm/vsosh2.0/raw/main/moscow%20schools%20-%20winners%20-%20moscow%20schools%20-%20winners%20(2)%20-%20moscow%20schools%20-%20winners%20-%20moscow%20schools%20-%20winners%20(2).csv.zip")
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
    st.info("Если при построении выдается ошибка, то формат выбранного параметра не подходит для построения графика такого типа. Выберите другой")
    if st.sidebar.checkbox('Count Plot'):
        st.subheader('Count Plot')
        column_count_plot_x = st.sidebar.selectbox("Х Подходят только числовые значения: ", df.columns)
        column_count_plot_y = st.sidebar.selectbox("Y дополнительная переменная:",
                                       df.columns.insert(0, None))
        fig = sns.countplot(x=column_count_plot_x, hue=column_count_plot_y, data=df, palette="husl", labels=[df.columns.insert(0, None)])
        st.pyplot()

    if st.sidebar.checkbox('Boxplot'):
        st.subheader('Boxplot')
        column_box_plot_X = st.sidebar.selectbox("X Подходят только числовые значения:",df.columns)
        column_box_plot_Y = st.sidebar.selectbox("Y: ",df.columns.insert(0, None))
        column_box_plot_Z = st.sidebar.selectbox("Z дополнительная переменная:", df.columns.insert(0, None))
        fig = sns.boxplot(x=column_box_plot_X, y=column_box_plot_Y, hue=column_box_plot_Z, data=df, palette="husl", labels=[df.columns.insert(0, None)])
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
    df_group_for_address = df.query('df_Year=="2019/2020"').query('df_Stage=="4"').groupby(['df_ShortName', 'Subject'], as_index=False)['df_Add'].sum()
    st.write(df_group_for_address)

    ## Importing the required modules
    import pandas as pd
    from geopy.geocoders import Nominatim
    from geopy.extra.rate_limiter import RateLimiter

    # Creating a dataframe with address of locations we want to reterive
    #locat = ['Coorg, Karnataka', 'Khajjiar, Himachal Pradesh', \
             'Chail, Himachal Pradesh', 'Pithoragarh, Uttarakhand', 'Munnar, Kerala']
    #df = pd.DataFrame({'add': locat})

    # Creating an instance of Nominatim Class
    #geolocator = Nominatim(user_agent="my_request")

    # applying the rate limiter wrapper
    #geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)

    # Applying the method to pandas DataFrame
    #df['location'] = df['add'].apply(geocode)
    #df['Lat'] = df['location'].apply(lambda x: x.latitude if x else None)
    ##df['Lon'] = df['location'].apply(lambda x: x.longitude if x else None)
    #
    #  df
