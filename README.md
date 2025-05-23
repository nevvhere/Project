# Анализ треков SoundCloud

## Авторы

**Герасимова Мелания Петровна**

ИСУ: 465525

Парсинг, очистка и подготовка данных

**Загитова Маргарита Евгеньевна**

ИСУ: 465916

Анализ данных, dashboard

## Описание проекта

Наш проект анализирует данные треков SoundCloud, чтобы понять:
- Как теги влияют на популярность треков (прослушивания, лайки, комментарии)
- Какие теги самые популярные среди выбранных категорий (хип-хоп, джаз, чилл, трэп, инди, поп)

## Возможности

- Интерактивная панель с визуализацией данных
- Анализ популярности тегов и вовлеченности аудитории
- Сравнение музыкальных жанров
- Визуализация самых популярных треков
- Анализ корреляции между прослушиваниями, лайками и комментариями

## Установка и запуск

Клонируйте репозиторий и установите зависимости одной командой:
```bash
git clone https://github.com/nevvhere/Project.git && \
cd Project && \
pip3 install -r requirements.txt && \
streamlit run dashboard/app.py
```

## Использование

**После запуска панели вы можете:**

Просматривать общую статистику по трекам

Фильтровать данные по жанру/тегу

Исследовать корреляции между метриками

Видеть топ треков по разным критериям

Анализировать популярность пользовательских тегов
