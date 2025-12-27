import streamlit as st
import plotly.express as px
from src.analyst import DataAnalyst

# Конфигурация страницы
st.set_page_config(page_title="AI Data Analyst", layout="wide")
st.title("🤖 Твой AI-Аналитик (Metrica DB)")

# Инициализируем аналитика один раз
if "analyst" not in st.session_state:
    st.session_state.analyst = DataAnalyst()

# Боковая панель
with st.sidebar:
    st.header("Настройки")
    if st.button("🗑 Очистить историю"):
        st.session_state.analyst.llm.clear_history()
        st.success("Память очищена")
    
    st.info("Доступные источники: yandex, vkads, telegram, organic и др.")

question = st.text_input("Задай вопрос к базе данных:", placeholder="Например: Покажи динамику сессий по дням")

if question:
    # Вызываем логику с ретраями
    df, sql, error = st.session_state.analyst.ask(question)
    
    st.code(sql, language="sql")
    
    if error:
        st.error(f"Не удалось исправить запрос: {error}")
    elif df is not None:
        col1, col2 = st.columns([1, 1])
            
        with col1:
            st.subheader("📊 Данные")
            st.dataframe(df, use_container_width=True)

        with col2:
            st.subheader("📈 Визуализация")
            # Авто-подбор графика
            cols = df.columns.tolist()
            date_keywords = ['date', 'week', 'year', 'day', 'month', 'quarter', 'session_date']
            has_date = any(any(key in col.lower() for key in date_keywords) for col in cols)
            
            if has_date and 'SELECT *' not in sql:
                # Если есть дата — рисуем линию, иначе — столбчатую диаграмму
                chart_type = px.line
                fig = chart_type(df, x=cols[0], y=cols[1], title=f"Зависимость {cols[1]} от {cols[0]}")
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.write("Невозможно построить график")





# import streamlit as st
# import pandas as pd
# import sqlite3
# import plotly.express as px
# from src.llm_client import SQLGenerator
# from main import execute_query

# # Конфигурация страницы
# st.set_page_config(page_title="AI Data Analyst", layout="wide")

# st.title("🤖 Твой AI-Аналитик (Metrica DB)")

# # Инициализация LLM в состоянии сессии, чтобы не сбрасывать историю при каждом клике
# if "llm" not in st.session_state:
#     st.session_state.llm = SQLGenerator()

# # Боковая панель
# with st.sidebar:
#     st.header("Настройки")
#     if st.button("🗑 Очистить историю"):
#         st.session_state.llm.clear_history()
#         st.success("Память очищена")
    
#     st.info("Доступные источники: yandex, vkads, telegram, organic и др.")

# # Основной интерфейс
# question = st.text_input("Задай вопрос к базе данных:", placeholder="Например: Покажи динамику сессий по дням")

# if question:
#     with st.spinner("Думаю над SQL..."):
#         sql_query = st.session_state.llm.get_sql(question)
    
#     st.code(sql_query, language="sql")
    
#     try:
#         # Выполнение запроса
#         conn = sqlite3.connect('yandex_metrica_fake_data.db')

#         # result = execute_query()

#         df = pd.read_sql_query(sql_query, conn)
#         conn.close()
        
#         if df.empty:
#             st.warning("Данные не найдены")
#         else:
#             # Разделяем экран на две колонки: Таблица и График
#             col1, col2 = st.columns([1, 1])
            
#             with col1:
#                 st.subheader("📊 Данные")
#                 st.dataframe(df, use_container_width=True)
            
#             with col2:
#                 st.subheader("📈 Визуализация")
#                 # Авто-подбор графика
#                 cols = df.columns.tolist()
                
#                 if len(cols) >= 2:
#                     # Если есть дата — рисуем линию, иначе — столбчатую диаграмму
#                     chart_type = px.line if "date" in str(cols).lower() else px.bar
#                     fig = chart_type(df, x=cols[0], y=cols[1], title=f"Зависимость {cols[1]} от {cols[0]}")
#                     st.plotly_chart(fig, use_container_width=True)
#                 else:
#                     st.write("Недостаточно колонок для построения графика")
                    
#     except Exception as e:
#         st.error(f"Ошибка выполнения SQL: {e}")