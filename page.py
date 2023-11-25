import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from PIL import Image

df = pd.read_csv('data/spotify_songs.csv')
df.duration_ms = df.duration_ms / 1000

df.dropna(axis = 0, inplace = True)

df_grouped = df.groupby(['playlist_genre', 'playlist_subgenre'])
df_count = df_grouped.count().reset_index()

cond = (df_count['track_name'] == max(df_count.drop(columns = ['playlist_genre','playlist_subgenre'])['track_name']))

df_mean = df_grouped.mean().reset_index()

popular_gen = ['edm', 'rap', 'pop']
unpopular_gen = ['r&b', 'latin', 'rock']

cond_popular = (df_mean['playlist_genre'] == popular_gen[0]) | (df_mean['playlist_genre'] == popular_gen[1]) | (df_mean['playlist_genre'] == popular_gen[2])
cond_unpopular = (df_mean['playlist_genre'] == unpopular_gen[0]) | (df_mean['playlist_genre'] == unpopular_gen[1]) | (df_mean['playlist_genre'] == unpopular_gen[2])

df_mean_pop = df_mean.loc[cond_popular, :]
df_mean_unpop = df_mean.loc[cond_unpopular, :]

# ==================
# layout streamlit
# ==================

st.set_page_config(layout = 'wide')

path = 'images/image.png'
image = Image.open(path)
st.sidebar.image(image, width = 120)

st.sidebar.markdown('# Analise exploratoria do dataset spotify 300000')
st.sidebar.markdown("""---""")

st.sidebar.markdown('## Selecione um genero')

generos = list(df_count.playlist_genre.unique())

genre_selector = st.sidebar.selectbox(
    'Escolha um genero de musica',
    generos
)

if genre_selector == 'rock':
    subgenre_selector = st.sidebar.selectbox(
        'Escolha um subgenero',
        ['album rock', 'classic rock', 'hard rock', 'permanent wave']
    )

elif genre_selector == 'edm':
    subgenre_selector = st.sidebar.selectbox(
        'Escolha um subgenero',
        ['big room', 'electro house', 'pop edm', 'progressive electro house']
    )

elif genre_selector == 'latin':
    subgenre_selector = st.sidebar.selectbox(
        'Escolha um subgenero',
        [ 'latin hip hop', 'latin pop', 'reggaeton', 'tropical']
)

elif genre_selector == 'pop':
    subgenre_selector = st.sidebar.selectbox(
        'Escolha um subgenero',
        ['dance pop', 'electropop', 'indie poptimism', 'post-teen pop']
)

elif genre_selector == 'r&b':
    subgenre_selector = st.sidebar.selectbox(
        'Escolha um subgenero',
        [ 'hip pop', 'neo soul',  'new jack swing', 'urban contemporary']
)

elif genre_selector == 'rap':
    subgenre_selector = st.sidebar.selectbox(
        'Escolha um subgenero',
        ['gangster rap', 'hip hop', 'southern hip hop', 'trap']
    
    )
tab1, tab2 = st.tabs(['Visao geral', 'Visao do usuario'])

with tab1:
    with st.container():
        st.markdown('## Popularidade por genero e subgenero')
        fig = px.sunburst(df, path = ['playlist_genre', 'playlist_subgenre'], color = 'track_popularity')
        st.plotly_chart(fig, use_container_width = True)
        st.markdown("""---""")

        st.markdown('## Quao animados sao os generos')
        fig = px.sunburst(df, path = ['playlist_genre', 'playlist_subgenre'], color = 'valence')
        st.plotly_chart(fig, use_container_width = True)
        st.markdown("""---""")

        st.markdown('## Distribuicao de musicas por genero e subgenero')
        fig = px.treemap(df_count, path = ['playlist_genre', 'playlist_subgenre'], values = 'track_name')
        st.plotly_chart(fig, use_container_width = True)

        col1, col2, col3 = st.columns(3)
        with col1:
            with st.container():
                st.markdown('### Quao bom de dancar sao as mais escutadas')
                fig = px.bar(df_mean_pop, x = 'playlist_genre', y = 'danceability', color = 'playlist_subgenre').update_xaxes(categoryorder = 'total ascending')
                fig.update_layout(showlegend = False)
                st.plotly_chart(fig, use_container_width = True)
                st.markdown("""---""")

        with col2:
            with st.container():
                st.markdown('### Quao alegre sao as musicas mais escutadas')
                fig = px.bar(df_mean_pop, x = 'playlist_genre', y = 'valence', color = 'playlist_subgenre').update_xaxes(categoryorder = 'total ascending')
                fig.update_layout(showlegend = False)
                st.plotly_chart(fig, use_container_width = True)
                st.markdown("""---""")

        with col3:
            with st.container():
                st.markdown('### Popularidade dentre as mais escutadas por subgenero')
                fig = px.scatter(df_mean_pop, x = 'track_popularity', y = 'playlist_genre', color = 'playlist_subgenre')
                st.plotly_chart(fig, use_container_width = True)
                st.markdown("""---""")

        with col1:
            with st.container():
                st.markdown('### Quao bom de dancar sao as menos escutadas')
                fig = px.bar(df_mean_unpop, x = 'playlist_genre', y = 'danceability', color = 'playlist_subgenre').update_xaxes(categoryorder = 'total ascending')
                fig.update_layout(showlegend = False)
                st.plotly_chart(fig, use_container_width = True)
                st.markdown("""---""")
        
        with col2:
            with st.container():
                st.markdown('### Quao alegres sao as menos escutadas')
                fig = px.bar(df_mean_unpop, x = 'playlist_genre', y = 'valence', color = 'playlist_subgenre').update_xaxes(categoryorder = 'total ascending')
                fig.update_layout(showlegend = False)
                st.plotly_chart(fig, use_container_width = True)
                st.markdown("""---""")

        with col3:
            with st.container():
                st.markdown('### Popularidade dentre as menos escutadas por subgenero')
                fig = px.scatter(df_mean_unpop, x = 'track_popularity', y = 'playlist_genre', color = 'playlist_subgenre')
                st.plotly_chart(fig, use_container_width = True)
                st.markdown("""---""")

        st.markdown('## generos e subgeneros com faixas mais longas')
        fig = px.bar(df_mean, x = 'playlist_genre', y = 'duration_ms', color = 'playlist_subgenre').update_xaxes(categoryorder = 'total ascending')
        st.plotly_chart(fig, use_container_width = True)


with tab2:
    with st.container():
        df_aux = df.loc[df['playlist_subgenre'] == subgenre_selector, :]
        df_aux2 = df.loc[df['playlist_genre'] == genre_selector, :]

        st.markdown('## Distribuicao popularidade do genero e subgeneros')
        fig = px.histogram(df_aux2, x = 'track_popularity', color = 'playlist_subgenre')
        st.plotly_chart(fig, use_container_width = True)
        st.markdown("""----""")

        st.markdown('## Distribuicao de duracao de faixas por genero e subgenero escolhido')
        fig = px.histogram(df_aux, x = 'duration_ms')
        st.plotly_chart(fig, use_container_width = True)
        st.markdown("""---""")

        st.markdown('## Quao alegre e o subgenero selecionado')
        fig = px.histogram(df_aux, x = 'valence')
        st.plotly_chart(fig, use_container_width = True)
        st.markdown("""---""")

        st.markdown('## Quao bom e de dancar um subgenero')
        fig = px.histogram(df_aux, x = 'danceability')
        st.plotly_chart(fig, use_container_width = True)
        st.markdown("""---""")