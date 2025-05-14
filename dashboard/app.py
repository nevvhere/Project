import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter

# Загрузка CSS-стилей
def load_css():
    with open("dashboard/assets/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Загрузка данных
@st.cache_data
def load_data():
    return pd.read_csv("../data/soundcloud_tracks_cleaned.csv", sep=';')

# Анализ пользовательских тегов
def analyze_tags(tags_series):
    all_tags = []
    for tags in tags_series.dropna():
        all_tags.extend(tags.split())
    return Counter(all_tags)

# Основная функция
def main():
    # Инициализация
    load_css()
    st.title("📊 Аналитика SoundCloud")
    st.markdown("Визуализация данных о треках и их популярности")
    
    # Загрузка данных
    df = load_data()
    
    # Сайдбар с фильтрами
    with st.sidebar:
        st.header("Фильтры")
        selected_tags = st.multiselect(
            "Выберите жанры",
            options=df['tag'].unique(),
            default=df['tag'].unique()
        )
        min_plays = st.slider(
            "Минимальное число прослушиваний",
            min_value=int(df['listens'].min()),
            max_value=int(df['listens'].max()),
            value=int(df['listens'].quantile(0.25))
        )
    
    # фильтры
    filtered_df = df[
        (df['tag'].isin(selected_tags)) & 
        (df['listens'] >= min_plays)
    ]
    
    # Ключевые метрики
    col1, col2, col3 = st.columns(3)
    col1.metric("Всего треков", len(filtered_df))
    col2.metric("Средние прослушивания", f"{filtered_df['listens'].mean():,.0f}")
    col3.metric("Средние лайки", f"{filtered_df['likes'].mean():,.0f}")
    
    # Вкладки
    tab1, tab2, tab3 = st.tabs(["📈 Обзор", "🎵 По жанрам", "🏆 Топ треки"])
    
    with tab1:
        # Корреляционная матрица
        st.subheader("Корреляция между показателями")
        corr = filtered_df[['listens', 'likes', 'comments']].corr()
        fig2, ax = plt.subplots()
        sns.heatmap(corr, annot=True, cmap='coolwarm', ax=ax)
        st.pyplot(fig2)
    
    with tab2:
        st.header("Анализ по жанрам")
        
        # Сравнение жанров
        genre_stats = filtered_df.groupby('tag').agg({
            'listens': 'mean',
            'likes': 'mean',
            'comments': 'mean'
        }).reset_index()
        
        fig3 = px.bar(
            genre_stats,
            x='tag',
            y=['listens', 'likes', 'comments'],
            title="Средние показатели по жанрам",
            barmode='group',
            labels={'value': 'Среднее значение', 'variable': 'Метрика'}
        )
        st.plotly_chart(fig3, use_container_width=True)
        
        # Boxplot прослушиваний по жанрам
        fig4 = px.box(
            filtered_df,
            x='tag',
            y='listens',
            title="Распределение прослушиваний по жанрам",
            log_y=True
        )
        st.plotly_chart(fig4, use_container_width=True)
    
    with tab3:
        st.header("Топ треков")
        
        # Топ по прослушиваниям
        top_n = st.slider("Количество треков в топе", 5, 50, 10)
        top_tracks = filtered_df.nlargest(top_n, 'listens')
        
        fig5 = px.bar(
            top_tracks,
            x='listens',
            y='name',
            orientation='h',
            color='tag',
            title=f"Топ {top_n} треков по прослушиваниям",
            labels={'listens': 'Прослушивания', 'name': 'Название трека'}
        )
        st.plotly_chart(fig5, use_container_width=True)
        
        # Популярные теги в топе
        st.subheader("Популярные теги в топ-треках")
        tag_counts = analyze_tags(top_tracks['user_tags'])
        tags_df = pd.DataFrame(tag_counts.most_common(15), columns=['Тег', 'Количество'])
        
        fig6 = px.pie(
            tags_df,
            names='Тег',
            values='Количество',
            title="Распределение тегов в топ-треках"
        )
        st.plotly_chart(fig6, use_container_width=True)

if __name__ == "__main__":
    main()
