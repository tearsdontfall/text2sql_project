import requests 
import json
import time
import ollama

class SQLGenerator:
    def __init__(self, model="qwen2.5-coder:7b"):
        self.model = model
        # Это база знаний, которую модель помнит всегда
        self.system_instructions = {
            "role": "system",
            "content": """Ты — опытный SQL-аналитик. 
            Работай с таблицей 'metrica_hits'. 
            Колонки:
                - session_date (DATE): дата сессии (в формате 2025-MM-DD)
                - session_id (TEXT): уникальный ID сессии (UUID)
                - client_id (INTEGER): ID клиента (диапазон 10000-15000)
                - city (TEXT): название города
                - utm_source (TEXT): источник трафика ('yandex', 'vkads', 'telegram', 'hybrid', 'soloway', 'mintegral', 'organic')
                - event_type (TEXT): тип события ('page_view', 'ib_draft_created', 'sdelka_draft_created')
                - user_id (TEXT): уникальный ID пользователя (UUID)
            Разбивки:
            каналы - utm_source
            неделя - date(session_date, 'weekday 1')
            месяц - date('now','start of month','+0 month')
            год - date(session_date, 'start_of_year')
            Метрики:
            Черновики Сделка - COUNT(CASE WHEN event_type = 'sdelka_draft_created' THEN 1 ELSE NULL END)
            Черновики ИБ - COUNT(CASE WHEN event_type = 'ib_draft_created' THEN 1 ELSE NULL END)
            Черновики - COUNT(CASE WHEN event_type != 'page_view' THEN 1 ELSE NULL END)
            Сессии - COUNT(DISTINCT CASE WHEN event_type = 'page_view' session_id 1 ELSE NULL END)
            Уники - COUNT(DISTINCT CASE WHEN event_type = 'page_view' client_id 1 ELSE NULL END)
            Юзеры с Черновиком - COUNT(DISTINCT CASE WHEN event_type != 'page_view' THEN user_id ELSE NULL END)
            Правила:
            1. Пиши ТОЛЬКО чистый SQL-код для SQLite.
            2. Метрики считай только по формулам выше.
            3. Не используй Markdown (```).
            4. Если тебя просят 'отфильтровать' или 'добавить', учитывай предыдущие запросы.
            5. Если тебя просят поправить предыдущий запрос и присылают код ошибки - сделай коррекцию, но не добавляй никаких комментариев.
            6. Запрещены любые команды кроме SELECT."""
        }

        # Здесь будет храниться история текущей сессии
        self.history = [self.system_instructions]

    def get_sql(self, user_question):
        # Добавляем вопрос пользователя в историю
        self.history.append({"role": "user", "content": user_question})
        
        try:
            # Отправляем всю цепочку сообщений
            response = ollama.chat(model=self.model, messages=self.history)
            
            sql = response['message']['content'].strip()
            
            # Очистка (на всякий случай)
            sql = sql.replace('```sql', '').replace('```', '').strip()
            
            # Добавляем ответ модели в историю, чтобы она помнила, какой SQL составила
            self.history.append({"role": "assistant", "content": sql})
            
            return sql
            
        except Exception as e:
            return f"-- Ошибка Ollama: {str(e)}"

    def clear_history(self):
        """Метод для сброса контекста"""
        self.history = [self.system_instructions]

if __name__ == "__main__":
    SQLGenerator.get_sql("Покажи 3 строки")
